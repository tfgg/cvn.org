import urllib
import copy

from utils import json

api_key = "FH8qJGE5t7opGVTuXTDumuUK"
service_url = "http://www.theyworkforyou.com/api/"

params = {'key': api_key,
          'output': 'js'}


from django.core.cache import cache

class Fetcher(object):
    "Fetches urls and caches the result"
    def __call__(self, url):
        chit = cache.get(url)
        if chit:
            return chit
        else:
            resp = urllib.urlopen(url)
            cval = resp.headers, resp.read()
            cache.set(url, cval)
            return cval

fetch = Fetcher()


def charset(headers):
    "charset of content"
    ctype = headers['content-type']
    return ctype[ctype.find("charset=")+len("charset="):]

def svcurl(method, sparams):
    """
    Return the twfy api url for a method
    """
    p = params.copy()
    p.update(sparams)
    return service_url + method + "?" + urllib.urlencode(p)




def getConstituency(postcode):
    "Constituency postcode is in"
    _, response = fetch(svcurl("getConstituency", {"postcode": postcode}))
    result = json.loads(response)
    if not result.has_key('error'):
        return result['name']
    else:
        return None


def getConstituencies(**kw):
    """
    A list of constituencies

    args - either:
      date - the list of constituencies as it was on this date

    or:
      latitude, longitude, distance - list of constituencies
                                 within distance of lat, lng
    """
    geoargs = ("latitude", "longitude", "distance")
    validargs = ("date", ) + geoargs

    invalid_args = list(k for k in kw.keys() if k not in validargs)
    if len(invalid_args) > 0:
        raise ValueError("Invalid args %r" % ",".join(invalid_args))

    if any(kw.has_key(k) for k in geoargs):
        if not all(kw.has_key(k) for k in geoargs):
            raise ValueError("Need all geoargs")

    params = dict((k, v) for k,v in kw.items() if v != None)
    headers, result = fetch(svcurl("getConstituencies", params))
    return [x['name'].decode(charset(headers)) for x in json.loads(result)]


def getGeometry(name=None):
    """
    Centre and bounding box of constituencies

    Don't provide any argument to get all constituencies
    """
    if name:
        params = dict(name=name)
    else:
        params = dict()

    headers, result = fetch(svcurl("getGeometry", params))
    data = json.loads(result, encoding=charset(headers))["data"]
    return data

