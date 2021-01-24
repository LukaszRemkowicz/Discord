import psutil
from PIL import Image

from global_functions import *
from selenium.common.exceptions import NoSuchElementException
from local_variables import *

if platform.system() == 'Windows':
    from selenium.webdriver.chrome.options import Options
elif platform.system() == 'Linux':
    from selenium.webdriver.firefox.options import Options


def taking_screen_shot_meteoblue(city_name, new_folder_path, folder, driver):
    url = f'https://www.meteoblue.com/en/weather/outdoorsports/seeing/{CITIES[city_name]}'
    cpu_usage = psutil.virtual_memory().percent
    driver.get(url)
    driver.set_window_position(0, 0)
    driver.set_window_size(1500, 2000)
    try:
        driver.find_element_by_xpath('//*[@value="Accept and continue"]').click()
    except NoSuchElementException:
        pass
    """pause 1 second to let page loads"""
    time.sleep(1)
    """save screenshot and return name of it to crop"""
    screen_file_name = screenshot(driver, folder)
    file = Image.open(screen_file_name)
    final_photo = cropping_file(file, new_folder_path, METEOBLUE_CROP_PARAM, city_name)
    os.remove(screen_file_name)
    # print(f' Cpu usage: {cpu_usage}')
    return final_photo


"""For testing"""

# taking_screen_shot_meteoblue('elblag', os.path.join(SAVING_TO_DISC_TASK, 'meteo'), SAVING_TO_DISC_TASK)
