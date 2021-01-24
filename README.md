<h2> Discord bot</h2>

Main functionality (discord_bot.py) is to capture screenshots of some website to get current weather/ astro-weather and return them to Discord on wish. You can find there some tasks which are making screenshots in specified time. Each website is a separate file. There are some additional files:

- base.png - is used for merge with meteo screenshot (required)
- city_base.xlsx, city_base_dictionary.txt - Polish cities coordinates (not required)
- exporting_xml_todict_file.py - additional script for export data from xlsx to txt (not required)
- moon.py - script for getting screenshots with information about full Moon and new Moon. (not required)
- testing_speed_time.py - some script for check time speed of taking screenshots (not required)
- trip_task_code.py - if you going to plan some trip, you can add cities where you gonna travel, and start task wich will collect screenshots in some period of time

<b><h2>Usage</h2></b>

1) Put your path to your folders (main configuration in local_variables.py),
2) Create them in main Discord folder, 
3) Add your discord name channels in dictionary (CHANNELS) as: {'channel_name': channel ID}
4) Add cities to variables:

CITIES = dict() <br>
TRIP_CITIES = [] <br>
DAYLY_CITIES = []

5) If you want to have possibility to give an "answer" to channel with random time or for speccific word, add answers to:

WRONG_VALUE = [] <br>
ANSWER_DICT = {}

6) Add coutries, where you want to search weater to be sure, user will not use strange words. Used in UM.

COUNTRIES_FOR_SEARCH = []

7) Dont forget to create .env file with your Discord token and server name:

DISCORD_TOKEN={wirte you token here}<br>
DISCORD_GUILD={write your guildname here}


<b>Note</b> that you need to change code for UM function if you want use it, becouse code needs some file with data (.bin) which is not included here. 


