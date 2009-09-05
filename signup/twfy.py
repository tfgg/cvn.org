import urllib
import copy

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

def getConstituencies(date=None):
    p = copy.copy(params)
    if date:
        p.update({'date':date})
    params_encoded = urllib.urlencode(p)
    url = "%sgetConstituencies?%s" % (service_url, params_encoded)
    result = urllib.urlopen(url)
    ctype = result.headers['content-type']
    charset = ctype[ctype.find("charset=")+len("charset="):]
    
    return [x['name'].decode(charset) for x in eval(result.read())]
