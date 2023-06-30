from collections.abc import Mapping
from types import MappingProxyType

from . import keys, localizations

available_keys: Mapping[str, keys.Key] = MappingProxyType(
    {
        attr.lower(): v
        for attr in dir(keys)
        if isinstance(v := getattr(keys, attr), keys.Key)
        }
    )

available_localizations: Mapping[str, localizations.Localization] = MappingProxyType(
    {
        attr.lower(): v
        for attr in dir(localizations)
        if isinstance(v := getattr(localizations, attr), localizations.Localization)
        }
    )

__all__ = 'available_keys', 'available_localizations'
