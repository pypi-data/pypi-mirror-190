from __future__ import annotations
import graphviz_artist.graph as ga
import graphviz_artist.attr as attr
from graphviz import Digraph
import typing


import spirit_link.descriptors as desc

class Splines(attr.Attr):
    def __init__(self, value: typing.Literal['polyline', 'ortho', 'true', 'false']):
        attr.Attr.__init__(self, value)

class FontName(attr.Attr):
    pass

class Ratio(attr.Attr):
    def __init__(self, value: float):
        attr.Attr.__init__(self, str(value))

class Url(attr.Attr):
    pass

class Tooltip(attr.Attr):
    pass


_default_splines = Splines('ortho')
_link_spines = Splines('polyline')

_T = typing.TypeVar('_T')

def build_graph(
        top: desc.Node, font: str = 'Microsoft YaHei',
        outliers: typing.Sequence[desc.Node] = ()
    ):
    self = GraphBuilder(top, font)
    for each in outliers:
        self.build_node(each)

    self.build_node(self.top)
    return self

def output(d: GraphBuilder, filename: str):
    d.graph.update()
    if not filename.endswith(".pdf"):
        raise ValueError("filename should end with .pdf")
    d.graph.g.render(filename[:-len(".pdf")]) # type: ignore

class Built:
    node: ga.Node
    is_built: bool

    def __init__(self, node: ga.Node, is_built: bool):
        self.node = node
        self.is_built = is_built

class GraphBuilder:

    def __init__(self, top: desc.Node, font: str = 'Microsoft YaHei'):
        dot = Digraph(filename=getattr(top, "name", "digraph"), format="pdf")
        self.font = FontName(font)
        self.graph = ga.Graph(_default_splines, Ratio(0.7), self.font, directed=True, dot=dot)
        self.styles: dict[object, typing.Sequence[attr.Attr]] = {}
        self.top = top
        self.visited_nodes: dict[desc.Node, Built] = {}

        self.add_style(desc.Project, (attr.Shape("folder"), attr.Color("goldenrod1")))
        self.add_style(desc.Requirement, (attr.Shape("doublecircle"), attr.Color("crimson")))
        self.add_style(desc.Document, (attr.Shape("note"), attr.Color("cornflowerblue")))
        self.add_style(desc.Link, (attr.Shape("rarrow"), attr.Color("darkcyan")))
        self.add_style(desc.Module, (attr.Shape("component"), attr.Color("darkolivegreen3")))
        self.add_style(desc.Task, (attr.Shape("box"), attr.Color("coral2")))

    def add_style(self, node_type, styles: typing.Sequence[attr.Attr]):
        self.styles[node_type] = styles

    def analyze_links_(self, in_node: desc.Node, out_node: ga.Node):
        for to, edge in in_node.rel.links.items():
            x = self.create_node(to, bind = lambda x: x).node
            _ = out_node[self.font, attr.Color("deeppink4"), _link_spines, attr.XLabel(edge)] == x

        for to, edge in in_node.rel.requires.items():
            x = self.create_node(to, bind = lambda x: x).node

            _ = out_node[self.font, attr.Color("dodgerblue2"), _link_spines, attr.XLabel(edge)] > x


    def create_project(self, node_in: desc.Project):
        visited_nodes = self.visited_nodes
        if n := visited_nodes.get(node_in):
            return n
        n = self.graph.new(
            attr.Label(node_in.name),
            self.font
        )
        n.update(*self.styles.get(type(node_in), ()))
        r = visited_nodes[node_in] = Built(n, False)
        return r

    def create_requirement(self, node_in: desc.Requirement):
        visited_nodes = self.visited_nodes
        if n := visited_nodes.get(node_in):
            return n
        n = self.graph.new(
            attr.Label(node_in.title),
            Tooltip(node_in.description),
            self.font
        )
        n.update(*self.styles.get(type(node_in), ()))
        r = visited_nodes[node_in] = Built(n, False)
        return r

    def create_document(self, node_in: desc.Document):
        visited_nodes = self.visited_nodes
        if n := visited_nodes.get(node_in):
            return n
        n = self.graph.new(
            attr.Label(node_in.filepath),
            attr.Shape("note"),
            self.font
        )
        n.update(*self.styles.get(type(node_in), ()))
        r = visited_nodes[node_in] = Built(n, False)
        return r

    def create_link(self, node_in: desc.Link):
        visited_nodes = self.visited_nodes
        n = self.graph.new(
            attr.Label(node_in.show),
            Tooltip(node_in.url),
            self.font
        )
        n.update(*self.styles.get(type(node_in), ()))
        r = visited_nodes[node_in] = Built(n, False)
        return r

    def create_module(self, node_in: desc.Module):
        visited_nodes = self.visited_nodes
        n = self.graph.new(
            attr.Label(node_in.name),
            self.font
        )
        n.update(*self.styles.get(type(node_in), ()))
        r = visited_nodes[node_in] = Built(n, False)
        return r

    def create_task(self, node_in: desc.Task):
        visited_nodes = self.visited_nodes
        n = self.graph.new(
            attr.Label(node_in.name),
            self.font
        )
        n.update(*self.styles.get(type(node_in), ()))
        r = visited_nodes[node_in] = Built(n, False)
        return r

    def build_children_(self, in_node: desc.Node, out_node: ga.Node):
        for node in in_node.children:
            _ = out_node[self.font] > self.build_node(node)

    def create_node(self, node: desc.Node, bind: typing.Callable[[Built], _T]) -> _T:
        visited_nodes = self.visited_nodes
        if n_and_built := visited_nodes.get(node):
            return bind(n_and_built)
        if isinstance(node, desc.Project):
            n_and_built = self.create_project(node)
        elif isinstance(node, desc.Requirement):
            n_and_built = self.create_requirement(node)
        elif isinstance(node, desc.Document):
            n_and_built = self.create_document(node)
        elif isinstance(node, desc.Link):
            n_and_built = self.create_link(node)
        elif isinstance(node, desc.Module):
            n_and_built = self.create_module(node)
        elif isinstance(node, desc.Task):
            n_and_built = self.create_task(node)
        else:
            raise TypeError(f'Unknown node type: {type(node)}')
        self.analyze_links_(node, n_and_built.node)
        return bind(n_and_built)


    def build_node(self, node: desc.Node) -> ga.Node:
        def bind(built: Built):
            if built.is_built:
                return built.node
            self.build_children_(node, built.node)
            return built.node

        n = self.create_node(
            node,
            bind=bind
        )

        return n
