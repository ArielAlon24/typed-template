from src import Template
import pytest


def test_one_correct_entry() -> None:
    template = Template("Hello {name: str}!")

    assert template(name="Python") == "Hello Python!"
    assert template(name="typed-template") == "Hello typed-template!"


def test_one_wrong_entry() -> None:
    template = Template("Hello {name: str}!")

    with pytest.raises(TypeError):
        template(name=123)
    with pytest.raises(TypeError):
        template(name=["Python"])


def test_multiple_correct_entries() -> None:
    template = Template(
        "This is a string: {string: str}, and this is a number: {number: int}."
    )

    assert (
        template(string="test", number=123)
        == "This is a string: test, and this is a number: 123."
    )


def test_multiple_correct_entries_and_one_wrong() -> None:
    template = Template("{a: int} {b: str} {c: bool}")

    with pytest.raises(TypeError):
        template(a=1, b=2, c=True)


def test_multiple_occurences_of_a_replacement() -> None:
    template = Template("{a: int} and {a: int}")

    assert template(a=1) == "1 and 1"
