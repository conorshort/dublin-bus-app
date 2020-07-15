import pandas as pd
import datetime
import pickle


def predict_journey_time(lineId, segments, departure_dt):
    
    modelFile = f'//Users/wenghsin-ping/Desktop/dublin-bus-app/WebApp/pickles/{lineId}.pkl'
    
    # Load the Model back from file
    with open(modelFile, 'rb') as file:  
        model = pickle.load(file)

    # get all features of the route model
    features = model.get_booster().feature_names

    # create a dictionary and set key to features and value to [0]
    dic = {feature: [0] for feature in features}
    
    hour = departure_dt.hour
    weekday = departure_dt.weekday
    isPeak = int(isPeaktime(departure_dt) == True)


    df = pd.DataFrame()

    for seg in segments:
        
        try:
            dic['arr_hour_' + hour] = [1]
            dic['segment_id_' + seg] = [1]
            dic['weekday'] = [weekday]
            dic['isPeaktime'] = [isPeak]

            dic['temp'] = [1]
            dic['wind_speed'] = [2]
            dic['sun'] = [0.0]
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
