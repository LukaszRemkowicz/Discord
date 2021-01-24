import re
import uuid

import bs4
import requests

from global_functions import *
from PIL import Image
import urllib.request


def searching_in_ICM_database(city):
    web_post = requests.post('http://www.meteo.pl/um/php/gpp/next.php', data={"name": f'{city}'})
    post_soup = bs4.BeautifulSoup(web_post.text, "lxml")
    if "NIE ZNALEZIONO" in post_soup.text:
        return None
    post_hrefs = list(post_soup.find_all(href=True))
    id_result = [re.findall("[0-9]+", str(element)) for element in post_hrefs if 'show_mgram' in str(element)][0]
    url = f'http://www.meteo.pl/um/php/meteorogram_id_um.php?ntype=0u&id={str(id_result[0])}'
    get_req = requests.get(url)
    get_soup = bs4.BeautifulSoup(get_req.text, "lxml")
    get_scripts = get_soup.find_all(language=True)
    get = str(get_scripts).split(';')
    var_act_x = [re.findall("[0-9]+", act_x) for act_x in get if 'var act_x' in act_x]
    var_act_y = [re.findall("[0-9]+", act_y) for act_y in get if 'var act_y' in act_y]
    return int(var_act_x[0][0]), int(var_act_y[0][0])


def searching_index(long, lat, array):
    longitude_arr = array[:, :, 1] - long
    latitude_arr = array[:, :, 0] - lat
    distance_between_points = numpy.sqrt(longitude_arr ** 2 + latitude_arr ** 2)
    array_with_distance_results = numpy.unravel_index(numpy.argmin(distance_between_points),
                                                      distance_between_points.shape)
    new_coords = (10 + round((array_with_distance_results[0] - 10) / 7) * 7,
                  10 + round((array_with_distance_results[1] - 10) / 7) * 7)
    return new_coords


def merging_two_photos(city, url):
    base_photo = 'base.png'
    urllib.request.urlretrieve(METEO_BASE_PHOTO, base_photo)
    save_name = 'my_image.png'
    urllib.request.urlretrieve(url, save_name)
    image1 = Image.open(base_photo)
    image2 = Image.open(save_name)
    image1_width, image1_height = image1.size
    image2_width, image2_height = image2.size
    new_image = Image.new('RGB', (image1_width + image2_width, image1_height))
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (image1_width, 0))
    new_path = os.path.join(FILES_PATH_METEPL, city + "merged_image.jpg")
    new_image.save(new_path, "png")
    return new_path


def taking_screen_shot_meteopl(city, coords):
    im_coords_dat = searching_in_ICM_database(city)
    if im_coords_dat:
        url_two = f'http://www.meteo.pl/um/metco/mgram_pict.php?ntype=0u&row=' \
                  f'{im_coords_dat[1]}&col={im_coords_dat[0]}&lang=pl&uid={str(uuid.uuid1())}'
    else:
        coordinates = coords
        parameters_to_website = searching_index(coordinates[0], coordinates[1], MATRIX_RESHAPE)
        url_two = f'http://www.meteo.pl/um/metco/mgram_pict.php?ntype=0u&row=' \
                  f'{parameters_to_website[0]}&col={parameters_to_website[1]}&lang=pl&uid={str(uuid.uuid1())}'
    path_of_new_file = merging_two_photos(city, url_two)
    return path_of_new_file


"""For testing"""

# (coord_list, city), country = find_city_coordinates('gdansk')
# taking_screen_shot_meteopl('gdansk', coord_list)
