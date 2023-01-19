import dataclasses
from typing import List, Tuple
from items import Item


@dataclasses
class BaseRecipe:
    """Класс для рецептика"""
    ingredients: List[Tuple[Item, int]]
    result: Item
