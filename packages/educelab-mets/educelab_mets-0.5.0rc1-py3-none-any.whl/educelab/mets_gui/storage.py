# provides a method for storing and managing ID values for the whole mets document
from PySide6.QtCore import Qt

from educelab.mets_gui import constants

_id_list = {}  # stores ID together with the type of the element


# checks whether an id value exists and if not, adds it to storage
def add_id(value: str, element_type: str) -> bool:
    if value:
        if value in _id_list.keys():
            return False
        else:
            _id_list[value] = element_type
        return True
    else:
        return True


# changes id value into new one if it doesnt exist
def change_id(old_id: str, new_id: str) -> bool:
    if new_id:
        if new_id in _id_list.keys():
            return False
        else:
            _id_list[new_id] = _id_list[old_id]
            del _id_list[old_id]
            return True
    else:
        remove_id(old_id)
        return True


# removes id value from storage
def remove_id(id_value: str) -> None:
    if id_value:
        _id_list.pop(id_value)
    return


# removes id value of a list item from storage
def remove_list_item_id(item) -> None:
    remove_id(item.data(Qt.ItemDataRole.UserRole)[constants.Attributes.ID.name])
    return


# removes id value of a tree item from storage
def remove_tree_item_id(item) -> None:
    for i in range(item.rowCount()):
        remove_tree_item_id(item.child(i))
    remove_id(item.data(Qt.ItemDataRole.UserRole)[constants.Attributes.ID.name])
    return


# gets all ids of a specific element type from storage
# TODO: create an autofinish list for attributes that reference IDs in dialogs
def get_type_ids(element_type: str) -> dict:
    return {key: value for key, value in _id_list.items() if
            value == element_type}
