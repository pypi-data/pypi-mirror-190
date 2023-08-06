from __future__ import annotations
from typing import Any, Union, Iterable, Optional, List
import itertools

class cdict():
    @classmethod
    def dict(cls, **kwargs: Any) -> cdict:
        return cls(_add_items=[dict(**kwargs)])

    @classmethod
    def list(cls, *args: Any) -> cdict:
        return cls.iter(list(args))

    @classmethod
    def iter(cls, it: Any) -> cdict:
        return cls(_add_items=it)

    def __init__(self, _add_items: Optional[Iterable]=None, _mul_items: Optional[List[cdict]]=None, _or_items: Optional[List[cdict]]=None) -> cdict:
        assert _add_items is None or _mul_items is None
        if _mul_items is not None:
            assert _add_items is None
            assert _or_items is None
            self._type = "mul"
            for c in _mul_items:
                assert isinstance(c, cdict), "Cannot multiply"
            self._mul_items = _mul_items
        elif _add_items is not None:
            assert _or_items is None
            self._type = "add"
            self._add_items = _add_items
        else:
            assert _or_items is not None
            self._type = "or"
            self._or_items = _or_items

    def __iter__(self):
        if self._type == "add":
            for d in iter(self._add_items):
                if isinstance(d, cdict):
                    yield from d
                elif isinstance(d, dict):
                    # if values of dict are cdicts, need to combinatorially yield
                    ks = list(d.keys())
                    viters = []
                    for k in ks:
                        v = d[k]
                        if isinstance(v, cdict):
                            viters.append(iter(v))
                        else:
                            viters.append([v])
                    for vs in itertools.product(*viters):
                        yield {k: v for k, v in zip(ks, vs)}
                else:
                    yield d
        elif self._type == "mul":
            for ds in itertools.product(*self._mul_items):
                yield dict(sum((list(d.items()) for d in ds), []))
        elif self._type == "or":
            for items in zip(*self._or_items):
                res = dict()
                for d in items:
                    res.update(d)
                yield res
        else:
            raise ValueError(f"Unknown type {self._type}")

    def __add__(self, other) -> cdict:
        return cdict(_add_items=[self, other])

    def __mul__(self, other) -> cdict:
        return cdict(_mul_items=[self, other])

    def __or__(self, other) -> cdict:
        return cdict(_or_items=[self, other])

    def __repr_helper__(self) -> str:
        if self._type == "add":
            if isinstance(self._add_items, list):
                return " + ".join([str(d) for d in self._add_items])
            else:
                return "sum(" + str(self._add_items) + ")"
        else:
            assert self._type == "mul"
            return " * ".join([d.__repr_helper__() for d in self._mul_items])

    def __repr__(self) -> str:
        return f"cdict({self.__repr_helper__()})"

    def __len__(self) -> int:
        return len(list(iter(self)))
