import datetime
import os
import time

from PIL import Image
from selenium.common.exceptions import WebDriverException


from global_functions import screenshot, cropping_file
from local_variables import CLEAROUTSITE_CROP_PARAM


def taking_screen_shot_clearoutsite(new_folder_path, folder, city_coordinates, driver, task_or_not, day=None):
    print(id(task_or_not))
    (latitude, longitude), city_name = city_coordinates
    url = f'https://clearoutside.com/forecast/{latitude}/{longitude}'

    driver.get(url)

    """testing window size"""

    # driver.set_window_position(0, 0)
    # driver.set_window_size(1500, 2000)

    day_now = datetime.datetime.now().date().strftime("%d/%m/%Y")
    day_now_obj = datetime.datetime.strptime(day_now, '%d/%m/%Y')

    """testing window size"""

    # size = driver.get_window_size()
    # print("Window size: width = {}px, height = {}px".format(size["width"], size["height"]))

    try:
        driver.find_element_by_xpath("//*[@aria-label='dismiss cookie message']").click()
        # time.sleep(2)
    except WebDriverException:
        pass

    if day:
        if isinstance(day, int) and int(day) == datetime.datetime.now().day:
            pass
        elif isinstance(day, int) and int(day) != datetime.datetime.now().day:
            searching_day_index = int(day) - day_now_obj.day

            try:
                driver.find_element_by_xpath(f"//div[@id='day_{searching_day_index}']"
                                             f"//div[@class='fc_day_date'][contains(text(),'{day}')]").click()
            except WebDriverException:
                driver.find_element_by_xpath(f"// div[contains(text(),'{day}')]").click()

            """pause 1 second to let page loads"""
            time.sleep(1)
            """save screenshot and return name of it to crop"""
            screen_file_name = screenshot(driver, folder)
            file = Image.open(screen_file_name)
            top_add = searching_day_index * 100
            bottom_add = searching_day_index * 100
            final_photo = cropping_file(file, new_folder_path, CLEAROUTSITE_CROP_PARAM,
                                        city_day=(city_name, int(day)), top_add=top_add, bottom_add=bottom_add)
            os.remove(screen_file_name)
            return final_photo
        else:

            try:
                driver.find_element_by_xpath(f"//div[@id='day_{0}']//div[@class='fc_day_date'][contains(text(),"
                                             f"'{datetime.datetime.now().day}')]").click()
            except WebDriverException:
                pass

    time.sleep(1)
    """save screenshot and return name of it to crop"""
    screen_file_name = screenshot(driver, folder)
    file = Image.open(screen_file_name)
    final_photo = cropping_file(file, new_folder_path, CLEAROUTSITE_CROP_PARAM, city_day=(city_name, day))
    os.remove(screen_file_name)
    if task_or_not:
        try:
            day_now_obj += datetime.timedelta(3)
            driver.find_element_by_xpath(f"// div[contains(text(),'{day_now_obj.day}')]").click()
        except KeyError:
            driver.find_element_by_xpath(f"//div[@id='day_{3}']//div[@class='fc_day_date'][contains(text(),"
                                         f"'{day_now_obj.day}')]").click()
    else:
        pass
    return final_photo


"""For testing"""

# (city_coordinates), country = find_city_coordinates('elblag')
# taking_screen_shot_clearoutsite('Z:\Python\Rozne_programy\Discord\saving_to_disc_task\clear\elblag',
#                                 'Z:\Python\Rozne_programy\Discord\saving_to_disc_task',
#                                 city_coordinates)
