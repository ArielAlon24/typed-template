from src import Template
from datetime import datetime


class Header:
    def __init__(self, name):
        self.name = name

    def __str__(self) -> str:
        return f"-=- {self.name} -=-"


html = """{heading: Header}

This is a test, here's today's date: {date: datetime},
A template can (would) even utilize python's format options!
And this is pi: {pi: float}.
"""


t = Template(html)

print(t.format(heading=Header(name="this"), date=datetime.now(), pi=3.14))
