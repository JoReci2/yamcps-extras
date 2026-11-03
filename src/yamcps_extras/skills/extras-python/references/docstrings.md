# Docstrings publiques

Documenter toutes les fonctions et méthodes publiques avec des docstrings en
anglais au format Google, avec `Args`, `Returns` et `Raises` lorsque pertinents.
Inclure des exemples d’utilisation lorsqu’ils clarifient le comportement.

```python
def example_function(param1: str, param2: int) -> bool:
    """Check whether text meets a minimum length.

    Args:
        param1: Text to check.
        param2: Minimum accepted length.

    Returns:
        Whether the text meets the minimum length.

    Raises:
        ValueError: If the minimum length is negative.

    Examples:
        >>> example_function("yamcps", 3)
        True
    """
    if param2 < 0:
        raise ValueError("Minimum length must be nonnegative")
    return len(param1) >= param2
```

