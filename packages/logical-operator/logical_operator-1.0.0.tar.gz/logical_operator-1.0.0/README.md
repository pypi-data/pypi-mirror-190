# logical_operator

Normalized logical operators as functions.

The ``and``, ``or``, and ``not`` operators implemented as free-standing
functions.

## Getting Started

This project is available through pip (requires Python 3.8 or later):

```
$ pip install logical_operator
```

This library contains just three functions: ``logical_and()``, ``logical_or()``, and ``logical_not()``. Each function simply converts their arguments to truth values (we call this "normalization"), and performs the built-in ``and``, ``or``, or ``not`` operation, respectively:

```python
>>> from logical_operator import logical_and
>>> logical_and(0, 0)
False
>>> logical_and(0, 1)
False
>>> logical_and(1, 1)
True
```

These functions are implemented in Python alone, and are fully typed. Type-hint inspection is supported.

Why does this library exist? There are many instances, particularly in using functions like ``map()``, where performing a logical operation over the iterables' elements is useful. Writing a ``lambda`` function for each instance of this use case can become tedious - especially if present in more than one place.

Why are these functions written in Python? The difference in time between this library and an equivalent C extension is marginal, especially when taking advantage of the faster [``not not`` conversion trick](https://www.youtube.com/watch?v=9gEX7jesV34) (which these functions utilize).

## Contributing

This project is currently maintained by [Braedyn L](https://github.com/braedynl). Feel free to report bugs or make a pull request through this repository.

## License

Distributed under the MIT license. See the [LICENSE](LICENSE) file for more details.
