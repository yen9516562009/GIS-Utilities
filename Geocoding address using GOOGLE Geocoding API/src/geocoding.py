# -*- coding: utf-8 -*-
"""
Geocoding address using GOOGLE Geocoding API
- return address centroids

@author: Jeff Yen
"""

import requests

# Use GOOGLE Geocoding API
API_KEY = 'YOUR_API_KEY'
base_url = 'https://maps.googleapis.com/maps/api/geocode/json'

def geocoding(address):
    endpoint = f"{base_url}?address={address}&key={API_KEY}"
    resultDF = requests.get(endpoint).json()['results'][0]
    lat = resultDF['geometry']['location']['lat']
    lng = resultDF['geometry']['location']['lng']
    centroid = [address, lat, lng]
    
    return centroid