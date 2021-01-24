import json
import xlrd
from local_variables import *


def writing_dict_from_xml_to_file():
    loc = LOCATION_OF_CITY_BASE
    """opening .xls file"""
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    city_dict = {}
    """creating new dictionary with {city_name:coordinate values}"""
    for row in range(0, sheet.nrows):
        city_dict[sheet.cell_value(row, 0).lower()] = (sheet.cell_value(row, 1), sheet.cell_value(row, 2))
    with open(CITY_DICT_FILE, 'r+') as file:
        file.write(json.dumps(city_dict))


def finding_coordinates(city):
    with open(CITY_DICT_FILE, 'r') as file:
        city_dict = json.loads(file.read())
    return city_dict[city]


"""For testing"""

# if __name__=='__main__':
#     writing_dict_from_xml_to_file()
#     print(finding_coordinates('elblag'))
