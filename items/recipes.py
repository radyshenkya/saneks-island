from typing import Dict, List, Tuple
from items.item import Item


class Recipe:
    """Класс для рецептика"""

    def __init__(self, name: str, ingredients: Dict[Item, int], result: Dict[Item, int]) -> None:
        self.ingredients = ingredients
        self.result = result
        self.name = name

    def is_enough_ingredients(self, ingredients: List[Item]) -> Tuple[bool, Item | None, int | None]:
        """Хватает ли ингредиентов для крафта

        Если да - возвращает (True, None, None)

        Если нет - (False, КЛАСС_АЙТЕМА_КОТОРОГО_НЕ_ХВАТАЕТ, НУЖНОЕ_КОЛВО_ЭТОГО_АЙТЕМА)"""
        for needed_ingred, amount in self.ingredients.items():
            current_amount = 0

            for ingred in ingredients:
                if isinstance(ingred, needed_ingred):
                    current_amount += ingred.amount

            if current_amount < amount:
                return (False, needed_ingred, amount)

        return (True, None, None)

    def craft(self, ingredients: List[Item]) -> Tuple[List[Item], List[Item]]:
        """Создает предметы, возвращает результат крафта и то, что осталось от ингредиентов

        ОН НЕ СМОТРИТ НА КОЛ-ВО ПРЕДМЕТОВ, ПЕРЕД ИСПОЛЬЗОВАНИЕМ ЛУЧШЕ ВЫЗВАТЬ `self.is_enough_ingredients()`"""

        result = [item(amount) for item, amount in self.result.items()]

        for needed_ingred, amount in self.ingredients.items():
            current_amount = 0

            for ingred in ingredients:
                if isinstance(ingred, needed_ingred):
                    destroyed_amount = min(
                        amount - current_amount, ingred.amount)
                    ingred.amount -= destroyed_amount
                    current_amount += amount

        return (result, ingredients)
