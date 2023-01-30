from typing import List, Tuple
from items.item import Item


class BaseRecipe:
    """Класс для рецептика"""
    ingredients: List[Tuple[Item, int]]
    result: Item
