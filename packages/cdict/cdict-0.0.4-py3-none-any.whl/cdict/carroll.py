from __future__ import annotations
from typing import Any, Sequence, Union


Params = dict[str, Any]  # should be considered immutable!


class ParamSweep(object):
    @classmethod
    def dict(cls, **kwargs: Any) -> ParamSweep:
        return cls([dict(**kwargs)])

    def __init__(self, params: Sequence[Params], /):
        params = list(params)
        if not all(isinstance(p, dict) for p in params):
            raise TypeError("Cannot initialize ParamSweep with non-dict param types.")
        self.params = [p.copy() for p in params]

    # Combining sweeps together:

    def __add__(self, other: ParamSweep) -> ParamSweep:
        return ParamSweep(self.params + other.params)

    def __mul__(self, other: ParamSweep):
        return ParamSweep({**a, **b} for a in self.params for b in other.params)

    def __or__(self, other: ParamSweep):
        if len(self.params) != len(other.params):
            raise ValueError("ParamSweeps must be the same length when zipping them together.")
        return ParamSweep({**a, **b} for a, b in zip(self.params, other.params))

    # Some basic dict/list like functions:

    def __len__(self):
        return len(self.params)

    def __getitem__(self, idx):
        return self.params[idx]

    def __iter__(self):
        return iter(self.params)

    def __str__(self) -> str:
        return str(self.params)

    def __repr__(self) -> str:
        return f"ParamSweep({self})"
