from ._parsing_error import ParsingError
import ast
from typing import Dict, Any


class SpecifierDeleter(ast.NodeTransformer):
    def __init__(self) -> None:
        self.__annotations__: Dict[str, Any] = {}
        self.inside = False

    def visit_Constant(self, node: ast.Constant) -> str:
        return node.value

    def visit_FormattedValue(self, node: ast.FormattedValue) -> str:
        name = getattr(node.value, "id", None)
        if not name:
            raise ParsingError("A replacment must include a name.")

        format_spec = node.format_spec
        if not isinstance(format_spec, ast.JoinedStr):
            raise ParsingError("Cannot find format specifier string.")

        if len(format_spec.values) != 1:
            raise ParsingError(
                "Currenly only type annotation in the format specifier is allowed."
            )

        constant = format_spec.values[0]
        if not isinstance(constant, ast.Constant):
            raise ParsingError("Could not find Constant node for type annotation.")
        annotation = constant.value

        self.__annotations__[name] = annotation.strip()
        return "{" + name + "}"

    def visit_JoinedStr(self, node: ast.JoinedStr) -> Any:
        string = ""
        for sub_node in node.values:
            if isinstance(sub_node, ast.Constant):
                string += self.visit_Constant(sub_node)
            elif isinstance(sub_node, ast.FormattedValue):
                string += self.visit_FormattedValue(sub_node)

        return ast.Constant(value=string)
