from django.test import TestCase, Client
from django.urls import reverse
# from routeplanner.models
import json

class TestViews(TestCase):
        def setUp(self):
        self.client = Client()

    #to test if each function each can use the correct template
    def test_stops(self):
        response1 = self.client.get(reverse('stops'))
        response2 = self.client.get(reverse('stops/nearby'))
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)


    def test_routes(self):
        response1 = self.client.get(reverse('routes'))
        response2 = self.client.get(reverse('routes/routename'))
        response3 = self.client.get(reverse('routes/variations, '))
        response4 = self.client.get(reverse('routes/stops'))
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response3.status_code, 200)
        self.assertEqual(response4.status_code, 200)



    def test_shapes(self):
        response = self.client.get(reverse('routes'))
        self.assertEqual(response.status_code, 200)


