import pickle
from items.item import Item


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
