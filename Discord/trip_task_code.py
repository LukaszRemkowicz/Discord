from discord_clearousite_screenshots import *
from discord_meteoblue_screenshots import *
from global_functions import *
from local_variables import *


def taking_screenshot_with_task_before_trip_function(cities, driver):
    task_or_not = True
    day_list = datetime_list()
    preparing_empty_folder(FILES_PATH_TRIP)
    os.mkdir(os.path.join(os.path.join(FILES_PATH_TRIP, 'meteo')))
    new_folder_path_meteo = os.path.join(FILES_PATH_TRIP, 'meteo', '')
    for city in cities:
        taking_screen_shot_meteoblue(city, new_folder_path_meteo, FILES_PATH_TRIP, driver)
    os.mkdir(os.path.join(os.path.join(FILES_PATH_TRIP, 'clear')))
    new_folder_path = os.path.join(FILES_PATH_TRIP, 'clear', '')
    for city in cities:
        os.mkdir(os.path.join(new_folder_path, city))
        new_city_folder_path = os.path.join(new_folder_path, city, '')
        try:
            if COORDS_CACHE[city]:
                (city_coordinates), country = COORDS_CACHE[city]
        except KeyError:
            (city_coordinates), country = find_city_coordinates(city)
        taking_screen_shot_clearoutsite(new_city_folder_path, FILES_PATH_TRIP, city_coordinates, driver, task_or_not)
        for day_in_list in day_list:
            taking_screen_shot_clearoutsite(new_city_folder_path, FILES_PATH_TRIP, city_coordinates, driver,
                                            task_or_not, day_in_list)
        taking_screen_shot_clearoutsite(new_city_folder_path, FILES_PATH_TRIP, city_coordinates, driver,
                                        task_or_not, 'all')


"""For testing"""

# taking_screenshot_with_task_before_trip_function([ 'lapszanka', 'lutowiska', 'steznica', 'zakopane'])
