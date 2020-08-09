from dublin_bus.config import GOOGLE_DIRECTION_KEY
from django.http import JsonResponse
from .prediction import predict_journey_time, get_models_name
from .models import SmartDublinBusStop, GTFSTrip
from datetime import datetime, timedelta
import requests
import logging


logger = logging.getLogger(__name__)


def direction_to_first_transit(origin, destination, departureUnix):
    print("=============================================")
    print('origin:', origin)
    print('destination:', destination)
    print('departureUnix:', departureUnix)


    # check is all the parameters given
    # response 400 error if missing any parameter
    if not(origin and destination and departureUnix):
        response_data = {'message': 'Missing Parameter',
                        'status': 'Zero Result'}
        return response_data

    url = 'https://maps.googleapis.com/maps/api/directions/json'
    PARAMS = {'origin': origin,
              'destination': destination,
              'departure_time': departureUnix,
              'key': GOOGLE_DIRECTION_KEY,
              'transit_mode': 'bus',
              'mode': 'transit'}

    r = requests.get(url=url, params=PARAMS)
    data = r.json()

    # check the status and existance of the google direction response
    if keys_exists(data, 'status') == False:
        logger.warning('Key status does not exist in google direction api response.')
        return data
    
    if data['status'] != 'OK':
        logger.warning('Status is not OK in google direction api response.')
        return data

    try:
        # count how many steps which travel model is TRANSIT
        transitCount = r.text.count("TRANSIT")

        if keys_exists(data, 'routes', 0, 'legs', 0) == False:
            logger.warning('Key legs does not exist in google direction api response.')
            return data

        leg = data['routes'][0]['legs'][0]

        if keys_exists(leg, 'steps') == False:
            logger.warning('Key steps does not exist in google direction api response.')
            return data

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
        # happen when steps including transit step
        if 'departure_time' in leg:
            newData['leg']['departure_time'] = leg['departure_time'].copy()
            newData['leg']['arrival_time'] = leg['departure_time'].copy()

        # happen when steps only has walking step
        else:
            # FIXME: timezone  & daylight saving problem
            # when convert unix to time string shows one hour late
            timestr = datetime.fromtimestamp(int(departureUnix)) \
                + timedelta(hours=1)
            timestr = timestr.strftime("%l:%M%p")
            timestr = timestr.replace('PM', 'pm').replace('AM', 'am')
            newData['leg']['departure_time'] = {'value': int(departureUnix),
                                                'text': timestr}
            newData['leg']['arrival_time'] = {'value': int(departureUnix),
                                              'text': timestr}
        
        totalDistance = 0
        transitStepCount = 0

        for index, step in enumerate(steps):

            isValiedForPrediction = True

            while isValiedForPrediction:

                # check if the step is transit and the line ML model is existed
                # ex: if the value of step is 39, than it is valid,
                # since the route_39.pkl is existed
                if not is_route_exist_for_prediction(step):
                    isValiedForPrediction = False
                    break
                
                lineId = step['transit_details']['line']['short_name']
                stops = get_stops(step, lineId)

                if stops == None:
                    isValiedForPrediction = False
                    logger.warning('get None stop fron getStop function.')
                    break
                
                if len(stops) < 2:
                    isValiedForPrediction = False
                    logger.warning('length stops less than 2')
                    break
                
                segments = get_segments(stops)
                if segments == None:
                    isValiedForPrediction = False
                    break
                
                # predict traveling time for all segmentid
                journeyTime = predict_journey_time(
                    lineId,
                    segments,
                    int(departureUnix))

                if journeyTime == None:
                    isValiedForPrediction = False
                    break

                # set duration to predicted journey time
                duration = int(journeyTime)

                arr_unix = newData['leg']['arrival_time']['value'] + duration
                timestr = datetime.fromtimestamp(arr_unix) + timedelta(hours=1)
                timestr = timestr.strftime('%l:%M%p')
                timestr = timestr.replace('PM', 'pm').replace('AM', 'am')
                step['transit_details']['arrival_time']['value'] = arr_unix
                step['transit_details']['arrival_time']['text'] = timestr
                step['transit_details']['stops'] = stops
                step['duration']['value'] = duration
                step['duration']['text'] = get_time_string(duration)
                newData['leg']['arrival_time']['value'] = arr_unix
                
                transitStepCount += 1
                break
            
            # Not valid / fail to get journey prediction
            if not isValiedForPrediction:
                duration = int(step['duration']['value'])
                newData['leg']['arrival_time']['value'] += duration

            distance = int(step['distance']['value'])
            newData['leg']['steps'].append(step)
            totalDistance += distance
            newData['leg']['end_location'] = step['end_location']

                
            # if there have more than one transit
            # break the for loop
            # set another google direction API requestion
            # to get the direction for rest of the journey
            if transitCount > 1 and transitStepCount >= 1:
                break

        totalDuration = newData['leg']['arrival_time']['value'] - newData['leg']['departure_time']['value']
        newData['leg']['duration']['value'] = totalDuration
        newData['leg']['distance']['value'] = totalDistance
        newData['leg']['duration']['text'] = get_time_string(totalDuration)
        newData['leg']['distance']['text'] = get_destination_string(totalDistance)

        # FIXME: timezone  & daylight saving problem
        # when convert unix to time string shows one hour late
        timestr = datetime.fromtimestamp(newData['leg']['arrival_time']['value']) + timedelta(hours=1)
        timestr = timestr.strftime('%l:%M%p')
        timestr = timestr.replace('PM', 'pm').replace('AM', 'am')
        newData['leg']['arrival_time']['text'] = timestr
        newData['status'] = 'OK'

        return newData

    except Exception as e:
        print("direction_to_first_transit error:", str(e))
        message = {'status': 'ZERO_RESULT'}
        return message



def keys_exists(element, *keys):
    _element = element
    for key in keys:
        try:
            _element = _element[key]
        except KeyError:
            return False
    return True



def is_route_exist_for_prediction(step):
    if step['travel_mode'] == 'TRANSIT':
        # get all ML models' name
        # only do the journey time prediction if the model of the line is existed
        lines = [modelName.replace('.pkl', '') for modelName in get_models_name()]
        
        try:
            lineId = step['transit_details']['line']['short_name'].upper()
            if ('route_'+lineId) in lines:
                return True
        except:
            return False
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
        return None

    if len(stops) > 0:
        return stops[0]
    return None


def get_segments(stops):

    if len(stops) >= 2:
        segments = []
        for index, stop in enumerate(stops, start=1):
            segments.append(stops[index-1]['plate_code'] + '-' + stop['plate_code'])
        return segments
    return None


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
