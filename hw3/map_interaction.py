import urllib.parse
import urllib.request
import json

baseurl= 'http://open.mapquestapi.com/directions/v2/route?key=Fmjtd%7Cluu821uan5%2C70%3Do5-94aa14&'

def get_parameter()-> 'parameter':
    parameter=[('from','W.PELTASON DR'),
               ('to','E.PELTASON DR'),
               ('unit','m'),
        ('mapState','mapLat')]
    
    return parameter

def get_url(parameter)->'jsonresponse':
    search_query=urllib.parse.urlencode(parameter)
    querytosend=baseurl+search_query
    return querytosend

def get_json_result(querytosend)->'jsonresult':
    response=urllib.request.urlopen(querytosend)
    json_text=response.read().decode(encoding='utf-8')
    json_result=json.loads(json_text)
    return json_result
  
def main():
    
    parameter=get_parameter()
    querytosend=get_url(parameter)
    json_result=get_json_result(querytosend)
    #print(querytosend)
    for i in json_result['route']['legs']:
        for j in i['maneuvers']:
            print(j['narrative'])

                else:
        for msg in results['route']['legs']:
            for sub_msg in msg['maneuvers']:
                print(sub_msg['narrative'])
   
main()
