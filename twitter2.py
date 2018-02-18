import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl
import folium
from geopy.geocoders import Nominatim

# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#Changes start here

print('')
acct = input('Enter Twitter Account:')
url = twurl.augment(TWITTER_URL,
                    {'screen_name': acct, 'count': '10'})
print('Retrieving', url)
connection = urllib.request.urlopen(url, context=ctx)
data = connection.read().decode()

js = json.loads(data)
#print(json.dumps(js, indent=2))

headers = dict(connection.getheaders())
print('Remaining', headers['x-rate-limit-remaining'])
names = []
locations = []
for u in js['users']:
    names.append((u['screen_name']))
    locations.append(u['location'])
    if 'status' not in u:
        #print('   * No status found')
        continue
    s = u['status']['text']
    #print('  ', s[:50])

for i in range(len(names)):
    print(names[i], "is at", locations[i])


def createmap(name, place):
    map = folium.Map(zoom_start=4, tiles="Mapbox bright")
    geolocator = Nominatim()

    feature_group = folium.FeatureGroup("Locations")

    for i in range(len(name)):
        if place[i] != "":
            location = geolocator.geocode(place[i])
            lat = location.latitude
            lng = location.longitude
            new = folium.Marker(location=[lat, lng], popup=name[i])
            feature_group.add_child(new)

    map.add_child(feature_group)
    map.save("Friends.html")

print(len(names), len(locations))
createmap(names, locations)
