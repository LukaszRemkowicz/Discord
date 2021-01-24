import platform

import numpy

"""Discord channels"""

CHANNELS = dict()

"""system variables"""

"""Please put your main path here:  """

MAIN_PATH_WINDOWS = ''
LINUX_MAIN_PATH = r''

if platform.system() == 'Windows':
    SAT_FOLDER = f'{MAIN_PATH_WINDOWS}\sat24'
    LOG_FILE = rf'{MAIN_PATH_WINDOWS}\Log\geckodriver.log'
    LOCATION_OF_CITY_BASE = rf'{MAIN_PATH_WINDOWS}\city_base.xlsx'
    CITY_DICT_FILE = rf'{MAIN_PATH_WINDOWS}\city_base_dictionary.txt'
    FILES_PATH = rf'{MAIN_PATH_WINDOWS}\Meteoblue_Files\\'
    EXEC_PATH = rf'{MAIN_PATH_WINDOWS}\chromedriver_win32\chromedriver.exe'
    FILES_PATH_CLEAR = rf'{MAIN_PATH_WINDOWS}\Clearoutsite_Files\\'
    FILES_PATH_METEPL = rf'{MAIN_PATH_WINDOWS}\Meteopl\\'
    FILES_PATH_TRIP = rf'{MAIN_PATH_WINDOWS}\trip\\'
    SAVING_TO_DISC_TASK = rf'{MAIN_PATH_WINDOWS}\saving_to_disc_task\\'
    BIN_FILE_WIT_MATRIX = ""
    MOON = rf'{MAIN_PATH_WINDOWS}\moon\\'

elif platform.system() == 'Linux':
    MOON = rf'{LINUX_MAIN_PATH}/moon'
    SAT_FOLDER = f'{LINUX_MAIN_PATH}/sat24'
    LOG_FILE = f'{LINUX_MAIN_PATH}/Log/geckodriver.log'
    LOCATION_OF_CITY_BASE = rf'{LINUX_MAIN_PATH}/city_base.xlsx'
    CITY_DICT_FILE = rf'{LINUX_MAIN_PATH}/city_base_dictionary.txt'
    FILES_PATH = rf'{LINUX_MAIN_PATH}/Meteoblue_Files/'
    EXEC_PATH = '/home/ubuntu/Desktop/rozne_programy/geckodriver'
    FILES_PATH_CLEAR = rf'{LINUX_MAIN_PATH}/Clearoutsite_Files/'
    FILES_PATH_METEPL = rf'{LINUX_MAIN_PATH}/Meteopl/'
    FILES_PATH_TRIP = rf'{LINUX_MAIN_PATH}/trip/'
    SAVING_TO_DISC_TASK = rf'{LINUX_MAIN_PATH}/saving_to_disc_task/'
    BIN_FILE_WIT_MATRIX = rf'{LINUX_MAIN_PATH}'


"""Um variables"""

DECIMAL_PARAMETER_FOR_FORMATTING = '2'
MATRIX = numpy.fromfile(BIN_FILE_WIT_MATRIX)
MATRIX_RESHAPE = numpy.reshape(MATRIX, (616, 448, 2))
METEO_BASE_PHOTO = 'http://www.meteo.pl/um/metco/leg_um_pl_cbase_256.png'

"""the base of Cities to daily/ on wish generate"""

CITIES = dict()
TRIP_CITIES = []
DAYLY_CITIES = []

"""Answers"""

WRONG_VALUE = []
ANSWER_DICT = {}

"""Driver variables"""

CHROME_DRIVER_OPTIONS = ["--headless", "--window-size=1500x2000", "--hide-scrollbars"]

COUNTRIES_FOR_SEARCH = []

CALENDER = {'1': 'styczen', '2': 'luty', '3': 'marzec', '4': 'kwiecien', '5': 'maj', '6': 'czerwiec',
            '7': 'lipiec', '8': 'sierpien', '9': 'wrzesien', '10': 'pazdziernik', '11': 'listopad', '12': 'grudzien'}

"""Cropping parameters"""

METEOBLUE_CROP_PARAM = (200, 400, 2000, 2200)
CLEAROUTSITE_CROP_PARAM = (170, 250, 1350, 1450)
UM_CROP_PARAM = (0, 0, 820, 660)

"""Cache variable"""

COORDS_CACHE = dict()

