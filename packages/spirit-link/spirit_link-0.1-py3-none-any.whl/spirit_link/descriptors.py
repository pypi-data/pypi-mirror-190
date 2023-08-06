from __future__ import annotations
import abc
import typing

_N = typing.TypeVar('_N', bound='Node')

class Tag:
    """继承Tag类型创建一种标签。
    同类标签可以是没有差异的，如“项目已延期”这样的tag。
    但同类可以是有差异的，例如“项目进度”可以是“已完成”，“进行中”，“未开始”等：这可以用继承自Tag的枚举类型实现。
    """
    name: str

标签 = Tag

class Relationship:
    """Relationship是Node的一个属性，用于描述和其他Node之间的关系。
    Relationship由三部分组成
    1. links：与其他Node的链接关系，可以是多对多的关系
    2. requires：对其他Node的依赖关系，是一对多的关系
    3. tags：一组标签
    """
    links: dict[Node, str]
    requires: dict[Node, str]
    tags: set[Tag]

    def __init__(self, *, links: dict[_N, str] | None = None, requires: dict[_N, str] | None = None, tags: list[Tag] | None = None):
        self.links = typing.cast('dict[Node, str]', links or {})
        self.requires = typing.cast('dict[Node, str]', requires or {})
        self.tags = set(tags or [])

关系 = Relationship

class Node(abc.ABC):
    """Node是SpiritLink的基本元素，它可以是Requirement、Project、Task、Module、Link等。
    用户可以在Node之间创建联系，可以在Node上添加标签。
    所有Node都具有以下组件：
    1. children：所有子Node对象形成的列表
    2. rel：一个Relationship对象，用于描述和其他Node之间的关系
    """
    children: list[Node]
    rel: Relationship

    def __init__(self, children: list[_N] | None = None, rel: Relationship | None = None):
        self.children = typing.cast('list[Node]', children or [])
        self.rel = rel or Relationship()

    def depends(self, other: Node_, edge: str = "依赖"):
        """创建一个依赖关系
        """
        self.rel.requires[other] = edge

    def link(self, other: Node_, edge: str = ""):
        """创建一个链接关系
        """
        self.rel.links[other] = edge

    def tag(self, tag: Tag):
        """添加一个标签
        """
        self.rel.tags.add(tag)

    @abc.abstractmethod
    def short_repr(self) -> str:
        raise NotImplementedError

节点 = Node

class Requirement(Node):
    """需求是SpiritLink的核心元素，它有一个标题和一个简述。
    """

    title: str
    description: str
    def __init__(self,
                 title: str,
                 description: str = "",
                 children: list[Node_] | None = None,
                 rel: Relationship | None = None):
        self.title = title
        self.description = description
        super().__init__(children, rel=rel)

    def short_repr(self):
        return self.title


需求 = Requirement

class Project(Node):
    """项目是SpiritLink的核心元素，它有一个名称。
    """

    def __init__(self, name: str, children: list[_N] | None = None, rel: Relationship | None = None):
        self.name = name
        super().__init__(children, rel=rel)

    def short_repr(self):
        return self.name


项目 = Project

class Task(Node):
    """具体任务是SpiritLink的核心元素，它有一个内容字符串。
    """
    name: str
    def __init__(self, name: str, children: list[_N] | None = None, rel: Relationship | None = None):
        self.name = name
        super().__init__(children, rel=rel)

    def short_repr(self):
        return self.name

任务 = Task

class Module(Node):
    """模块是SpiritLink的核心元素，它有一个名称。
    """

    def __init__(self, name: str, children: list[_N] | None = None, rel: Relationship | None = None):
        self.name = name
        super().__init__(children, rel=rel)

    def short_repr(self):
        return self.name

模块 = Module

class Link(Node):
    """链接是SpiritLink的核心元素，它有一个显示名称和一个链接地址。
    """
    show: str
    url: str
    def __init__(self, show: str, url: str, children: list[_N] | None = None, rel: Relationship | None = None):
        self.show = show
        self.url = url
        super().__init__(children, rel=rel)

    def short_repr(self):
        return self.show

链接 = Link

class Document(Node):
    """Document是SpiritLink的核心元素，它有一个文件路径和一个文件格式（可选）。
    """
    filepath: str
    format: str | None = ""

    def __init__(self, filepath: str, format: str | None = None, children: list[_N] | None = None, rel: Relationship | None = None):
        self.filepath = filepath
        self.format = format
        super().__init__(children, rel=rel)

    def short_repr(self):
        from pathlib import Path
        return Path(self.filepath).name

文档 = Document

Node_ = Document | Link | Module | Project | Requirement | Task
