import os
import shutil
from datetime import time
import time

from dateutil.rrule import rrule, DAILY
from geopy import Nominatim
import http.client
import socket

from selenium import webdriver
from selenium.webdriver.remote.command import Command
from testing_speed_time import *
from local_variables import *
if platform.system() == 'Windows':
    from selenium.webdriver.chrome.options import Options
elif platform.system() == 'Linux':
    from selenium.webdriver.firefox.options import Options


def start_driver():
    chrome_options = Options()
    for option in CHROME_DRIVER_OPTIONS:
        chrome_options.add_argument(option)

    if platform.system() == 'Windows':
        driver = webdriver.Chrome(EXEC_PATH, options=chrome_options, service_log_path=LOG_FILE)
    elif platform.system() == 'Linux':
        driver = webdriver.Firefox(options=chrome_options, log_path=LOG_FILE)
    return driver


def get_status(driver):
    try:
        driver.execute(Command.STATUS)
        return "Alive"
    except (socket.error, http.client.CannotSendRequest):
        return "Dead"


def new_names(folder):
    name_of_file = time.asctime().replace(':', "-")
    file_name = folder + name_of_file + '.png'
    return file_name


def screenshot(d, folder):
    new_name = new_names(folder)
    d.save_screenshot(new_name)
    return new_name


def creating_empty_folder(files_path, name=None):
    now = datetime.datetime.now()
    name_of_folder = now.strftime("%m_%d_%Y_%Hh%Mm")  # %Ss
    if not os.path.exists(rf'{files_path}' + name_of_folder):
        os.mkdir(rf'{files_path}' + name_of_folder)
    folder_path = os.path.join(files_path, name_of_folder, '')
    if name:
        if not os.path.exists(folder_path + name):
            os.mkdir(folder_path + name)
        folder_path += os.path.join(name, '')
        return folder_path
    return folder_path


def preparing_empty_folder(file_path):
    for root, dirs, files in os.walk(file_path):
        for file in files:
            os.unlink(os.path.join(root, file))
        for directory in dirs:
            shutil.rmtree(os.path.join(root, directory))


# preparing_empty_folder(SAVING_TO_DISC_TASK)


def find_city_coordinates(city):
    """This commented code is a alternative, if you dont have any API, which returns long/lat.
    THe file is saved as a txt with json inside (generated from excel file)
    Before implemating remeber to load json outsite function (in local variables)"""
    # with open(CITY_DICT_FILE, 'r') as file:
    #     dict = json.loads(file.read())
    # return dict[city], city
    geolocator = Nominatim(user_agent="lukas")
    location = geolocator.geocode(city)
    if not location:
        return (None, None), None
    else:
        coord_list = [location.latitude, location.longitude]
        country = (''.join(location.raw['display_name'].split(',')[-1]))[1::]
        try:
            if COORDS_CACHE[city]:
                pass
        except KeyError:
            COORDS_CACHE[city] = (coord_list, city), country
        return (coord_list, city), country


"""" just for testing """


# city_coordinates= find_city_coordinates('gdansk')
# print(find_city_coordinates('gdansk'))
# print('')

def cropping_file(file, new_folder_path, param_to_crop, city=None, city_day=None, top_add=0, bottom_add=0):
    left, top, right, bottom = param_to_crop
    image_crop = file.crop((left, top + top_add, right, bottom + bottom_add))
    if city:
        file_name = os.path.join(new_folder_path, city + '.png')
        image_crop.save(file_name, quality=95)
        return file_name
    else:
        city, day = city_day
        if not city_day or not day:
            file_name = os.path.join(new_folder_path, 'Today' + '.png')
        elif day == 'all':
            file_name = os.path.join(new_folder_path, 'all' + '.png')
        else:
            day_parameter = 'st' if int(day) == 1 else 'nd' if int(day) == 2 else 'th'
            file_name = os.path.join(new_folder_path, str(day) + day_parameter + '.png')
        image_crop.save(file_name, quality=95)
        return file_name


def weather_from_disc(name, path, what_service, day=None):
    if what_service == 'clear':
        if day:
            day_parameter = ('st' if int(day) == 1 else 'nd' if int(day) == 2 else 'th') if str(day).isdigit() else ''
            file_path = os.path.join(path, what_service, name, str(day) + day_parameter + '.png')
            time_created = time.ctime(os.path.getmtime(file_path))
        else:
            file_path = os.path.join(path, what_service, name, 'today.png')
            time_created = time.ctime(os.path.getmtime(file_path))
        return file_path, time_created
    elif what_service == 'meteo':
        file_path_to_generate = os.path.join(path, what_service, name + '.png')
        time_created = time.ctime(os.path.getmtime(file_path_to_generate))
        return file_path_to_generate, time_created
    elif what_service == 'moon':
        file_path_to_generate = os.path.join(path, name + str(datetime.datetime.now().year) + '.png')
        return file_path_to_generate


def clearing_cahe(cahe):
    global COORDS_CACHE
    new_cahe = {}
    if len(cahe) >= 100:
        for number, (key, valu) in enumerate(cahe.items()):
            if 100 >= number + 1 >= 70:
                new_cahe[key] = valu
        COORDS_CACHE = new_cahe


def datetime_list():
    start_day = datetime.datetime.now()
    end_day = datetime.datetime.now() + datetime.timedelta(6)
    day_list = [int(dt.strftime("%Y-%m-%d")[-2::]) for dt in rrule(DAILY, dtstart=start_day, until=end_day)]
    return day_list
