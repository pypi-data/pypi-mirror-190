import json

from pathlib import Path
from typing import Mapping

from la_panic.panic_parser.addresses.address_symbol_mapper import AddressSymbolMapper
from la_panic.panic_parser.system.system_manager import SystemManager


class UserDefinedAddressManager(object):

    __user_input_file_path: Path
    __user_defined_map: Mapping[str, hex]

    def __init__(self, user_input_file_path: Path):
        self.__user_input_file_path = user_input_file_path

        with user_input_file_path.open("rb") as user_input_file:
            data = user_input_file.read()
            self.__user_input_file_path = json.loads(data)


class LaAddress(object):
    __user_input_address: str

    def __init__(self, address: hex):
        self.__user_input_address = address

    @property
    def unslide_address(self) -> hex:
        return SystemManager.kernel_cache_based_address(self.__user_input_address)

    @property
    def unslide_named_address(self) -> str:
        unslide_address = SystemManager.kernel_cache_based_address(self.__user_input_address)
        return AddressSymbolMapper.address_name(unslide_address).ljust(18)

    @property
    def named_address(self) -> str:
        return AddressSymbolMapper.address_name(self.__user_input_address).ljust(18)

    def __repr__(self):
        return f"{self.__user_input_address}"

    def __str__(self):
        return self.__repr__()
