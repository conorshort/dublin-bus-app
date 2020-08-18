from django.test import TestCase
from api.models import GTFSAgency, GTFSCalendar, GTFSCalendarDate, GTFSRoute, GTFSShape, GTFSStop, GTFSStopTime, GTFSTrip, SmartDublinBusStop
from datetime import datetime, date
import pytest
import factory

pytestmark = pytest.mark.django_db

agency_dict = {"name": "Dublin Bus",
               "id": "978",
               "path": "api/files/dublin_bus_gtfs/"}


class GTFSAgencyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GTFSAgency
    agency_id = "978"
    agency_name = "Dublin Bus"
    agency_url = "https://www.transportforireland.ie"
    agency_timezone = "Europe/Dublin"
    agency_lang = "EN"


class GTFSCalendarFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GTFSCalendar
    agency = factory.SubFactory(GTFSAgencyFactory)
    service_id = "1"
    agency_service_id = "978_1"
    monday = "1"
    tuesday = "0"
    wednesday = "0"
    thursday = "0"
    friday = "0"
    saturday = "0"
    sunday = "0"
    start_date = datetime.strptime(
        "20200608", "%Y%m%d")
    end_date = datetime.strptime(
        "20200808", "%Y%m%d")
    display_days = "Mon"


class GTFSCalendarDateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GTFSCalendarDate
    calendar = factory.SubFactory(GTFSCalendarFactory)
    service_id = 1
    date = datetime.strptime(
        "20200803", "%Y%m%d")
    exception_type = 2
    unique_calendar_date_id = "978_1_20200803"


class GTFSRouteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GTFSRoute
    route_id="60-1-b12-1"
    route_name="1"
    agency=factory.SubFactory(GTFSAgencyFactory)


class GTFSShapeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GTFSShape
    unique_point_id="60-1-b12-1.1.O:1"
    shape_id="60-1-b12-1.1.O"
    shape_pt_lat=53.3911764950851
    shape_pt_lon=-6.26219900048751
    shape_pt_sequence=1

    @classmethod
    def make_shape_sequence(cls):
        for i in range(1,100):
            cls.build(unique_point_id=f"60-1-b12-1.1.O:{i}",
                      shape_id="60-1-b12-1.1.O",
                      shape_pt_lat=(53 + (i / 100)),
                      shape_pt_lon=(-6 + (i / 100)),
                      shape_pt_sequence=i).save()


class GTFSTripFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GTFSTrip
    route=factory.SubFactory(GTFSRouteFactory)
    calendar=factory.SubFactory(GTFSCalendarFactory)
    trip_id="1.2.60-1-b12-1.1.O"
    shape_id="60-1-b12-1.1.O"
    trip_headsign="Shanard Road(Shanard Avenue) - Saint John's Road East"
    direction_id=0

    @classmethod
    def make_trips(cls):
        for i in range(1, 10):
            cls.build(trip_id=f"{i}.2.60-1-b12-1.1.O",
                      direction_id=0).save()


class GTFSStopFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GTFSStop
    stop_id="AB123"
    stop_name="Nowhere land"
    plate_code="123"
    stop_lat=53
    stop_lon=-6

    @classmethod
    def make_stops(cls):
        for i in range(1,100):
            cls.build(stop_id=f"AB{i}",
                      stop_name=f"Place {i}",
                      plate_code=(1000 + i),
                      stop_lat=(53 + i/10),
                      stop_lon=-(6 + i/10)
            ).save()


class GTFSStopTimeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GTFSStopTime
    unique_trip_id="1.2.60-1-b12-1.1.O:1"
    trip_id="1.2.60-1-b12-1.1.O"
    arrival_time = 28500
    departure_time=28500
    stop=factory.SubFactory(GTFSStopFactory)
    stop_sequence=1
    stop_headsign="Saint John's Road"

    @classmethod
    def make_stop_times(cls):
        for i in range(1,10):
            for j in range(1, 100):
                cls.build(unique_trip_id=f"{i}.2.60-1-b12-1.1.O:{j}",
                          trip_id=f"{i}.2.60-1-b12-1.1.O",
                        arrival_time=(28500 + (j * 100)),
                        departure_time=(28500 + (j * 100)),
                          stop_id=f"AB{j}",
                        stop_sequence=j,
                        stop_headsign="Saint John's Road"
                        ).save()

class SmartDublinBusStopFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SmartDublinBusStop
    stopid = 123
    shortnamelocalized = "Áit 1"
    fullname = "Place 1"
    latitude = 53
    longitude = -6
    lastupdated = datetime.strptime(
        "20200603", "%Y%m%d")
    routes = ["1","2","3","4"]
    localname = "Street 1"

    @classmethod
    def make_stops(cls):
        for i in range(1, 100):
            cls.build(stopid=(1000 + i),
                      shortnamelocalized=f"Áit {i}",
                      fullname=f"Place {i}",
                      latitude=(53 + i/10),
                      longitude=-(6 + i/10),
                      localname=f"Street {i}"
                      ).save()







class GTFSAgencyTest(TestCase):
    """ Test module for GTFSAgency """

    def setUp(self):
        GTFSAgencyFactory.build().save()


    def test_name_and_id(self):
        agency_978 = GTFSAgency.objects.get(agency_id='978')
        self.assertEqual(
            agency_978.agency_name, "Dublin Bus")

    def test_from_dict(self):
        agency = {"agency_id": "3",
            "agency_name": "Go-Ahead",
            "agency_url": "https://www.transportforireland.ie",
            "agency_timezone": "Europe/Dublin",
            "agency_lang": "EN"}
        GTFSAgency.from_dict(agency, agency_dict).save()
        agency_GA = GTFSAgency.objects.get(agency_name='Go-Ahead')
        self.assertEqual(
            agency_GA.agency_id, "3")

class GTFSCalendarTest(TestCase):
    """ Test module for GTFSCalendar """

    def setUp(self):
        GTFSAgencyFactory.build().save()
        GTFSCalendarFactory.build().save()



    def test_agency_service_id(self):
        calendar_978 = GTFSCalendar.objects.get(agency_service_id='978_1')
        self.assertEqual(
            calendar_978.agency.agency_name, "Dublin Bus")


    def test_from_dict(self):
        calendar = {"agency": "978",
            "service_id": "3",
            "monday": "0",
            "tuesday": "0",
            "wednesday": "0",
            "thursday": "0",
            "friday": "0",
            "saturday": "0",
            "sunday": "1",
            "start_date": "20200608",
            "end_date": "20200808",
            "display_days": "Sun"}

        GTFSCalendar.from_dict(calendar, agency_dict).save()
        calendar_03 = GTFSCalendar.objects.get(agency_service_id='978_3')
        self.assertEqual(calendar_03.service_id, "3")


    def test_date(self):
        calendar_978=GTFSCalendar.objects.get(
                    agency_service_id = '978_1')

        self.assertEqual(
            calendar_978.start_date, date(2020, 6, 8))
        self.assertEqual(
            calendar_978.end_date, date(2020, 8, 8))









class GTFSCalendarDateTest(TestCase):
    """ Test module for GTFSCalendarDate """

    def setUp(self):
        GTFSAgencyFactory.build().save()
        GTFSCalendarFactory.build().save()
        GTFSCalendarDateFactory.build().save()

    def test_from_dict(self):
        cd_dict={
            "service_id":1,
            "date":"20201212",
            "exception_type":2
            }
        GTFSCalendarDate.from_dict(cd_dict, agency_dict).save()
        cd = GTFSCalendarDate.objects.get(
            unique_calendar_date_id='978_1_20201212')
        self.assertEqual(
            cd.date, date(2020, 12,12))

    def test_date(self):
        calendardate_978 = GTFSCalendarDate.objects.get(
            unique_calendar_date_id='978_1_20200803')

        self.assertEqual(
            calendardate_978.date, date(2020, 8, 3))

    def test_calendar(self):
        calendardate_978 = GTFSCalendarDate.objects.get(
            unique_calendar_date_id='978_1_20200803')

        self.assertEqual(
            calendardate_978.calendar.agency_service_id, "978_1")








class GTFSRouteTest(TestCase):
    """ Test module for GTFSRoute """

    def setUp(self):
        GTFSAgencyFactory.build().save()
        GTFSRouteFactory.build().save()

    def test_from_dict(self):
        route_dict = {"route_id": "60-999-b12-1",
                      "agency_id": 978, "route_short_name": "999"}
        GTFSRoute.from_dict(route_dict, agency_dict).save()
        route = GTFSRoute.objects.get(
            route_id="60-999-b12-1")
        self.assertEqual(
            route.agency.agency_id, "978")
        self.assertEqual(
            route.route_name, "999")

    def test_route(self):
        route_1 = GTFSRoute.objects.get(
            route_id='60-1-b12-1')
        self.assertEqual(
            route_1.route_name, "1")









class GTFSShapeTest(TestCase):
    """ Test module for GTFSShape """
    def setUp(self):
        GTFSAgencyFactory.build().save()
        GTFSRouteFactory.build().save()
        GTFSShapeFactory.make_shape_sequence()

    def test_from_dict(self):
        shape_dict = {"shape_id":"60-999-d12-1.61.O",
                    "shape_pt_lat":99.999,
                    "shape_pt_lon":-6.6666,
                    "shape_pt_sequence":999,
                    "shape_dist_traveled":999.99}

        GTFSShape.from_dict(shape_dict, agency_dict).save()
        shape = GTFSShape.objects.get(
            shape_id='60-999-d12-1.61.O')
        self.assertEqual(
            shape.unique_point_id, "60-999-d12-1.61.O:999")


    def test_shape(self):
        shape = GTFSShape.objects.get(unique_point_id="60-1-b12-1.1.O:5")
        self.assertEqual(shape.shape_pt_lat, 53.05)
        self.assertEqual(shape.shape_pt_sequence, 5)

    def test_get_points_by_id(self):
        points = GTFSShape.objects.get_points_by_id("60-1-b12-1.1.O")
        self.assertEqual(points[0], [-5.99, 53.01])
        self.assertEqual(points[-1], [-5.01, 53.99])







class GTFSStopTest(TestCase):
    """ Test module for GTFSStop """

    def setUp(self):
        GTFSStopFactory.build().save()
    
    def test_stop(self):
        stop = GTFSStop.objects.get(stop_id="AB123")
        self.assertEqual(stop.plate_code, "123")
        self.assertEqual(stop.stop_lat, 53)

    def test_from_dict(self):
        stop_dict = {"stop_id":"ABCDEFGHIJK",
                    "stop_name":"Dict test stop, stop 9999",
                    "stop_lat":-6.6666,
                    "stop_lon":999}

        GTFSStop.from_dict(stop_dict, agency_dict).save()
        stop = GTFSStop.objects.get(
            stop_id='ABCDEFGHIJK')
        self.assertEqual(
            stop.plate_code, "9999")
        self.assertEqual(
            stop.stop_name, "Dict test stop")


class GTFSStopTimeTest(TestCase):
    """ Test module for GTFSStopTime """

    def setUp(self):
        GTFSAgencyFactory.build().save()
        GTFSCalendarFactory.build().save()
        GTFSRouteFactory.build().save()
        GTFSTripFactory.make_trips()
        GTFSStopFactory.make_stops()
        GTFSStopTimeFactory.make_stop_times()

    def test_stop_time(self):
        stoptime_1 = GTFSStopTime.objects.get(
            unique_trip_id="1.2.60-1-b12-1.1.O:1")
        stoptime_2 = GTFSStopTime.objects.get(
            unique_trip_id="5.2.60-1-b12-1.1.O:50")
        self.assertEqual(stoptime_1.arrival_time, 28600)
        self.assertEqual(stoptime_2.stop_sequence, 50)


    def test_from_dict(self):
        stop_time_dict = {"trip_id":"1.2.60-1-b12-1.1.O",
                    "arrival_time":"09:59:59",
                    "departure_time": "09:59:59",
                    "stop_id":"AB1",
                    "stop_sequence":999,
                    "stop_headsign":"Dict test headsign"}

        GTFSStopTime.from_dict(stop_time_dict, agency_dict).save()
        stop_time = GTFSStopTime.objects.get(
            unique_trip_id='1.2.60-1-b12-1.1.O:999')
        self.assertEqual(
            stop_time.stop_id, "AB1")
        self.assertEqual(
            stop_time.arrival_time, 35999)


class GTFSTripTest(TestCase):
    """ Test module for GTFSTrip """

    def setUp(self):
        GTFSAgencyFactory.build().save()
        GTFSCalendarFactory.build().save()
        GTFSRouteFactory.build().save()
        GTFSTripFactory.make_trips()
        GTFSStopFactory.make_stops()
        GTFSStopTimeFactory.make_stop_times()

    def test_stops_on_route(self):
        stops = GTFSTrip.objects.stops_on_route("60-1-b12-1.1.O")
        self.assertEqual(len(stops), 99)
        self.assertEqual(stops[0].arrival_time, 28600)
        self.assertEqual(stops[98].arrival_time, 38400)

    def test_get_stops_between(self):
        stops = GTFSTrip.objects.get_stops_between(1005, 1010, "1", origin_time=29000, headsign="Saint John's Road")
        self.assertEqual(len(stops), 1)
        self.assertEqual(len(stops[0]), 6)
        self.assertEqual(stops[0][0]["stop_name"], "Place 5")
        self.assertEqual(stops[0][1]["stop_name"], "Place 6")
        self.assertEqual(stops[0][2]["stop_name"], "Place 7")

    def test_from_dict(self):
        stop_time_dict = {"route_id":"60-1-b12-1",
                    "service_id":"1",
                    "trip_id":"test_trip",
                    "shape_id":"test_shape",
                    "trip_headsign":"Dict test headsign",
                    "direction_id":0}

        GTFSTrip.from_dict(stop_time_dict, agency_dict).save()
        trip = GTFSTrip.objects.get(
            trip_id='test_trip')
        self.assertEqual(
            trip.route.route_name, "1")
        self.assertEqual(
            trip.calendar.service_id, "1")


class SmartDublinBusStopTest(TestCase):
    """ Test module for SmartDublinBusStop """

    def setUp(self):
        SmartDublinBusStopFactory.make_stops()

    def test_get_nearest_id(self):
        stop_id = SmartDublinBusStop.objects.get_nearest_id(51.005, -6.005)
        self.assertEqual(stop_id, 1001)
    
