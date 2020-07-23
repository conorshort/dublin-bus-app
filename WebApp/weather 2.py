from dublin_bus.config import OPENWEATHER_KEY
import requests
import json
import ast


def getWeatherHourly():

    DUBLIN_COORDINATE = {'lat' : 53.3482, 
                         'lng' : -6.2641}
    url = f'https://api.openweathermap.org/data/2.5/onecall?lat={DUBLIN_COORDINATE["lat"]}&lon={DUBLIN_COORDINATE["lng"]}&exclude=current,daily,minutely&appid={OPENWEATHER_KEY}'
    weatherObj = requests.get(url).json()
    weatherList = weatherObj['hourly']


    # as requested in comment
    with open('weatherData.txt', 'w') as file:
        file.write(json.dumps(weatherList)) 
        file.close()


def getWeather(unixTime):

    with open("weatherData.txt", "r") as file:
        contents = file.read()
        hourlyWeather = ast.literal_eval(contents)
        file.close()


    for weather in hourlyWeather:
        if weather['dt'] == unixTime:
            return weather
    return None
    

getWeatherHourly()
# weather = getWeather(1595016000)
# print(weather)


    