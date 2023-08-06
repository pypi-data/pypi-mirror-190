# Welcome

The library implements a simple yet, an important object that is a core component on the why I like to write software. Essentially, the library implements a list with enforce constraints. The constraints are:

1. Fix length
2. `prune_state` method that only works is the registry contains values.

The usage goes as follows:


``` python
from usecase_registry import UseCaseRegistry

registry = UseCaseRegistry[int](max_length=2) # (1)
# or registry = UseCaseRegistry[str](max_length=2)
# or registry = UseCaseRegistry[AnotherObject](max_length=2)
```

1.  The `int` typing annotation can be replaced by any other object the `UseCaseRegistry` may store. (`UseCaseRegistry[str]` or `UseCaseRegistry[WriteTransaction]`)

So... how a simple object helps me build a foundation of the way I like to write software.
The key is a ***workflow*** per ***use case***
