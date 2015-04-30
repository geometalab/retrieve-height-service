'''
Created on 30 April 2015
Created by Eugene Phua
'''

from test.TestBase import BaseTestCase
import unittest

class TestGetHeightResponse(BaseTestCase):
    def test_get_correct_height(self):
        response = self.client.get("/dtm/v1/elevation?lat=47&lon=8&format=geojson")
        self.assert200(response)

    def test_missing_format(self):
        response = self.client.get("/dtm/v1/elevation?lat=47&lon=8")
        self.assert200(response)

    def test_missing_lat(self):
        response = self.client.get("/dtm/v1/elevation?lat=47")
        self.assert400(response)

    def test_missing_lat_format(self):
        response = self.client.get("/dtm/v1/elevation?lat=47&format='geojson'")
        self.assert400(response)

    def test_missing_lon(self):
        response = self.client.get("/dtm/v1/elevation?lon=8")
        self.assert400(response)

    def test_missing_lon_format(self):
        response = self.client.get("/dtm/v1/elevation?lon=8&format='geojson'")
        self.assert400(response)

    def test_missing_all(self):
        response = self.client.get("/dtm/v1/elevation")
        self.assert400(response)

class TestGetHeightMain(BaseTestCase):
    def test_correct_raw(self):
        response = self.client.get("/dtm/v1/elevation?lat=47&lon=8&format=raw")
        raw = [8.0, 47.0, 919]
        self.assertEqual(response.json, raw)

    def test_correct_json(self):
        response = self.client.get("/dtm/v1/elevation?lat=47&lon=8&format=json")
        json = [8.0, 47.0, 919]
        self.assertEqual(response.json['coordinates'], json)

    def test_correct_geojson(self):
        response = self.client.get("/dtm/v1/elevation?lat=47&lon=8&format=geojson")
        geojson = [8.0, 47.0, 919]
        self.assertEqual(response.json['coordinates'], geojson)
        self.assertEqual(response.json['type'], 'Point')

    def test_default_geojson(self):
        response = self.client.get("/dtm/v1/elevation?lat=47&lon=8")
        geojson = [8.0, 47.0, 919]
        self.assertEqual(response.json['coordinates'], geojson)
        self.assertEqual(response.json['type'], 'Point')

    def test_different_order(self):
        response = self.client.get("/dtm/v1/elevation?format=json&lon=8&lat=47")
        json = [8.0, 47.0, 919]
        self.assertEqual(response.json['coordinates'], json)
