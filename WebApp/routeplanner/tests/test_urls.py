from django.test import SimpleTestCase
from django.urls import reverse, resolve
from routeplanner.views import home, stops, routes, leapcard


class TestUrls(SimpleTestCase):

    def test_routeplanner_url_is_resolved(self):
        url = reverse('routeplanner')
        self.assertEquals(resolve(url).func, home)

    def test_stops_url_resolves(self):
        url = reverse('stops')
        self.assertEquals(resolve(url).func, stops)

    def test_routes_url_resolves(self):
        url = reverse('routes')
        self.assertEquals(resolve(url).func, routes)

    def test_leapcard_url_resolves(self):
        url = reverse('leapcard')
        self.assertEquals(resolve(url).func, leapcard)