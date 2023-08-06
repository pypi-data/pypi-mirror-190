from __future__ import annotations
from types import SimpleNamespace as SN
from typing import Any, Iterable, Tuple, Union, Optional


class SimpleNamespace(SN):

    def __init__(self, **kwargs) -> None:
        data = {}
        for k, v in kwargs.items():
            if not isinstance(k, str):
                continue
            if isinstance(v, dict):
                v = SimpleNamespace(**v)
            if isinstance(v, list):
                rl = []
                for lv in v:
                    if isinstance(lv, dict):
                        rl.append(SimpleNamespace(**lv))
                    else:
                        rl.append(lv)
                v = rl
            if isinstance(v, str):
                if any((v=='True', v=='False')):
                    v = v=='True'
            data.update({k: v})
        super().__init__(**data)

    def __iter__(self) -> Iterable[str]:
        for k in self.__dict__:
            if not k.startswith('_'):
                yield k

    def __len__(self) -> int:
        return len(list(self.__iter__()))

    def __bool__(self) -> bool:
        return self.__len__() != 0

    def __class_getitem__(cls, key) -> Any:
        ...

    def __getattribute__(self, __name: str) -> Union[SimpleNamespace, Any]:
        return object.__getattribute__(self, __name)

    def __getattr__(self, __name:str) -> Any:
        return SimpleNamespace()

    def __getitem__(self, key:Union[str, int, slice]) -> Optional[Any]:
        if isinstance(key, str):
            return getattr(self, key, None)
        return None

    def items(self) -> Iterable[Tuple[str, Union[SimpleNamespace, Any]]]:
        for k in self:
            yield k, self.__dict__[k]

    @property
    def as_dict(self) -> dict:
        d = {}
        for k,v in self.items():
            if isinstance(v, SimpleNamespace):
                v = v.as_dict
            d.update({k:v})
        return d