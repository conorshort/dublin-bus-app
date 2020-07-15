from dublin_bus.config import OPENWEATHER_KEY
import requests


WEATHER_DATA = []

def getWeatherHourly():

    DUBLIN_COORDINATE = {'lat' : 53.3482, 
                         'lng' : -6.2641}
    url = f'https://api.openweathermap.org/data/2.5/onecall?lat={DUBLIN_COORDINATE["lat"]}&lon={DUBLIN_COORDINATE["lng"]}&exclude=current,daily,minutely&appid={OPENWEATHER_KEY}'
    weatherObj = requests.get(url).json()
    WEATHER_DATA = weatherObj['hourly']
    print(WEATHER_DATA)


def getWeather(unixTime):
    for hourWeather in WEATHER_DATA:
        if hourWeather['dt'] == unixTime:
            return hourWeather
    return None
    

getWeatherHourly()


    