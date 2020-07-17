import pandas as pd
from weather import getWeather
import datetime
import time
import pickle
from os import walk

def predict_journey_time(lineId, segments, departure_unix):
    
    print('=========predict_journey_time===========')
    # cheak if the departure unix within 48 hour,
    # forecase weather only provide within 48 hour
    
    weather = getWeather(int(departure_unix))
    print(weather)
    if weather != None:
        model = get_route_model(lineId)

    else:
        model = get_route_model(lineId, hasWeather = False)
    
        
    # get all features of the route model
    features = model.get_booster().feature_names


    # create a dictionary as data for creating tested dataframe 
    # set dictionary key to features and value to [0]
    data = {feature: [0] for feature in features}
    departure_dt = datetime.datetime.fromtimestamp(departure_unix)
    
    hour = departure_dt.hour
    weekday = departure_dt.weekday
    isPeak = int(isPeaktime(departure_dt) == True)

    segments_df = pd.DataFrame()

    for seg in segments:
        
        try:
            data['arr_hour_' + hour] = [1]
            data['segment_id_' + seg] = [1]
            data['weekday' + weekday] = [1]
            data['isPeaktime'] = [isPeak]
        except:
            pass
        
        
        if weather:
            data['temp'] = [weather['temp']]
            data['wind_speed'] = [weather['wind_speed']]
            if 'rain' in weather:
                data['rain'] = [weather['rain']['1h']]
        

        # create segment dataframe which storing segment data
        seg_df = pd.DataFrame(data=data)

        # reorder the columns sequence same as the model
        seg_df = seg_df[features]

        # add each segment dataframe to df dataframe
        segments_df = segments_df.append(seg_df, ignore_index=True)

    # ger journey time prediction for all segments
    journeyTime = predict_journey_time_by_df(segments_df, lineId)
    
    print(journeyTime)

    return journeyTime




def predict_journey_time_by_df(test_dataframe, lineId):

    weatherFeatures = ["wind_speed", "temp", "rain"]
    isWeatherColumnsExist =  all(elem in weatherFeatures  for elem in test_dataframe)


    if isWeatherColumnsExist:
        model = get_route_model(lineId)
    else:
        model = get_route_model(lineId, hasWeather = False)

    # predict journey time
    prediction = model.predict(test_dataframe)
    journeyTime = sum(prediction)

    return journeyTime


def get_models_name():

    files = []
    for (dirpath, dirnames, filenames) in walk('/Users/wenghsin-ping/Desktop/dublin-bus-app/WebApp/pickles/pickles'):
        files.extend(filenames)
        break
    return files



def get_route_model(lineId, hasWeather = False):

    # path for model pickle without weather
    modelFile = f'//Users/wenghsin-ping/Desktop/dublin-bus-app/WebApp/pickles/pickles/route_{lineId}.pkl'
    
    if hasWeather == False:
        # path for model pickle
        modelFile = f'//Users/wenghsin-ping/Desktop/dublin-bus-app/WebApp/pickles/pickles_without_weather/route_{lineId}_without_weather.pkl'
    
    print('modelFile::::', modelFile)
    
    
    # Load the Model back from file
    with open(modelFile, 'rb') as file:  
        model = pickle.load(file)

    return model


def isPeaktime(dt):
    return (dt.time() >= datetime.time(6, 30) and dt.time() <= datetime.time(9, 30)) \
        or (dt.time() >= datetime.time(15, 30) and dt.time() <= datetime.time(18, 30))

# isPeak = isPeaktime(datetime.datetime.now())
# print(isPeak)


# f = get_models_name()
# print(f)