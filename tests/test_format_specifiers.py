from src import Template
import math

# typelate


def test_float_round() -> None:
    template = Template("Pi is {pi: float: .2f}")

    assert template.format(pi=math.pi) == "Pi is 3.14"


def test_int_base() -> None:
    template = Template("Binary of 10 is {num: int: b}")
    assert template.format(num=10) == "Binary of 10 is 1010"


def test_str_spacing() -> None:
    template = Template("Hello {name: str: >10}")
    assert template.format(name="World") == "Hello      World"


def test_local_specifier() -> None:
    class A:
        def __init__(self, content: str) -> None:
            self.content = content

        def __format__(self, format_spec: str) -> str:
            if format_spec == "rev":
                return self.content[::-1]

            return super().__format__(format_spec)

    template = Template("A's content reversed: {a: A: rev}")
    assert (
        template.format(a=A("TypedTemplate")) == "A's content reversed: etalpmeTdepyT"
    )
