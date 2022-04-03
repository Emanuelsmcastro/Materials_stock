from Utils.SQL import sqlite_python as sql
from Utils.connection import connection_methods as connection_m
from Utils.data_processing import data_processing as dp
from Utils.date import date
from Utils.Console.console_manager import BeautifulPrint
import keyboard

# Establishing connection
ser = connection_m.connection_serial()

# Creating database
data_base = sql.DataBase('data_base')
data_base.create_table('materials', ['bar_code TEXT NOT NULL', 'name TEXT NOT NULL', 'measure REAL NOT NULL',
                                     'total_measure REAL NOT NULL', 'price REAL NOT NULL',
                                     'expiration_date TEXT NOT NULL', 'registration_date TEXT NOT NULL'])

data_base.create_table('materials_used', ['bar_code TEXT NOT NULL', 'name TEXT NOT NULL', 'measure REAL NOT NULL',
                                          'fraction_price REAL NOT NULL', 'expiration_date',
                                          'registration_date TEXT NOT NULL'])

# Methods


def consumed_material(table_to_send, _transfer_measure):
    """
    Consume the material
    :param table_to_send: table that will receive the material;
    :param _transfer_measure: Measure that will be transfer;
    """
    material_used_measure = 0
    if _transfer_measure == 0:
        return None
    material_measure = dp.named_data(data_base, 'materials', bar_code).measure
    try:
        material_used_measure_t = dp.named_data(data_base, 'materials_used', bar_code).measure
    except AttributeError:
        pass
    else:
        material_used_measure = material_used_measure_t
    measurement_difference = material_measure - _transfer_measure
    price = dp.named_data(data_base, 'materials', bar_code).price
    total_measure = dp.named_data(data_base, 'materials', bar_code).total_measure
    formula = (price * _transfer_measure) / total_measure
    if material_measure == float(0):
        data_base.__delitem__('materials', 'bar_code', bar_code)
        return None
    if _transfer_measure > material_measure:
        print(f'Maximum transfer: {material_measure}')
        return None
    if _transfer_measure < float(0):
        if (_transfer_measure * -1) > material_used_measure:
            print(f'Maximum transfer: {material_used_measure}')
            return None
    data_base.update_value('materials', 'bar_code', bar_code, 'measure', measurement_difference)
    _materials_used = dp.named_data(data_base, 'materials_used', bar_code)
    fraction_price = formula
    if _materials_used is None:
        data_base.insert_data('materials_used', [bar_code, captured_inf.name, _transfer_measure, fraction_price,
                                                 captured_inf.expiration_date, date.get_date()])
    else:
        sum_of_measure = dp.named_data(data_base, 'materials_used', bar_code).measure + _transfer_measure
        sum_of_fraction_price = dp.named_data(data_base, 'materials_used', bar_code).fraction_price + fraction_price
        data_base.update_value(dp.string_treatment(table_to_send), 'bar_code', bar_code, 'measure', sum_of_measure)
        data_base.update_value(dp.string_treatment(table_to_send), 'bar_code', bar_code, 'fraction_price',
                               sum_of_fraction_price)


def register_material(table_name, _bar_code):
    """
    Register material;
    :param table_name: Name of table;
    :param _bar_code: Bar code to analyze.
    :return:
    """
    _material_name = dp.string_handling('Enter the material name')
    _material_measure = dp.float_treatment('Enter the material measure')
    _material_price = dp.float_treatment('Enter the material price')
    _material_expiration_date = dp.date_treatment('Enter the material expiration date')
    _total_measure = _material_measure
    if _material_name is None or _material_measure is None or _material_price is None or \
            _material_expiration_date is None:
        print('Registration canceled!')
        pass
    else:
        data_base.insert_data(dp.string_treatment(table_name), [_bar_code, _material_name, _material_measure,
                                                                _total_measure, _material_price,
                                                                _material_expiration_date, date.get_date()])
        print(f'Code |{bar_code}| registered!')


# Loop
if __name__ == '__main__':
    while True:
        bar_code = connection_m.read_serial_data(ser)
        if bar_code != '':
            named_material = dp.named_data(data_base, 'materials', bar_code)
            if named_material is None:
                register_material('materials', bar_code)
            else:
                captured_inf = dp.named_data(data_base, 'materials', bar_code)
                BeautifulPrint().print_table(captured_inf)
                transfer_measure = dp.float_treatment('Transfer measure')
                print('\n')
                if transfer_measure is not None:
                    consumed_material('materials_used', transfer_measure)
        if keyboard.is_pressed('q'):
            break
