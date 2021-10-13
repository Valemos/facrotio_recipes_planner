import pyperclip

obj_name = pyperclip.paste()

result = f"""
class {obj_name}List(list, AContainerJsonSerializable):
    __element_type__ = {obj_name}
"""

pyperclip.copy(result)
