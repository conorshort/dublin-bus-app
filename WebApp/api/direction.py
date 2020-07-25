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

    # extracting data in json format 
    data = r.json() 

    if data['status'] != 'OK':
        return JsonResponse(data)

    transitCount = r.text.count("TRANSIT")  
    
    # check if the specific route model exist
    # if yes: predict the jourent time
    # if not: response google direction API data 
    try:
        lines = [modelName.replace('.pkl', '') for modelName in get_models_name()]

        leg = data['routes'][0]['legs'][0]
        
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

       
        steps = leg['steps']

        totalDuration, totalDistance = 0, 0

        # forloop steps from google direction API response
        for i in range(len(steps)):


            # print('i:', i, ' ,mode:', steps[i]['travel_mode'], ',step[i]:', steps[i])
            # check if the step travel_mode is TRANSIT
            # if not, save duration and distance value of this step to totalDuration, totalDistance
            # than skip this loop to next index
            if (steps[i]['travel_mode'] != 'TRANSIT'):
                duration = int(steps[i]['duration']['value'])
                distance = int(steps[i]['distance']['value'])

                totalDuration += duration
                totalDistance += distance

               # append the step to newData['leg']['steps']
                newData['leg']['steps'].append(steps[i])

                # if the step is the last step
                if i == len(steps)-1:
                    newData['leg']['end_location'] = steps[i]['end_location']
                    newData['leg']['duration'] = totalDuration
                    newData['leg']['arrival_time']['value'] += totalDuration
                    newData['leg']['arrival_time']['text'] = datetime.utcfromtimestamp(newData['leg']['arrival_time']['value']).strftime('%H:%M')
                    

                continue
            
            # check if the line model exist 
            lineId = steps[i]['transit_details']['line']['short_name'].upper()
            if ('route_'+lineId) not in lines:
                duration = int(steps[i]['duration']['value'])
                distance = int(steps[i]['distance']['value'])
                totalDuration += duration
                totalDistance += distance
                
                # append the step to newData['leg']['steps']
                newData['leg']['steps'].append(steps[i])
                # if the step is the last step
                if i == len(steps)-1:
                    
                  
                    newData['leg']['end_location'] = steps[i]['end_location']
                    newData['leg']['duration'] = totalDuration
                    newData['leg']['distance'] = totalDistance
                # print('end_location:', steps[i]['end_location'])
                # print('new data end_location:', newData['leg']['end_location'])
                    
                    newData['leg']['arrival_time']['value'] += totalDuration
                    newData['leg']['arrival_time']['text'] = datetime.utcfromtimestamp(newData['leg']['arrival_time']['value']).strftime('%H:%M')
                    
                continue

            arrStopCoordination = steps[i]['transit_details']['arrival_stop']['location']
            depStopCoordination = steps[i]['transit_details']['departure_stop']['location']

            # get stop id by stop coordinate
            arrStopId = SmartDublinBusStop.objects.get_nearest_id \
                (arrStopCoordination['lat'], arrStopCoordination['lng'])
            
            depStopId = SmartDublinBusStop.objects.get_nearest_id \
                (depStopCoordination['lat'], depStopCoordination['lng'])
            
            

            # get stops between origin and destination stops
            headsign = steps[i]['transit_details']['headsign']
            origin_time = steps[i]['transit_details']['departure_time']['text']

            print("depStopId:", depStopId)
            print("arrStopId:", arrStopId)
            print("lineId:", lineId)
            print("origin_time:", origin_time)
            print("headsign:", headsign)
            

            stops = GTFSTrip.objects.get_stops_between(depStopId, arrStopId, lineId, origin_time=origin_time, headsign=headsign)

            

            if len(stops) <= 0:
                print('stop len <= 0')

                newData['leg']['end_location'] = steps[i]['end_location']
                newData['leg']['duration'] = totalDuration
                newData['leg']['arrival_time']['value'] += totalDuration
                newData['leg']['arrival_time']['text'] = datetime.utcfromtimestamp(newData['leg']['arrival_time']['value']).strftime('%H:%M')
                print("arr time:", newData['leg']['arrival_time'])
                continue
            
            
            stops = stops[0]
        

            # get all the segmentid by stopsid
            segments = []
            for index in range(len(stops)-1):
                segments.append(stops[index]['plate_code'] + '-' + stops[index+1]['plate_code'])
            
            # predict traveling time for all segmentid
            lineId = steps[i]['transit_details']['line']['short_name']
            journeyTime = predict_journey_time(lineId, segments, int(departureUnix))

            # store stops info in data json for response 
            stepData = steps[i]
            stepData['transit_details']['stops'] = stops
            
            duration = int(journeyTime) // 60
            distance = int(steps[i]['distance']['value'])
            totalDuration += duration
            totalDistance += distance
            newData['leg']['steps'].append(stepData)

           
            
            newData['leg']['end_location'] = stepData['end_location']
            newData['leg']['duration'] = totalDuration
            newData['leg']['distance'] = totalDistance

            newData['leg']['arrival_time']['value'] += totalDuration
            newData['leg']['arrival_time']['text'] = datetime.utcfromtimestamp(newData['leg']['arrival_time']['value']).strftime('%H:%M')

            if transitCount > 1:
                break
  
        newData['status'] = 'OK'
        return newData
        

    except Exception as e:
        print("type error:", str(e))
        message = {'status' : 'Not OK'}
        return message


# d = directionUntilFirstTransit((53.2887254, -6.2442945), (53.2943958, -6.1338666), 1594850400)
# print(d)



   
        