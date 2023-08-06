import json
from operator import itemgetter
from pathlib import Path
from typing import Mapping


class AddressSymbolMapper(object):
    __map: Mapping[str, str] = {}

    @staticmethod
    def parse(address_symbols_file_path: Path):
        if not address_symbols_file_path.exists():
            return

        building_map = {}
        with address_symbols_file_path.open("r") as address_symbols_file:
            for line in address_symbols_file.readlines():
                json_data = line.split("=")
                building_map[json_data[1].split(";")[0]] = json_data[0].strip()

        AddressSymbolMapper.__map = {key: building_map[key] for key in sorted(building_map)}

    @staticmethod
    def address_name(address: hex) -> str:
        try:
            return AddressSymbolMapper.__map[address]
        except KeyError:
            # for saved_address, name in AddressSymbolMapper.__map.items():
            #     if int(saved_address, 16) > int(address, 16):
            #         return name
            return address
