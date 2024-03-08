from __future__ import annotations
from ._specifier_deleter import SpecifierDeleter
from typing import get_type_hints, Any, Dict, Tuple
from typeguard import check_type, TypeCheckError
import types
import ast
import os
import inspect


class Template(str):
    _CALLER_FRAME = "f_back"

    __slots__ = ("__annotations__",)

    def __new__(
        cls,
        content: Any,
        *,
        _annotations: Dict[str, Any] | None = None,
        _is_preprocessed: bool = False,
    ):
        annotations = {}
        if _is_preprocessed:
            instance = super().__new__(cls, content)
            if not _annotations:
                raise ValueError(
                    "A preprocessed Template must provide __annotations__ dict."
                )
            annotations = _annotations
        else:
            frame = getattr(inspect.currentframe(), "f_back", None)
            if not frame:
                raise ValueError("Could not find caller's frame.")

            content, annotations = cls._parse(content, frame)
            instance = super().__new__(cls, content)

        instance.__annotations__ = annotations

        return instance

    def __init__(self, content: str) -> None:
        super().__init__()

    @staticmethod
    def _parse(content: str, frame: types.FrameType) -> Tuple[str, Dict[str, Any]]:
        f_string = f'f"""{content}"""'
        parsed_ast = ast.parse(f_string, mode="eval")
        specifier_deleter = SpecifierDeleter()
        modified_ast = specifier_deleter.visit(parsed_ast)
        body = modified_ast.body
        evaluated_content = ast.literal_eval(body)
        annotations = get_type_hints(
            specifier_deleter,
            globalns=frame.f_globals,
            localns=frame.f_locals,
        )

        return evaluated_content, annotations

    def __call__(self, /, **kwargs) -> str:
        values = {}
        for key, annotation in self.__annotations__.items():
            if key not in kwargs:
                raise ValueError(
                    f"Template uses {tuple(self.__annotations__.keys())} keys but is missing replacement '{key}'."
                )

            value = kwargs[key]
            try:
                check_type(value, annotation)
            except TypeCheckError:
                raise TypeError(
                    f"Incorrect type for replacement '{key}', expected: {annotation}."
                )
            values[key] = value

        return self.format(**values)

    def __repr__(self) -> str:
        annotations = ", ".join(
            f"{name}: {annotation}" for name, annotation in self.__annotations__.items()
        )
        return f"<{self.__class__.__name__}({annotations})>"

    def __add__(self, other: str) -> Template:
        if isinstance(other, Template):
            pass
        else:
            other = Template(other)

        annotations = self.__annotations__ | other.__annotations__
        return Template.__new__(
            Template,
            super().__add__(other),
            _annotations=annotations,
            _is_preprocessed=True,
        )

    def __mul__(self, other: Any) -> Template:
        if not isinstance(other, int):
            raise NotImplementedError

        return Template.__new__(
            Template,
            super().__mul__(other),
            _annotations=self.__annotations__,
            _is_preprocessed=True,
        )

    def __rmul__(self, other: Any) -> Template:
        return self.__mul__(other)


class FileTemplate(Template):
    def __init__(self, path: str) -> None:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File path: {path} was not found.")
        with open(path) as file:
            content = file.read()
        super().__init__(content=content)
