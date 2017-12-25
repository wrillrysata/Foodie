import json
import httplib2
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import codecs
import json
import httplib2

app = Flask(__name__)
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "GCQZ0YREZOBQUMWO54DCJTBC33WPB4AR2N0L30ZVO5ZHC5GD"
foursquare_client_secret = "VVZIKOHDH0RIEPXBXZPYEYPWBC3ETZISHDXX3ILEU2R5DQP1"

google_api_key = "AIzaSyD_jewOWtrJj-qlqjyomIORxNAriILA-d8"


def getGeocodeLocation(inputString):
    # Replace Spaces with '+' in URL
    locationString = inputString.replace(" ", "+")
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' % (locationString, google_api_key))
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # print response
    latitude = result['results'][0]['geometry']['location']['lat']
    longitude = result['results'][0]['geometry']['location']['lng']
    return (latitude, longitude)


def findARestaurant(mealType, location):
    latitude, longitude = getGeocodeLocation(location)
    url = ('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20130815&ll=%s,%s&query=%s' % (
    foursquare_client_id, foursquare_client_secret, latitude, longitude, mealType))
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result['response'].get('venues'):
        # Grab the first restaurant
        restaurant = result['response']['venues'][0]
        venue_id = restaurant['id']
        restaurant_name = restaurant['name']
        restaurant_address = restaurant['location']['formattedAddress']
        # print restaurant_name
        # print restaurant_address
        # Format the Restaurant Address into one string
        address = ""
        for i in restaurant_address:
            address += i + " "
        restaurant_address = address

        # Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
        url = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&v=20150603&client_secret=%s' % (
        (venue_id, foursquare_client_id, foursquare_client_secret)))
        result = json.loads(h.request(url, 'GET')[1])
        # Grab the first image
        # if no image available, insert default image url
        if result['response']['photos']['items']:
            firstpic = result['response']['photos']['items'][0]
            prefix = firstpic['prefix']
            suffix = firstpic['suffix']
            imageURL = prefix + "300x300" + suffix
        else:
            imageURL = "http://pixabay.com/get/8926af5eb597ca51ca4c/1433440765/cheeseburger-34314_1280.png?direct"
        
        restaurantInfo = {'name': restaurant_name, 'address': restaurant_address, 'image': imageURL}
        return restaurantInfo
    else:
        # print "No Restaurants Found for %s" % location
        return "No Restaurants Found"


if __name__ == '__main__':
    findARestaurant("Pizza", "Lagos, Nigeria")
    findARestaurant("Pizza", "Tokyo, Japan")


