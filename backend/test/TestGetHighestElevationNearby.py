"""
Created on 280415
Created by Phua Joon Kai Eugene
Last Modification on 050515
"""
from test.TestBase import BaseTestCase


class TestGetHeightResponse(BaseTestCase):
    def test_get_correct(self):
        response = self.client.get("/dtm/v1/highestelevationnearby?lat=48&lon=8&radius=400")
        self.assert200(response)

    def test_missing_lat(self):
        response = self.client.get("/dtm/v1/highestelevationnearby?lon=8&radius=400")
        self.assert400(response)

    def test_missing_lon(self):
        response = self.client.get("/dtm/v1/highestelevationnearby?lat=47&radius=400")
        self.assert400(response)

    def test_missing_radius(self):
        response = self.client.get("/dtm/v1/highestelevationnearby?lat=47&lon=8")
        self.assert400(response)

    def test_missing_all(self):
        response = self.client.get("/dtm/v1/highestelevationnearby")
        self.assert400(response)

    def test_response(self):
        response = self.client.get("/dtm/v1/highestelevationnearby?lat=48&lon=8&radius=10")
        self.assertEqual(response.data,'Radius must be in between 120 and 2100')


class TestGetHeightMain(BaseTestCase):
    def test_correct_geojson(self):
        response = self.client.get("/dtm/v1/highestelevationnearby?lat=48&lon=8&radius=400")
        geojson = [8.002057803644078, 47.99885289735797, 654]
        a = response.json['geometry']['coordinates']
        self.assertEqual(response.json['geometry']['coordinates'], geojson)
        self.assertEqual(response.json['geometry']['type'], 'Point')

    def test_radius_less(self):
        response = self.client.get("/dtm/v1/highestelevationnearby?lat=48&lon=8&radius=10")
        self.assertEqual(response.data,'Radius must be in between 120 and 2100')

    def test_radius_more(self):
        response = self.client.get("/dtm/v1/highestelevationnearby?lat=48&lon=8&radius=2200")
        self.assertEqual(response.data,'Radius must be in between 120 and 2100')