import math
import twfy
import json, urllib

def haversine((lat1, lon1), (lat2, lon2)):
    """
    Haversine distance between two points
    """
    R = 6371; # Earth's radius in km
    dLat = math.radians(lat2-lat1)
    dLon = math.radians(lon2-lon1)
    a = (math.sin(dLat/2) * math.sin(dLat/2) + math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) * math.sin(dLon/2) * math.sin(dLon/2) )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)); 
    return R * c


def center(data, c):
    "lat,lng of the center of a constituency"
    return (data[c]["centre_lat"], data[c]["centre_lon"])


def neighbors(constituency, limit=5, _data=None):
    """
    List of constituency's neighbors.

    constituency - name of the constituency you want the neighbors of
    limit - max number of neighbors to return
    _data - the data to use for calculations (used for testing)
    """
    if _data == None:
        _data = twfy.getGeometry()

    data = dict((k, v) for k,v in _data.iteritems()
                if v.has_key("centre_lon") and v.has_key("centre_lat"))

    clat, clng = center(data, constituency)
    dist_to = lambda c: haversine((clat, clng), center(data, c))
    distance = dict((c, dist_to(c)) for c in data)
    nearest = sorted((c for c in data), key=lambda c: distance[c])
    return nearest[1:limit+1]


# nicked from http://github.com/simonw/geocoders/
def geocode(q):
    data = json.load(urllib.urlopen(
        'http://ws.geonames.org/searchJSON?' + urllib.urlencode({
            'q': q,
            'maxRows': 1,
            'lang': 'en',
            'style': 'full'
        })
    ))
    if not data['geonames']:
        return None, (None, None)
    
    place = data['geonames'][0]
    name = place['name']
    if place['adminName1'] and place['name'] != place['adminName1']:
        name += ', ' + place['adminName1']
    return name, (place['lat'], place['lng'])


# XX copied from signup/forms.py
import re
POSTCODE_RE = re.compile(r'\b[A-PR-UWYZ][A-HK-Y0-9][A-HJKSTUW0-9]?[ABEHMNPRVWXY0-9]? {0,2}[0-9][ABD-HJLN-UW-Z]{2}\b',re.I)

def constituency(place):
    try:
        if POSTCODE_RE.match(place):
            return twfy.getConstituency(place)
        else:
            _, (lat, lng) = geocode(place)
            consts = twfy.getConstituencies(latitude=lat, longitude=lng, distance=10)
            if len(consts) > 0:
                return consts[0]
    except Exception:
        return None
    
