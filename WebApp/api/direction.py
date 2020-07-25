from dublin_bus.config import GOOGLE_DIRECTION_KEY
from django.http import JsonResponse
from .prediction import predict_journey_time, get_models_name
from .models import SmartDublinBusStop, GTFSTrip
from datetime import datetime

import requests


def directionUntilFirstTransit(origin, destination, departureUnix):
    print("=============================================")
    print('origin:', origin)
    print('destination:', destination)
    print('departureUnix:', departureUnix)

    # check is all the parameters given
    # response 400 error if missing any parameter
    if not(origin and destination and departureUnix):
        response_data = {'message': 'Missing Parameter'}
        return JsonResponse(response_data, status=400)
        
    
    url = 'https://maps.googleapis.com/maps/api/directions/json'

    # defining a params dict for the parameters to be sent to the API 
    PARAMS = {'origin' : origin,
            'destination' : destination,
            'departure_time': departureUnix,
            'key' : GOOGLE_DIRECTION_KEY,
            'transit_mode' : 'bus',
            'mode' : 'transit'} 
            
    # sending get request and saving the response as response object 
    r = requests.get(url = url, params = PARAMS) 
    data = r.json() 

    if data['status'] != 'OK':
        return JsonResponse(data)

    # count how many steps which travel model is TRANSIT
    transitCount = r.text.count("TRANSIT")  
    
    try:

        leg = data['routes'][0]['legs'][0]
        steps = leg['steps']

        # create new dictionary to store direction data
        newData = {'leg': 
                    {'distance' : 0,
                     'duration' : 0,
                     'arrival_time': leg['arrival_time'],
                     'departure_time': leg['departure_time'],
                     'start_location' : leg['start_location'],
                     'start_address' : leg['start_address'],
                     'end_location' : leg['end_location'],
                     'steps' : []}}

        # create variable totalDuration and totalDistance to store updated duration and distance
        totalDuration, totalDistance = 0, 0


        for i in range(len(steps)):
            if isValidStepForPrediction(steps[i]):
                
                lineId = steps[i]['transit_details']['line']['short_name']
                stops = getStopsByStep(steps[i], lineId)

                # if stops num greater tan one, 
                # then segements will be created by stops 
                # prediction will be made by segments
                if len(stops) >= 2:
                    segments = getSegmentsByStops(stops)
                
                    # predict traveling time for all segmentid
                    journeyTime = predict_journey_time(lineId, segments, int(departureUnix))
                    
                    # store stops info in data json for response 
                    steps[i]['transit_details']['stops'] = stops
                    duration = int(journeyTime)
                    print('predict duration:', duration)
                else:
                    duration = int(steps[i]['duration']['value'])
                    print('original duration:', duration)
                    

                distance = int(steps[i]['distance']['value'])
                totalDuration += duration
                totalDistance += distance
                print('duration:', duration, ', totalDuration:', totalDuration)
                
                newData['leg']['steps'].append(steps[i])

                newData['leg']['end_location'] = steps[i]['end_location']
                newData['leg']['duration'] = totalDuration
                newData['leg']['distance'] = totalDistance
                newData['leg']['arrival_time']['value'] += totalDuration
                newData['leg']['arrival_time']['text'] = datetime.utcfromtimestamp(newData['leg']['arrival_time']['value']).strftime('%H:%M')

                if transitCount > 1:
                    break
            
            else:
                
                duration = int(steps[i]['duration']['value'])
                distance = int(steps[i]['distance']['value'])

                totalDuration += duration
                totalDistance += distance
                
                print('duration:', duration, ', totalDuration:', totalDuration)

               # append the step to newData['leg']['steps']
                newData['leg']['steps'].append(steps[i])

                # if the step is the last step
                if i == len(steps)-1:
                    newData['leg']['end_location'] = steps[i]['end_location']
                    newData['leg']['duration'] = totalDuration
                    newData['leg']['distance'] = totalDistance
                    newData['leg']['arrival_time']['value'] += totalDuration
                    newData['leg']['arrival_time']['text'] = datetime.utcfromtimestamp(newData['leg']['arrival_time']['value']).strftime('%H:%M')
                    
  
        newData['status'] = 'OK'
        return newData
        
    except Exception as e:
        print("type error:", str(e))
        message = {'status' : 'Not OK'}
        return message



def isValidStepForPrediction(step):
    if step['travel_mode'] == 'TRANSIT':
        # get all ML models' name 
        # only do the journey time prediction if the model of the line is existed 
        lines = [modelName.replace('.pkl', '') for modelName in get_models_name()]
        lineId = step['transit_details']['line']['short_name'].upper()
        if ('route_'+lineId) in lines:
            return True
    return False

def getStopsByStep(step, lineId):

    arrStopCoord = step['transit_details']['arrival_stop']['location']
    depStopCoord = step['transit_details']['departure_stop']['location']

    # get stop id by stop coordinate
    arrStopId = SmartDublinBusStop.objects.get_nearest_id \
        (arrStopCoord['lat'], arrStopCoord['lng'])
    
    depStopId = SmartDublinBusStop.objects.get_nearest_id \
        (depStopCoord['lat'], depStopCoord['lng'])


    # get stops between origin and destination stops
    headsign = step['transit_details']['headsign']
    origin_time = step['transit_details']['departure_time']['text']

    # print("depStopId:", depStopId)
    # print("arrStopId:", arrStopId)
    # print("lineId:", lineId)
    # print("origin_time:", origin_time)
    # print("headsign:", headsign)


    stops = GTFSTrip.objects.get_stops_between \
        (depStopId, arrStopId, lineId, origin_time=origin_time, headsign=headsign)

    if len(stops) > 0:
        return stops[0] 
    return []

def getSegmentsByStops(stops):

    if len(stops) >= 2: 
        segments = []
        for index in range(len(stops)-1):
            segments.append(stops[index]['plate_code'] + '-' + stops[index+1]['plate_code'])
        return segments
    return []

    



# d = directionUntilFirstTransit((53.2887254, -6.2442945), (53.2943958, -6.1338666), 1594850400)
# print(d)



   
        