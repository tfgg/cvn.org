import math
import twfy


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
