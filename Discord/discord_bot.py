"""This is my first Discord Bot"""
import asyncio
import calendar
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord_clearousite_screenshots import *
from discord_meteoblue_screenshots import *
from discord_meteopl_screenshots import *
from global_functions import *
from local_variables import *
from testing_speed_time import *
from trip_task_code import taking_screenshot_with_task_before_trip_function
from pathlib import Path
import sys

env_path = (Path('.') / '.env') if sys.version[0:3] == '3.6' else ''
load_dotenv(env_path)
TOKEN = os.getenv('DISCORD_TOKEN')[1:-1]
GUILD = os.getenv('DISCORD_GUILD')[1:-1]

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='!', intents=intents)

"""Events"""


@bot.event
async def on_ready():
    """searching the guild with name of the variable GUILD:"""
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user} is connected to the following guild:\n\n'
        f'Welcome to {guild.name} (id: {guild.id}) \n'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n\n - {members}')
    print('Debugs prints:  \n')
    """searching specified member and returning it:"""


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f"Hi {member.name}, welcome to our Discord server!"
    )


"""just for fun. Not used. Event when bot is answering on words"""


# @bot.event
# async def answer_on_message(message):
#     if message.author == bot.user:
#         return
#     if message.channel.id == CHANNELS['ogolny']:
#         return
#     for key, value in ANSWER_DICT.items():
#         if message.content in key:
#             answer, weight = value
#             bot_answer = random.choices(answer, weights=weight)
#             if bot_answer[0] is not None:
#                 await message.channel.send(str(bot_answer[0]))
#     """After await on_message bot no longer w8 for commands. That's why its important to use this:"""
#     await bot.process_commands(message)


@bot.event
async def on_error(event, *args):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


"""Sys commands"""


@bot.command(name='newchannel')
@commands.has_role('Admin')
async def create_channel(ctx, channel_name='new_one'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)


@bot.command(name='cahe')
@commands.has_role('Admin')
async def create_channel(ctx):
    await ctx.send(f'Cahe len is {len(COORDS_CACHE)}')


"""Weather commands"""


@bot.command(name='meteo',
             help="")
async def returning_weather_on_wish(ctx, name):
    if is_trip_started and name in TRIP_CITIES:
        name_of_file, date_created = weather_from_disc(name, FILES_PATH_TRIP, 'meteo')
        await ctx.send(f'This page has been generated @{date_created}')
        await ctx.send(file=discord.File(name_of_file))
    elif name not in ['sonsk', 'elblag', 'nysa']:
        await ctx.send(f'wrong city name. You can choose only beetween Sonk, Elblag, Nysa')
    else:
        """just for testing"""
        # new_folder_path = creating_empty_folder(FILES_PATH)
        # os.mkdir(new_folder_path)
        # name_of_file = taking_screen_shot_meteoblue(name, new_folder_path, FILES_PATH)
        # name_of_file, name_of_directory = weather_from_disc(name, FILES_PATH, 'meteo')
        # await ctx.send(f'This page has been generated @{name_of_directory}')
        name_of_file, date_created = weather_from_disc(name, SAVING_TO_DISC_TASK, 'meteo')
        await ctx.send(f'This page has been generated @{date_created}')
        await ctx.send(file=discord.File(name_of_file))


"""Global FLag"""
is_trip_started = False


@bot.command(name='clear',
             pass_context=True,
             help="use it with params:"
                  "1) !clear CITY_NAME - returning today's weather"
                  "2) !clear CITY_NAME ALL - returning table with all days"
                  "3) !clear CITY_NAME DAY - returning specific day (from now + 7 days)."
             )
async def returning_clearoutsite_on_wish(ctx, name, day=None):
    global task_or_not
    task_or_not = False
    cities = ['elblag', 'sonsk', 'nysa']
    starts = start()
    day_list = datetime_list()
    """check if trip started. If yes, then event should write photos to disc"""
    if name in cities or (is_trip_started is True and name in TRIP_CITIES):
        if day:
            if day.isalpha() and not day == 'all':
                await ctx.send(f'you think you know me..')
                return
            elif day == 'all':
                if name in TRIP_CITIES:
                    name_of_file, name_of_directory = weather_from_disc(name, FILES_PATH_TRIP, 'clear', day)
                else:
                    name_of_file, name_of_directory = weather_from_disc(name, SAVING_TO_DISC_TASK, 'clear', day)
                await ctx.send(f'This page has been generated @{name_of_directory}')
                await ctx.send(file=discord.File(name_of_file))
            elif not day.isdigit() or int(day) not in day_list:
                await ctx.send(
                    random.choices((f'Wrong day / parameter. You can only generate weather from now to +7 days later. '
                                    f'Choose beetween: 'f'{day_list}', 'Oh come one! is that hard?'), (6, 2)))
                return
            elif day.isdigit and int(day) in day_list:
                if name in TRIP_CITIES:
                    name_of_file, name_of_directory = weather_from_disc(name, FILES_PATH_TRIP, 'clear', int(day))
                else:
                    name_of_file, name_of_directory = weather_from_disc(name, SAVING_TO_DISC_TASK, 'clear', int(day))
                await ctx.send(f'This page has been generated @{name_of_directory}')
                await ctx.send(file=discord.File(name_of_file))
        else:
            if name in TRIP_CITIES:
                name_of_file, name_of_directory = weather_from_disc(name, FILES_PATH_TRIP, 'clear')
            else:
                name_of_file, name_of_directory = weather_from_disc(name, SAVING_TO_DISC_TASK, 'clear')
            await ctx.send(f'Generating today\'s weather')
            await ctx.send(f'This page has been generated @{name_of_directory}')
            await ctx.send(file=discord.File(name_of_file))
    else:
        preparing_empty_folder(FILES_PATH_CLEAR)
        new_folder_path = creating_empty_folder(FILES_PATH_CLEAR, name)
        new_city_folder_path = os.path.join(new_folder_path, '')
        try:
            clearing_cahe(COORDS_CACHE)
            (city_coordinates), country = COORDS_CACHE[name]
        except KeyError:
            (city_coordinates), country = find_city_coordinates(name)

        """checking if users search city from allowed countries
            it is must have coz Nominatim generates strange names like 'Dupa'"""

        if country not in COUNTRIES_FOR_SEARCH or not city_coordinates:
            await ctx.send(f'Wrong city man')
            return
        driver = start_driver()
        if day:
            if day.isalpha() and not day == 'all':
                await ctx.send(f'you think you know me..')
                return
            elif day == 'all':
                photo = taking_screen_shot_clearoutsite(new_city_folder_path, FILES_PATH_CLEAR, city_coordinates,
                                                        driver, task_or_not, day)
            elif int(day) > calendar.monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[1]:
                await ctx.send(f'{calendar.month_name[datetime.datetime.now().month]} dont have {day} days. Try again')
                return
            elif int(day) not in day_list:
                await ctx.send(random.choices((f'Wrong day / parameter. You can only generate weather from now to +7 '
                                               f'days later. Choose beetween: 'f'{day_list}',
                                               'Oh come one! is that hard?'), (6, 2)))
                return
            elif day.isdigit() and int(day) in day_list:
                photo = taking_screen_shot_clearoutsite(new_city_folder_path, FILES_PATH_CLEAR, city_coordinates,
                                                        driver, task_or_not, int(day))
        else:
            photo = taking_screen_shot_clearoutsite(new_city_folder_path, FILES_PATH_CLEAR, city_coordinates,
                                                    driver, task_or_not)
        now = datetime.datetime.now()
        driver.close()
        await ctx.send(f'This page has been generated @{now.strftime("%H:%M")}')
        await ctx.send(f'This code was generated in {stop(starts)}')
        await ctx.send(file=discord.File(photo))


@bot.command(name='umm',
             pass_context=True,
             help="This command will show you The Meteo.pl weather. "
             )
async def returning_weather_on_wish(ctx, name):
    try:
        clearing_cahe(COORDS_CACHE)
        (city_coordinates, city), country = COORDS_CACHE[name]
    except KeyError:
        (city_coordinates, city), country = find_city_coordinates(name)
    if city_coordinates and country in COUNTRIES_FOR_SEARCH:
        screenshot_path = taking_screen_shot_meteopl(name, city_coordinates)
        await ctx.send(file=discord.File(screenshot_path))
    else:
        await ctx.send(f'Wrong city')


@bot.command(name='sat')
async def return_sat(ctx):
    if 16 <= datetime.datetime.now().hour or datetime.datetime.now().hour <= 7:
        url = "https://api.sat24.com/animated/EU/infraPolair/3/Central%20European%20Standard'%20width=845%20height=615"
        urllib.request.urlretrieve(url, 'sat24\satinfra.gif')
        await ctx.send(file=discord.File(os.path.join(SAT_FOLDER, 'satinfra.gif')))
    else:
        url = "http://api.sat24.com/animated/EU/visual/3/Central%20European%20Standard'%20width=845%20height=615"
        urllib.request.urlretrieve(url, 'sat24\sat.gif')
        await ctx.send(file=discord.File(os.path.join(SAT_FOLDER, 'sat.gif')))


"""Tasks"""


@bot.command(hidden=True)
async def sending_weather_meteoblue_with_spec_hour():
    hour = ['07:00', '16:00', "18:00", '20:00']
    await bot.wait_until_ready()
    while not bot.is_closed():
        whats_the_hour_now = datetime.datetime.now().time().strftime("%H:%M")
        message_channel_id = CHANNELS['daily_weather']
        message_channel = bot.get_channel(message_channel_id)
        if whats_the_hour_now in hour:
            for city in DAYLY_CITIES:
                name_of_file, name_of_directory = weather_from_disc(city, SAVING_TO_DISC_TASK, 'meteo')
                await message_channel.send(f"{city} weather generated@ {name_of_directory}")
                await message_channel.send(file=discord.File(name_of_file))
        await asyncio.sleep(14400)


bot.loop.create_task(sending_weather_meteoblue_with_spec_hour())


@tasks.loop(hours=1)
async def called_once_a_hours_to_save_file():
    task_or_not = True
    print(id(task_or_not))
    print(f'Started task at: {datetime.datetime.now().strftime("%H:%M")}')
    day_list = datetime_list()
    whats_the_hour_now = int(datetime.datetime.now().time().strftime("%H"))
    if 0 < whats_the_hour_now < 6:
        pass
    else:
        driver = start_driver()
        started = start()
        preparing_empty_folder(SAVING_TO_DISC_TASK)
        os.mkdir(os.path.join(SAVING_TO_DISC_TASK, 'meteo'))
        new_folder_path = os.path.join(SAVING_TO_DISC_TASK, 'meteo', '')
        for city in DAYLY_CITIES:
            taking_screen_shot_meteoblue(city, new_folder_path, SAVING_TO_DISC_TASK, driver)
        for city in DAYLY_CITIES:
            os.makedirs(os.path.join(SAVING_TO_DISC_TASK, 'clear', city))
            new_city_folder_path = os.path.join(SAVING_TO_DISC_TASK, 'clear', city, '')
            (coord_list), country = find_city_coordinates(city)
            taking_screen_shot_clearoutsite(new_city_folder_path, SAVING_TO_DISC_TASK, coord_list, driver, task_or_not)
            for days in day_list:
                taking_screen_shot_clearoutsite(new_city_folder_path, SAVING_TO_DISC_TASK, coord_list, driver,
                                                task_or_not, days)
            taking_screen_shot_clearoutsite(new_city_folder_path, SAVING_TO_DISC_TASK, coord_list, driver,
                                            task_or_not, 'all')
        driver.quit()
        print('generated in: ', stop(started))
        time.sleep(2)


called_once_a_hours_to_save_file.start()


@tasks.loop(hours=random.choice([3, 4, 6, 8]))
async def called_once_a_some_hours():
    answers = ['Hey, you missed me?', 'Its Friday soon   \\.^.^./',
               "whats uuuuuuuuuup?"]
    message_channel_id = CHANNELS['ogolny']
    message_channel = bot.get_channel(message_channel_id)
    whats_the_hour_now = datetime.datetime.now().time().strftime("%H")
    if 22 > int(whats_the_hour_now) > 7:
        response = random.choice(answers)
        await message_channel.send(response)


@called_once_a_some_hours.before_loop
async def before():
    await bot.wait_until_ready()
    print("Finished waiting")


# called_once_a_some_hours.start()

"""Before Trip tasks"""


@bot.command(name='trip', help='start checking weather before trip', pass_context=True)
async def start_saving_trip_location_weather(ctx, name):
    global is_trip_started
    message_channel_id = CHANNELS['daily_weather']
    message_channel = bot.get_channel(message_channel_id)
    if name == 'stop':
        await message_channel.send('The trip has stopped')
        is_trip_started = False
        start_saving_once_four_hours.cancel()
    elif name == 'start':
        await message_channel.send('The trip has started')
        is_trip_started = True
        start_saving_once_four_hours.start()
    else:
        await message_channel.send('Wrong Value. Use command: "trip start" or "trip stop"')


@bot.command(name='moon')
async def give_me_a_moon(ctx, month):
    if not month.isdigit():
        await ctx.send('Podaj miesiac w postaci liczby')
    else:
        name_of_file = weather_from_disc(CALENDER[str(month)], MOON, 'moon')
        await ctx.send(file=discord.File(name_of_file))


@tasks.loop(hours=5)
async def start_saving_once_four_hours():
    cities_list = ['steznica', 'lapszanka', 'lutowiska', 'zakopane']
    driver = start_driver()
    taking_screenshot_with_task_before_trip_function(cities_list, driver)
    driver.quit()


@start_saving_once_four_hours.before_loop
async def before():
    await bot.wait_until_ready()


@tasks.loop(hours=1)
async def preparing_folders():
    update_time = '00'
    whats_the_hour_now = datetime.datetime.now().time().strftime("%H")
    if whats_the_hour_now == update_time:
        preparing_empty_folder(FILES_PATH)
        preparing_empty_folder(FILES_PATH_METEPL)


preparing_folders.start()


@tasks.loop(hours=24)
async def send_moon():
    await bot.wait_until_ready()
    day_now = datetime.datetime.now().date().strftime("%d/%m/%Y")[0:2]
    if day_now == '02':
        message_channel_id = CHANNELS['moon']
        message_channel = bot.get_channel(message_channel_id)
        name_of_file = weather_from_disc(CALENDER[str(datetime.datetime.now().month)], MOON, 'moon')
        await message_channel.send(file=discord.File(name_of_file))


send_moon.start()

bot.run(TOKEN, bot=True)
