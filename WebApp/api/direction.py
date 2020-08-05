from dublin_bus.config import GOOGLE_DIRECTION_KEY
from django.http import JsonResponse
from .prediction import predict_journey_time, get_models_name
from .models import SmartDublinBusStop, GTFSTrip
from datetime import datetime, timedelta
import requests


def direction_to_first_transit(origin, destination, departureUnix):
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
    PARAMS = {'origin': origin,
              'destination': destination,
              'departure_time': departureUnix,
              'key': GOOGLE_DIRECTION_KEY,
              'transit_mode': 'bus',
              'mode': 'transit'}

    r = requests.get(url=url, params=PARAMS)
    data = r.json()

    # check the status of the google direction response
    if data['status'] != 'OK':
        return JsonResponse(data)

    try:
        # count how many steps which travel model is TRANSIT
        transitCount = r.text.count("TRANSIT")

        leg = data['routes'][0]['legs'][0]
        steps = leg['steps']

        # create new dictionary to store direction data
        newData = {'leg':
                   {'distance': {'value': 0, 'text': ''},
                    'duration': {'value': 0, 'text': ''},
                    'start_location': leg['start_location'],
                    'start_address': leg['start_address'],
                    'end_location': leg['end_location'],
                    'end_address': leg['end_address'],
                    'steps': []},
                   'arrival_time': {},
                   'departure_time': {}}

        # if direction API response json has given departure_time
        # store 'departure_time' data for
        # 'arrival_time' and 'departure_time' in newData
        if 'departure_time' in leg:
            newData['leg']['departure_time'] = leg['departure_time'].copy()
            newData['leg']['arrival_time'] = leg['departure_time'].copy()

        else:
            # FIXME: timezone  & daylight saving problem
            # when convert unix to time string shows one hour late
            timestr = datetime.fromtimestamp(int(departureUnix)) \
                + timedelta(hours=1)
            timestr = timestr.strftime("%I:%M%p")
            newData['leg']['arrival_time'] = {'value': int(departureUnix),
                                              'text': timestr}
            newData['leg']['departure_time'] = {'value': int(departureUnix),
                                                'text': timestr}

        # store updated total distance
        totalDistance = 0

        for index, step in enumerate(steps):

            # check if the step is transit and the line ML model is existed
            # ex: if the value of step is 39, than it is valid,
            # since the route_39.pkl is existed
            if is_valid_for_prediction(step):

                lineId = step['transit_details']['line']['short_name']
                stops = get_stops(step, lineId)

                # if stops num greater than one,
                # then segements will be created by stops
                # prediction will be made by segments
                if len(stops) >= 2:
                    segments = get_segments(stops)

                    # predict traveling time for all segmentid
                    journeyTime = predict_journey_time(
                        lineId,
                        segments,
                        int(departureUnix))

                    # set duration to predicted journey time
                    duration = int(journeyTime)

                    arr_unix = newData['leg']['arrival_time']['value'] + duration
                    timestr = datetime.fromtimestamp(arr_unix) + timedelta(hours=1)
                    timestr = timestr.strftime('%I:%M%p')
                    step['transit_details']['arrival_time']['value'] = arr_unix
                    step['transit_details']['arrival_time']['text'] = timestr
                    step['transit_details']['stops'] = stops
                    step['duration']['value'] = duration
                    step['duration']['text'] = get_time_string(duration)
                    newData['leg']['arrival_time']['value'] = arr_unix

                else:
                    arr_time_unix = int(
                        steps[i]['transit_details']['arrival_time']['value'])
                    newData['leg']['arrival_time']['value'] = arr_time_unix

                distance = int(step['distance']['value'])
                totalDistance += distance

                newData['leg']['steps'].append(step)
                newData['leg']['end_location'] = step['end_location']

                # if there have more than one transit
                # break the for loop
                # set another google direction API requestion
                # to get the direction for rest of the journey
                if transitCount > 1:
                    break

            # if the step is not valied for prediction
            else:
                duration = int(step['duration']['value'])
                distance = int(step['distance']['value'])
                newData['leg']['arrival_time']['value'] += duration
                newData['leg']['steps'].append(step)
                totalDistance += distance

                # if the step is the last step
                # update the newData end_location to end_location of the step
                if index == len(steps)-1:
                    newData['leg']['end_location'] = step['end_location']

        totalDuration = newData['leg']['arrival_time']['value'] - newData['leg']['departure_time']['value']
        newData['leg']['duration']['value'] = totalDuration
        newData['leg']['distance']['value'] = totalDistance
        newData['leg']['duration']['text'] = get_time_string(totalDuration)
        newData['leg']['distance']['text'] = get_destination_string(totalDistance)

        # FIXME: timezone  & daylight saving problem
        # when convert unix to time string shows one hour late
        timestr = datetime.fromtimestamp(newData['leg']['arrival_time']['value']) + timedelta(hours=1)
        timestr = timestr.strftime('%I:%M%p')
        newData['leg']['arrival_time']['text'] = timestr
        newData['status'] = 'OK'
        return newData

    except Exception as e:
        print("direction_to_first_transit error:", str(e))
        message = {'status': 'ZERO_RESULT'}
        return message


def is_valid_for_prediction(step):
    if step['travel_mode'] == 'TRANSIT':
        # get all ML models' name
        # only do the journey time prediction if the model of the line is existed
        lines = [modelName.replace('.pkl', '') for modelName in get_models_name()]
        lineId = step['transit_details']['line']['short_name'].upper()
        if ('route_'+lineId) in lines:
            return True
    return False


def get_stops(step, lineId):
    try:
        arrStopCoord = step['transit_details']['arrival_stop']['location']
        depStopCoord = step['transit_details']['departure_stop']['location']

        # get stop id by stop coordinate
        arrStopId = SmartDublinBusStop.objects.get_nearest_id(arrStopCoord['lat'], arrStopCoord['lng'])
        depStopId = SmartDublinBusStop.objects.get_nearest_id(depStopCoord['lat'], depStopCoord['lng'])

        # get stops between origin and destination stops
        headsign = step['transit_details']['headsign']
        originTime = step['transit_details']['departure_time']['text']

        stops = GTFSTrip.objects.get_stops_between(depStopId, arrStopId, lineId, origin_time=originTime, headsign=headsign)

    except Exception as e:
        print('function get_stops error:', e)
        return []

    if len(stops) > 0:
        return stops[0]
    return []


def get_segments(stops):

    if len(stops) >= 2:
        segments = []
        for index, stop in enumerate(stops, start=1):
            segments.append(stops[index-1]['plate_code'] + '-' + stop['plate_code'])
        return segments
    return []


def get_time_string(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    if h == 0:
        return str(m) + ' mins'
    return str(h) + ' hour ' + str(m) + ' mins'


def get_destination_string(meter):
    km, m = divmod(meter, 1000)

    if km == 0:
        return str(m) + ' m'
    return str(km) + ' km ' + str(m) + ' m'
