from pyperclip import copy, paste

table = paste()

result_copy = ""
for line in table.split('\n'):
    parts = line.strip().split(" ")
    name = parts[0]
    t = parts[-1].strip()
    t = t.replace("Object", "dict")
    t = t.replace("Array", "list")
    t = t.replace("String", "str")
    t = t.replace("Boolean", "bool")
    t = t.replace("Integer", "int")
    t = t.replace("uint", "int")

    result_copy += f'{name}: {t} = None\n'

copy(result_copy)
