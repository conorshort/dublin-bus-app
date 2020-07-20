import pandas as pd
from weather import getWeather
import datetime
import time
import pickle
import os


path = os.path.dirname(__file__)

def predict_journey_time(lineId, segments, departure_unix):
    
    # get route model
    model = get_route_model(lineId)
    
    # get all features of the route model
    features = model.get_booster().feature_names

    # create a dictionary as data for creating tested dataframe 
    # set dictionary key to features and value to [0]
    data = {feature: [0] for feature in features}
    departure_dt = datetime.datetime.fromtimestamp(departure_unix)
    
    hour = departure_dt.hour
    weekday = departure_dt.weekday
    isPeak = int(isPeaktime(departure_dt) == True)

    weather = getWeather(int(departure_unix))
    if weather:
        data['temp'] = [weather['temp']]
        data['wind_speed'] = [weather['wind_speed']]
        if 'rain' in weather:
            data['rain'] = [weather['rain']['1h']]
        

    segments_df = pd.DataFrame()

    for seg in segments:
        
        try:
            data['arr_hour_' + hour] = [1]
            data['segment_id_' + seg] = [1]
            data['weekday' + weekday] = [1]
            data['isPeaktime'] = [isPeak]
        except:
            pass
        
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

    model = get_route_model(lineId)

    # predict journey time
    prediction = model.predict(test_dataframe)
    journeyTime = sum(prediction)

    return journeyTime


def get_models_name():

    files = []
    for (dirpath, dirnames, filenames) in os.walk(f'{path}/pickles'):
        files.extend(filenames)
        break
    return files



def get_route_model(lineId):
    # path for model pickle
    modelFile = f'{path}/pickles/route_{lineId}.pkl'
    
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
