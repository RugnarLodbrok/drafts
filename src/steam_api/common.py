from typing import Any

AnyDict = dict[str, Any]
_AnyJsonItem = AnyDict | bool | None
AnyJson = list[_AnyJsonItem] | _AnyJsonItem
