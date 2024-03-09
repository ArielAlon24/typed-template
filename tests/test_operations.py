from typelate import Template


def test_add_two_templates() -> None:
    t1 = Template("name: {name: str}")
    t2 = Template(", age: {age: int}")

    template = t1 + t2

    assert template(name="Typed Template", age=1) == "name: Typed Template, age: 1"


def test_duplicate_template_with_addition() -> None:
    t1 = Template("name: {name: str} ")

    template = t1 + t1 + t1 + t1

    assert template(name="test") == "name: test name: test name: test name: test "


def test_duplicate_template_with_multiplication() -> None:
    t1 = Template("name: {name: str} ")

    template = t1 * 4

    assert template(name="test") == "name: test name: test name: test name: test "


def test_duplicate_template_with_right_multiplication() -> None:
    t1 = Template("name: {name: str} ")

    template = 4 * t1

    assert template(name="test") == "name: test name: test name: test name: test "


def test_str_count_method() -> None:
    template = Template("thiS iS a teSt for counting S")

    assert template.count("S") == 4


def test_in_operator() -> None:
    template = Template("The first 5 letters are: ABCDE")

    assert "A" in template
    assert "F" not in template
