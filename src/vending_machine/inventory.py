import dataclasses
import json
import os
from dotenv import load_dotenv
from dacite import from_dict

load_dotenv()

INVENTORY_FILE = "./inventory.json"


@dataclasses.dataclass
class InventoryItem:
    box: int
    weight: float


@dataclasses.dataclass
class Inventory:
    stock: dict[str, InventoryItem]


def load_inventory() -> Inventory:
    with open(os.path.join(os.getcwd(), INVENTORY_FILE), 'rt') as json_file:
        inventory_json = json.load(json_file)
        inventory = from_dict(data_class=Inventory, data=inventory_json)

        return inventory


