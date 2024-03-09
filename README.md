# typelate

Python templates with type annotations and validation.

## Background

A somewhat hidden feature in Python is the ability to create `str` templates, they are similar to f-strings but they don't require you to know the values in advance.

```python
template = "Hello, {name}!"
```

Using it is as simple as calling the `format` function

```pycon
>>> template.format(name="World")
"Hello, World!"
```

```pycon
>>> template.format(name=123)
"Hello, 123!"
```

In addition to that, like f-strings we can specify a _format specifier_ to each argument.

```python
template = "Pi is {pi: .2f}"
```

```pycon
>>> import math
>>> template.format(pi=math.pi)
"Pi is 3.14"
```

## Usage

With `typelate` this behavior is extended even more, now you can specify types for each argument in the template, in runtime a template formatting will have validation that can be handled as you wish!

```python
from typed_template import Template

template = Template("Hello, {name: str}!")
```

Notice that `Template` uses the `__call__` instead of `format`

```pycon
>>> template(name="World")
"Hello, World!"
```

Now, let's pass an invalid type.

```pycon
>>> template(name=123)
TypeError: Incorrect type for replacement 'name', expected: <class 'str'>.
```

Moreover, you can use the default format specifiers in addition to the type annotation:

```python
from typed_template import Template

template = Template("Pi is {pi: float: .2f}")
```

```pycon
>>> import math
>>> template(pi=math.pi)
"Pi is 3.14"
```
