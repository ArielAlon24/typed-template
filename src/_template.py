from ._specifier_deleter import SpecifierDeleter
from typing import get_type_hints
from typeguard import check_type, TypeCheckError
import ast
import os
import sys
import inspect


class Template:
    _CALLER_FRAME = "f_back"
    _GLOBALS_KEY = "_globals"

    def __new__(cls, _: str):
        instance = super(Template, cls).__new__(cls)

        frame = getattr(inspect.currentframe(), cls._CALLER_FRAME, None)
        if not frame:
            raise ValueError("Could not find the caller frame.")

        module_name = inspect.getmodule(frame).__name__

        setattr(instance, cls._GLOBALS_KEY, sys.modules[module_name].__dict__)

        return instance

    def __init__(self, content: str) -> None:
        parsed_ast = self._parse_ast(content)
        specifier_deleter = SpecifierDeleter()
        modified_ast = specifier_deleter.visit(parsed_ast)
        constant = modified_ast.body
        self.content = ast.literal_eval(ast.unparse(constant))
        self.__annotations__ = get_type_hints(
            specifier_deleter, globalns=getattr(self, self._GLOBALS_KEY)
        )

    @staticmethod
    def _parse_ast(content: str) -> ast.Expression:
        f_string = f'f"""{content}"""'
        return ast.parse(f_string, mode="eval")

    def format(self, **kwargs) -> str:
        values = {}
        for key, annotation in self.__annotations__.items():
            if key not in kwargs:
                raise ValueError(
                    f"Template uses {tuple(self.__annotations__.keys())} keys but is missing replacment '{key}'."
                )

            value = kwargs[key]
            try:
                check_type(value, annotation)
            except TypeCheckError:
                raise TypeError(
                    f"Incorrect type for replacment '{key}', expected: {annotation}."
                )
            values[key] = str(value)

        return self.content.format(**values)


class FileTemplate(Template):
    def __init__(self, path: str) -> None:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File path: {path} was not found.")
        with open(path) as file:
            content = file.read()
        super().__init__(content=content)
