

class BeautifulPrint:
    @staticmethod
    def printer(word):
        return print(word)

    @staticmethod
    def print_table(named_inf):
        table_struct = '-=' * 33 + '\n' + f'Barcode: {named_inf.bar_code:<20}Name: ' \
                                          f'{named_inf.name:<20}Price: {named_inf.price}' \
                                          f'\nMeasure: {named_inf.measure:<20}Total measure: {named_inf.total_measure}'
        return print(table_struct)
