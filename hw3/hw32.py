###hw3(2)
###Name: Yihan Xu
###ID#: 47011405
###connect module

import json
import urllib.parse
import urllib.request

###put the parameter into a list of tuple and append the location 
def build_parameter(num_location, location_list):
    parameter = [('from', location_list[0])]
    
    for k in range(1, num_location):
        target_location = location_list[k]
        parameter.append(('to', target_location))
    
    return parameter

###get parameter add it to the base url/key
def build_url(parameter):
    Base_Url_route = 'http://open.mapquestapi.com/directions/v2/route?key=Fmjtd%7Cluu821u2nl%2Crl%3Do5-94ax5r&'
    Url_to_send = Base_Url_route + urllib.parse.urlencode(parameter)

    return Url_to_send


###get the json result, and check if there is connection error or no route found
def read_result(Url):
    try:
        result = urllib.request.urlopen(Url)

    except:
        print()
        print('MAPQUEST ERROR')
        return -1
    
    json_info = result.read().decode(encoding = 'utf-8')
    json_result = json.loads(json_info)

    if json_result['info']['statuscode'] == 400 or json_result['info']['statuscode'] == 500:
            print()
            print('NO ROUTE FOUND')
            return -1

    else:
        return json_result



###build url and get json result the same way as previous
def build_url_ele(latlng):
    Base_Url_ele = 'http://open.mapquestapi.com/elevation/v1/profile?key=Fmjtd%7Cluu821u2nl%2Crl%3Do5-94ax5r&shapeFormat=raw&unit=f&latLngCollection='
    Url_ele = Base_Url_ele + latlng
    
    try:
        result = urllib.request.urlopen(Url_ele)
    except:
        print()
        print('MAPQUEST ERROR')
        return -1

    
    json_info = result.read().decode(encoding = 'utf-8')
    json_result_ele = json.loads(json_info)
    
    return json_result_ele
