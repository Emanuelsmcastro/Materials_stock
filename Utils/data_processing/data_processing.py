from collections import namedtuple
import re


def named_data(database, table_name, barcode):
    """
    The function will return the data, using namedtuple, found with a given barcode
    :param database: Connection with database;
    :param table_name: Table name;
    :param barcode: Barcode to be used to search in table;
    :return: Return named information.
    """
    data = database.table_columns([table_name])
    data_columns = data[0][1]
    data_name = data[0][0]
    columns = ' '.join(data_columns)
    named_struct = namedtuple(f'{data_name}', f'{columns}')
    _material = database.locator(table_name, 'bar_code', barcode)
    if _material is not None:
        return named_struct._make(_material)
    else:
        return None


def string_handling(text):
    """
    This function will treat a string;
    :param text: Text to be show;
    :return: Return string treated.
    """
    n = input(f'{text}: ')
    n_strip = n.strip().lower()
    if len(n_strip) == 0:
        return None
    return n_strip


def date_treatment(text):
    """
    This function will treat a string and convert it to date format
    :param text: Text to be show;
    :return: Return date formatted
    """
    n = input(f'{text}: ')
    regex = re.compile(r'([0-9]{2}/)?([0-9]{2}/)([0-9]{4})')
    validator = regex.match(n)
    if validator is not None:
        return validator.group()
    return None


def float_treatment(text):
    """
    This function will treat a string and convert it to float;
    :param text: Text to be show;
    :return: Return float treated.
    """
    n = string_handling(text)
    if n is not None:
        try:
            number = float(n)
        except ValueError:
            return None
        else:
            return number


def string_treatment(string):
    try:
        string_to_return = str(string)
    except ValueError or TypeError:
        return None
    else:
        return string_to_return
