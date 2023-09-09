from os import listdir
from os.path import dirname, isfile, join
from types import MappingProxyType

directory = dirname(__file__)

available_configs = MappingProxyType(
    {
        file[:-5]: join(directory, file)
        for file in listdir(directory)
        if isfile(join(directory, file)) and file.endswith('.toml')
        }
    )

del listdir, dirname, isfile, join, MappingProxyType, directory
__all__ = 'available_configs',
