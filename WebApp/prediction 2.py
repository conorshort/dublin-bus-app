import pandas as pd
from weather import getWeather
import datetime
import time
import pickle
from os import walk

def predict_journey_time(lineId, segments, departure_unix, return_list=False):
    print(departure_unix)
    segments_df = create_test_dataframe(lineId, segments, departure_unix)

    # cheak if df has weather features
    weatherFeatures = ['temp', 'wind_speed', 'rain']
    hasWeatherFeatures =  all(elem in weatherFeatures for elem in segments_df.columns)
    if hasWeatherFeatures:
        model = get_route_model(lineId)
    else:
        model = get_route_model(lineId, hasWeather = False)


    # ger journey time prediction for all segments
    journeyTime = predict_journey_time_by_df(model, segments_df, return_list=return_list)
    
    return journeyTime



def create_test_dataframe(lineId, segments, departure_unix):
    
    # cheak if the departure unix within 48 hour,
    # forecase weather only provide within 48 hour
   
    weather = getWeather(int(departure_unix))
    
    if weather != None:
        model = get_route_model(lineId)
    else:
        model = get_route_model(lineId, hasWeather = False)
    
        
    # get all features of the route model
    features = model.get_booster().feature_names



    departure_dt = datetime.datetime.fromtimestamp(departure_unix)
    print(departure_dt)
    print("Line", lineId, )
    hour = departure_dt.hour
    weekday = departure_dt.weekday()
    isPeak = int(isPeaktime(departure_dt) == True)

    segments_df = pd.DataFrame()

    for seg in segments:
            # create a dictionary as data for creating tested dataframe
        # set dictionary key to features and value to [0]
        data = {feature: [0] for feature in features}

        data['arr_hour_' + str(hour)] = [1]
        data['segment_id_' + str(seg)] = [1]
        data['weekday_' + str(weekday)] = [1]
        data['isPeaktime'] = [isPeak]
        

        if weather:
            data['temp'] = [weather['temp']]
            data['wind_speed'] = [weather['wind_speed']]
            if 'rain' in weather:
                data['rain'] = [weather['rain']['1h']]
        
        # create segment dataframe which storing segment data
        seg_df = pd.DataFrame(data=data)

        # print(seg_df)
        # reorder the columns sequence same as the model
        seg_df = seg_df[features]

        # add each segment dataframe to df dataframe
        segments_df = segments_df.append(seg_df, ignore_index=True)
    segments_df.to_csv(r'C:\Users\cls15\Desktop\test.csv', index=False)
    return segments_df




def predict_journey_time_by_df(model, test_dataframe, return_list=False):
    
    prediction = model.predict(test_dataframe)

    if return_list:

        segment_cols = [
                col for col in test_dataframe if col.startswith('segment')]

        idxs = test_dataframe.loc[(test_dataframe[segment_cols] == 0).all(axis=1)].index

        for idx in idxs:
            prediction[idx] = -1
        print(prediction)
        return prediction
    else:
        journeyTime = sum(prediction)
        return journeyTime



def get_models_name():

    files = []
    for (dirpath, dirnames, filenames) in walk('WebApp/pickles/pickles'):
        files.extend(filenames)
        break
    return files

def get_route_model(lineId, hasWeather = False):

    # path for model pickle without weather
    modelFile = f'WebApp/pickles/pickles/route_{lineId}.pkl'
    
    if hasWeather == False:
        # path for model pickle
        modelFile = f'WebApp/pickles/pickles_without_weather/route_{lineId}_without_weather.pkl'

    
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