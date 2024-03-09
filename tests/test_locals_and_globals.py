from typelate import Template
import pytest


class GlobalA:
    def __str__(self) -> str:
        return "global"


def test_correct_global_class_type_entry() -> None:
    template = Template("This is of type GlobalA: {a: GlobalA}")
    assert template(a=GlobalA()) == "This is of type GlobalA: global"


def test_wrong_global_class_type_entry() -> None:
    template = Template("This is of type GlobalA: {a: GlobalA}")
    with pytest.raises(TypeError):
        template(a=123)


def test_correct_local_class_type_entry() -> None:
    class LocalA:
        def __str__(self) -> str:
            return "local"

    template = Template("This is of type LocalA: {a: LocalA}")
    assert template(a=LocalA()) == "This is of type LocalA: local"


def test_wrong_local_class_type_entry() -> None:
    class LocalA:
        def __str__(self) -> str:
            return "local"

    template = Template("This is of type LocalA: {a: LocalA}")
    with pytest.raises(TypeError):
        template(a=123)
