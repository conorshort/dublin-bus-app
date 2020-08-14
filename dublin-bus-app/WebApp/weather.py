from dublin_bus.config import OPENWEATHER_KEY
from dublin_bus.settings import BASE_DIR
import requests
import json
import ast
import bisect
import os

def getWeatherHourly():

    DUBLIN_COORDINATE = {'lat': 53.3482,
                         'lng': -6.2641}
    url = f'https://api.openweathermap.org/data/2.5/onecall?lat={DUBLIN_COORDINATE["lat"]}&lon={DUBLIN_COORDINATE["lng"]}&exclude=current,daily,minutely&appid={OPENWEATHER_KEY}'
    weatherObj = requests.get(url).json()
    weatherList = weatherObj['hourly']

    # get all dt values and store in a list
    # to make the future query faster
    dt_values = [i['dt'] for i in weatherList]

    with open(os.path.join(BASE_DIR, "weatherData.txt"), 'w') as file:

        # weather_dt_values : store the whole weather list which within 48 hrs
        # weather_hourly_data : store the dt of each weather in a list
        obj = {'weather_dt_values': dt_values,
               'weather_hourly_data': weatherList}

        file.write(json.dumps(obj))
        file.close()


def getWeather(unixTime):

    with open(os.path.join(BASE_DIR, "weatherData.txt"), "r") as file:
        contents = file.read()
        data = ast.literal_eval(contents)

        weather_hourly_data = data['weather_hourly_data']
        weather_dt_values = data['weather_dt_values']
        file.close()

    if len(weather_hourly_data) == 0:
        return None

    # check if the request unixTime within 48 hour
    if ((unixTime >= weather_dt_values[0]) and (unixTime <= weather_dt_values[len(weather_dt_values)-1])):
        # find the clostest dt value in the list by binary search
        weatherIndex = bisect.bisect(weather_dt_values, unixTime)
        if weatherIndex == len(weather_dt_values):
            weatherIndex -= 1
        return weather_hourly_data[weatherIndex]
    return None

if  __name__ == "__main__":

    getWeatherHourly()
