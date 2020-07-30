from django.test import TestCase, Client
from django.urls import reverse
# from routeplanner.models
import json


class TestVews(TestCase):

    def setUp(self):
        self.client = Client()
        # self.home_url = reverse('routeplanner')
        # self.home_url = reverse('stops')
        # self.home_url = reverse('routes')
        # self.home_url = reverse('leapcard')

    # to test if each function each can use the correct template
    def test_home(self):
        response = self.client.get(reverse('routeplanner'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'routeplanner/home.html')

    def test_stops(self):
        response = self.client.get(reverse('stops'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'routeplanner/stops.html')

    def test_routes(self):
        response = self.client.get(reverse('routes'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'routeplanner/routes.html')

    def test_leapcard(self):
        response = self.client.get(reverse('leapcard'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'routeplanner/leapcard.html')

    # to test the post method of leapcard: should show a error message since username and password passed are invalid
    def test_leapcard_POST(self):
        url = reverse('leapcard')
        response = self.client.post(url, {
            'username': '123',
            'password': '456'
        })
