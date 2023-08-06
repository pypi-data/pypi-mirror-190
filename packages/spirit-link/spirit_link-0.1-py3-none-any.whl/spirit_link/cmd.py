from wisepy2 import wise
from pathlib import Path
from spirit_link.descriptors import Node
from importlib import import_module
from colorama import Fore, Style
import spirit_link.backends.dot as dot_backend
import sys
import os


# import python source file from a given path
def import_path(path: str):
    from importlib.util import spec_from_file_location, module_from_spec
    spec = spec_from_file_location("__tmp__.spirit_link", path)
    if not spec:
        raise ValueError(f"cannot import {path}")
    module = module_from_spec(spec)
    loader = spec.loader
    if not loader:
        raise ValueError(f"cannot import {path}")
    loader.exec_module(module)
    return module

class Cmd:

    @staticmethod
    def run(filename: str, o: str = "", backend: str = "dot"):
        if filename.endswith(".pdf"):
            raise ValueError("input filename must not end with .pdf")

        o = o or Path(filename).with_suffix(".pdf").as_posix()
        p_input = Path(filename)
        sys.path.append(Path.cwd().as_posix())
        if p_input.is_file():
            if p_input.suffix == '.py':
                m = import_path(filename)
            else:
                raise ValueError(f"unknown file type {p_input.suffix}")
        elif p_input.is_dir():
            sys.path.append(p_input.parent.absolute().as_posix())
            m = import_module(p_input.name)
        else:
            raise ValueError(f"unknown input {filename}")
        root = getattr(m, 'root', None)
        outliers = getattr(m, 'outliers', ())
        if not isinstance(root, Node):
            raise ValueError("root must be a Node")
        if backend == "dot":
            g = dot_backend.build_graph(top=root, outliers=outliers)
            dot_backend.output(g, o)
        else:
            raise ValueError(f"unknown backend {backend}")


def entry():
    wise(Cmd.run)()
