import urllib
import copy
import json

api_key = "FH8qJGE5t7opGVTuXTDumuUK"
service_url = "http://www.theyworkforyou.com/api/"

params = {'key': api_key,
          'output': 'js'}

def getConstituency(postcode):
    p = copy.copy(params)
    p.update({'postcode':postcode})
    params_encoded = urllib.urlencode(p)
    url = "%sgetConstituency?%s" % (service_url, params_encoded)
    result = eval(urllib.urlopen(url).read())
    if not result.has_key('error'):
        return result['name']
    else:
        return None

def getConstituencies(**kw):
    geoargs = ("latitude", "longitude", "distance")
    validargs = ("date", ) + geoargs

    invalid_args = list(k for k in kw.keys() if k not in validargs)
    if len(invalid_args) > 0:
        raise ValueError("Invalid args %r" % ",".join(invalid_args))

    if any(kw.has_key(k) for k in geoargs):
        if not all(kw.has_key(k) for k in geoargs):
            raise ValueError("Need all geoargs")
    p = copy.copy(params)
    p.update((k, v) for k,v in kw.items() if v != None)
    params_encoded = urllib.urlencode(p)
    url = "%sgetConstituencies?%s" % (service_url, params_encoded)
    result = urllib.urlopen(url)
    ctype = result.headers['content-type']
    charset = ctype[ctype.find("charset=")+len("charset="):]
    
    return [x['name'].decode(charset) for x in eval(result.read())]

def getGeometry(name=None):
    """
    Centre and bounding box of constituencies

    Don't provide any argument to get all constituencies
    """
    p = copy.copy(params)
    if name:
        p.update({'name':name})
    params_encoded = urllib.urlencode(p)
    url = "%sgetGeometry?%s" % (service_url, params_encoded)
    result = urllib.urlopen(url)
    ctype = result.headers['content-type']
    charset = ctype[ctype.find("charset=")+len("charset="):]
    return json.load(result, encoding=charset)["data"]
    
