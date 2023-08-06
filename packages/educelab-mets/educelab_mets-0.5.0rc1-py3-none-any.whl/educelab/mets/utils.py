import datetime

from .constants import TIME_FORMAT, METS_REQUIRED_FUNCTION, NAMESPACES
from .exceptions import METSLibError


def _add_attribute_to_tree(tree, tag, attrib):
    if attrib is not None:
        tree.set(str(tag), str(attrib))
    return


def _add_namespace_attribute_to_tree(tree, qname, attrib):
    if attrib is not None:
        tree.set(qname, str(attrib))
    return


def _get_element_list(elem_list, cls, allow_none=True):
    output = []
    if elem_list is not None:
        if isinstance(elem_list, (list, tuple)):
            for item in elem_list:
                if isinstance(item, cls):
                    output.append(item)
                else:
                    raise METSLibError('Input type incorrect')
        elif isinstance(elem_list, cls):
            output.append(elem_list)
        else:
            raise METSLibError('Input type incorrect')
    else:
        if not allow_none:
            raise METSLibError('Value cannot be empty')
    return output


def _add_enum_value(value, enum, allow_none=True):
    if value is not None:
        value = str(value)
        if enum.has_value(value):
            return value
        else:
            raise ValueError(
                'Value is not one of the possible options.')  # TODO print out allowed values
    elif not allow_none:
        raise ValueError('Value cannot be None')
    else:
        return None


def _add_mets_class(obj, expected_cls, allow_none=True, duck_type=True):
    if obj is not None:
        if isinstance(obj, expected_cls):
            return obj
        else:
            if duck_type:
                if hasattr(obj, METS_REQUIRED_FUNCTION):
                    return obj
                else:
                    raise TypeError(
                        'Input type incorrect. Instance has to implement function ' +
                        METS_REQUIRED_FUNCTION)
            else:
                raise TypeError('Input type incorrect.')
    elif not allow_none:
        raise ValueError('Value cannot be None')
    else:
        return None


def _get_integer_value(value, allow_none=True):
    if value is not None:
        try:
            return int(value)
        except:
            raise ValueError('Parameter requires an integer value')
    elif not allow_none:
        raise ValueError('Value cannot be None')
    else:
        return None


def _get_string_value(value, allow_none=True):
    if value is not None:
        try:
            return str(value)
        except:
            raise ValueError('Parameter requires a string value')
    elif not allow_none:
        raise ValueError('Value cannot be None')
    else:
        return None


def _get_datetime_value(value, allow_none=True):
    if value is not None:
        if type(value) in (datetime.date, datetime.datetime, datetime.time):
            # return value.strftime(TIME_FORMAT)
            return value.isoformat()
        else:
            try:
                datetime.datetime.fromisoformat(value)
                return value
            except ValueError:
                try:
                    datetime.datetime.strptime(value, TIME_FORMAT)
                except ValueError:
                    raise ValueError(
                        "Incorrect date time input. Required format is YYYY-MM-DDThh:mm:ss.mmmm")
                    # raise ValueError("Incorrect date time input. ISO 8601 format is required.")
    elif not allow_none:
        raise ValueError('Value cannot be None')
    else:
        return None


def _check_tag(tag: str, expected: str, ns: str = NAMESPACES['mets']) -> bool:
    if tag == expected or tag == '{' + ns + '}' + expected:
        return True
    else:
        return False
