import pandas as pd
from weather import getWeather
import datetime
import time
import pickle


def predict_journey_time(lineId, segments, departure_unix):
    
    modelFile = f'//Users/wenghsin-ping/Desktop/dublin-bus-app/WebApp/pickles/{lineId}.pkl'
    
    # Load the Model back from file
    with open(modelFile, 'rb') as file:  
        model = pickle.load(file)

    # get all features of the route model
    features = model.get_booster().feature_names

    # create a dictionary and set key to features and value to [0]
    dic = {feature: [0] for feature in features}
    departure_dt = datetime.datetime.fromtimestamp(departure_unix)
    

    hour = departure_dt.hour
    weekday = departure_dt.weekday
    # isPeak = isPeaktime(departure_dt)
    isPeak = int(isPeaktime(departure_dt) == True)

    weather = getWeather(int(departure_unix))
    if weather:
        dic['temp'] = [weather['temp']]
        dic['wind_speed'] = [weather['wind_speed']]
        dic['sun'] = [weather['wind_speed']]

    df = pd.DataFrame()

    for seg in segments:
        
        try:
            dic['arr_hour_' + hour] = [1]
            dic['segment_id_' + seg] = [1]
            dic['weekday'] = [weekday]
            dic['isPeaktime'] = [isPeak]

            
        except:
            pass
        
        seg_df = pd.DataFrame(data=dic)
        seg_df = seg_df[features]

        # add each segment dataframe to df dataframe
        df = df.append(seg_df, ignore_index=True)

    prediction = model.predict(df)
    journeyTime = sum(prediction)

    return journeyTime



def isPeaktime(dt):
    return (dt.time() >= datetime.time(6, 30) and dt.time() <= datetime.time(9, 30)) \
        or (dt.time() >= datetime.time(15, 30) and dt.time() <= datetime.time(18, 30))

# isPeak = isPeaktime(datetime.datetime.now())
# print(isPeak)