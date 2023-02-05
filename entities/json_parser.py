registered_classes = {}


def register_json(original_class):
    registered_classes[original_class.__name__] = original_class

    return original_class


def json_dict_into_object(json_dict: dict):
    obj_type_name = json_dict['type']

    return registered_classes[obj_type_name].from_json(json_dict)


"""Каждый из зарегистрированных типов должен иметь 2 метода по типу:

```python
def to_json(self) -> dict:
        pass

@classmethod
def from_json(cls, json_dict: dict) -> "CLASS_NAME":
    pass
```
"""
