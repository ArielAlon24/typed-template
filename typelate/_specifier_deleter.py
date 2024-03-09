from ._parsing_error import ParsingError
import ast
from typing import Dict, Any


class SpecifierDeleter(ast.NodeTransformer):
    def __init__(self) -> None:
        self.__annotations__: Dict[str, Any] = {}
        self.inside = False

    def visit_JoinedStr(self, node: ast.JoinedStr) -> Any:
        string = ""
        for sub_node in node.values:
            if isinstance(sub_node, ast.Constant):
                string += self._parse_constant(sub_node)
            elif isinstance(sub_node, ast.FormattedValue):
                string += self._parse_formatted_value(sub_node)

        return ast.Constant(value=string)

    def _parse_constant(self, node: ast.Constant) -> str:
        return node.value

    def _parse_formatted_value(self, node: ast.FormattedValue) -> str:
        name = getattr(node.value, "id", None)
        if not name:
            raise ParsingError("A replacment must include a name.")

        format_spec = node.format_spec
        if not isinstance(format_spec, ast.JoinedStr):
            raise ParsingError("Cannot find format specifier string.")

        constant = format_spec.values[0]
        if not isinstance(constant, ast.Constant):
            raise ParsingError("Could not find Constant node for type annotation.")

        value = constant.value.replace(" ", "")

        return self._parse_format_specifier(name=name, value=value)

    def _parse_format_specifier(self, name: str, value: str) -> str:
        parts = value.split(":")

        annotation = None
        format_specifier = None
        if len(parts) == 1:
            annotation = parts[0]
        elif len(parts) == 2:
            annotation, format_specifier = parts
        else:
            raise ParsingError(
                "Format specifier must be <annotation> or <annotation: format> "
            )

        self.__annotations__[name] = annotation

        if format_specifier:
            return "{" + name + ":" + format_specifier + "}"
        return "{" + name + "}"
