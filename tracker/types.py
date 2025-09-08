from typing import List, Mapping, Union

Primitive = Union[str, int, float, bool, None]
JSONFields = Union[Primitive, List["JSONFields"], Mapping[str, "JSONFields"]]
Tags = Mapping[str, Primitive]
Contexts = Mapping[str, Mapping[str, JSONFields]]
