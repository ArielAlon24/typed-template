from src import Template
from datetime import datetime


class Header:
    def __init__(self, name):
        self.name = name

    def __str__(self) -> str:
        return f"-=- {self.name} -=-"


data1 = """{heading: Header}

This is a test, here's today's date: {date: datetime},
A template can (would) even utilize python's format options!
And this is pi: {pi: float}.
"""

data2 = "\n this is a continuation {number: int}"


t1 = Template(data1)
t2 = Template(data2)

print(t1)

print(t1.format(heading=Header(name="this"), date=datetime.now(), pi=3.14))
