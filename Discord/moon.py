from PIL import Image
from global_functions import *

crop_param = (350, 100, 850, 780)
miesiac = {'1': 'styczen', '2': 'luty', '3': 'marzec', '4': 'kwiecien', '5': 'maj', '6': 'czerwiec',
           '7': 'lipiec', '8': 'sierpien', '9': 'wrzesien', '10': 'pazdziernik', '11': 'listopad', '12': 'grudzien'}


def taking_moon(months, driver, year=None, month=None):
    url = f'http://www.lowiecki.pl/ao/w/{year}/{month}.htm'
    driver.get(url)
    time.sleep(1)
    """save screenshot and return name of it to crop"""
    screen_file_name = screenshot(driver, f'{MAIN_PATH_WINDOWS}\moon')
    file = Image.open(screen_file_name)
    final_photo = cropping_file_moon(file, f'{MAIN_PATH_WINDOWS}\moon', crop_param, months)
    os.remove(screen_file_name)
    return final_photo


def cropping_file_moon(file, new_folder_path, param_to_crop, months=None):
    left, top, right, bottom = param_to_crop
    image_crop = file.crop((left, top, right, bottom))
    file_name = os.path.join(new_folder_path, miesiac[str(months)] + str(datetime.datetime.now().year + 1) + '.png')
    image_crop.save(file_name, quality=95)
    return file_name


driver = start_driver()
for mon in range(1, 13):
    if len(str(mon)) == 2:
        taking_moon(mon, driver, str(datetime.datetime.now().year + 1)[2::], mon)
    else:
        taking_moon(mon, driver, str(datetime.datetime.now().year + 1)[2::], "{:02}".format(mon))
