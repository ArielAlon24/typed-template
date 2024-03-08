from src import Template
import math

template = Template("Pi is {pi: float : test}")

print(template.format(pi=math.pi))
