###hw3(3)
###Name: Yihan Xu
###ID#: 47011405
###class_module

import json
import urllib.parse
import urllib.request
import hw32

###to find the class by go through all the narrative which is the value of maneuvers
class STEPS:
    def transfer(self, json_result):
        print()
        print('DIRECTIONS')
        for msg in json_result['route']['legs']:
            for sub_msg in msg['maneuvers']:
                print(sub_msg['narrative'])

                
###get the totaldistance by get the value from json_result which is the value
###of distance and round to integer
class TOTALDISTANCE:
    def transfer(self, json_result):
        print()
        DISTANCE = round(json_result['route']['distance'])
        print('TOTALDISTANCE: ' + str(DISTANCE) + ' ' + 'miles')
            
            
###get the totaltime which is the value of time and round it to a integer    
class TOTALTIME:
    def transfer(self, json_result):
        print()
        TIME = str(int(round(json_result['route']['time']) / 60))
        print('TOTALTIME: ' + TIME + ' ' + 'minutes')
        
###get the latlong which is the value of locations in route, and check the
###positive and negative to make sure it is west or east, south or north
class LATLONG:
    def transfer(self, json_result):
        print()
        print('LATLONG')
        LATLNG = ''
        for msg in json_result['route']['locations']:
            if msg['latLng']['lat'] > 0 and msg['latLng']['lng'] > 0:
                LATLNG = LATLNG + '\n' + '%.2f'%(msg['latLng']['lat']) + 'N' + ' ' + '%.2f'%(msg['latLng']['lng']) + 'E'
            if msg['latLng']['lat'] < 0 and msg['latLng']['lng'] < 0:
                LATLNG = LATLNG + '\n' + '%.2f'%(-msg['latLng']['lat']) + 'S' + ' ' + '%.2f'%(-msg['latLng']['lng']) + 'W'
            if msg['latLng']['lat'] < 0 and msg['latLng']['lng'] > 0:
                LATLNG = LATLNG + '\n' + '%.2f'%(-msg['latLng']['lat']) + 'S' + ' ' + '%.2f'%(msg['latLng']['lng']) + 'E'
            if msg['latLng']['lat'] > 0 and msg['latLng']['lng'] < 0:
                LATLNG = LATLNG + '\n' + '%.2f'%(msg['latLng']['lat']) + 'N' + ' ' + '%.2f'%(-msg['latLng']['lng']) + 'W'
                                
        print(LATLNG[1:])

            
###get the elevation by another url and get the value in height        
class ELEVATION:
    def transfer(self, json_result):
        print()
        print('ELEVATIONS')
        for msg2 in json_result['route']['locations']:
            latlng = str(msg2['latLng']['lat']) + ',' + str(msg2['latLng']['lng'])
            json_result_ele = hw32.build_url_ele(latlng)
            if json_result_ele == -1:
                return
            
            height = json_result_ele['elevationProfile'][0]
            print('%.0f'%(height['height']))
        
        
