import pickle
from entities.json_parser import json_dict_into_object, register_json
from items.item import Item


@register_json
class Inventory:
    def __init__(self, slots_count: int = 10) -> None:
        self.slots = slots_count
        self.grid = [None for _ in range(self.slots)]

    def save(self):
        with open('inventory.inv', 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load():
        try:
            with open('inventory.inv', 'rb') as f:
                return pickle.load(f)
        except Exception:
            return Inventory()

    def add_item(self, item: Item) -> Item:
        """
        Добавляет предмет в инвентарь. Возвращает None,
        если поместилось все количество,
        иначе возвращает оставшиеся предметы.
        """
        for slot, item_in_inv in enumerate(self.grid):
            if type(item) is type(item_in_inv):
                fill_amount = min(item_in_inv.get_max_amount() -
                                  item_in_inv.amount, item.amount)
                item_in_inv.amount += fill_amount
                item.amount -= fill_amount

                if item.amount <= 0:
                    break
            elif item_in_inv is None:
                self.grid[slot] = item
                break
        else:
            return item

        return None

    def set_slot(self, item: Item | None, index: int):
        self.grid[index] = item

    def get_slot(self, index: int) -> Item | None:
        return self.grid[index]

    def swap_slot(self, slot_index: int, item: Item | None) -> Item | None:
        previous_item = self.get_slot(slot_index)
        self.set_slot(item, slot_index)
        return previous_item

    def to_json(self) -> dict:
        return {'type': self.__class__.__name__, 'slots_count': self.slots, 'slots': [el.to_json() for el in self.grid if not el is None]}

    @classmethod
    def from_json(cls, json_dict: dict) -> "Inventory":
        new_inv = cls(json_dict['slots_count'])

        for item in json_dict['slots']:
            new_inv.add_item(json_dict_into_object(item))

        return new_inv
