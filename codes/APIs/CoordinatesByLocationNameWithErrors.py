

import requests
#uri 소스에서 넣을 때 길이가 256자 이내로 

'''
https://api.openweathermap.org/geo/1.0/direct?q=seoul&appid=39fb7b1c6d4e11e7483aabcb737ce7b0

http://api.openweathermap.org/geo/1.0/direct?q={city name}&appid={API key}
'''
import json
class CoordiantesByLocationName:

    def nametogeocoordinates(cityname = None) :
        uri = f'https://api.openweathermap.org/geo/1.0/direct'
        params ={
            'q' : cityname, 
            'appid' : '39fb7b1c6d4e11e7483aabcb737ce7b0'
            }

        response = requests.get(uri, params=params)
        print(response.status_code)
        if response.status_code == 200 :
            if response.text !='[]' :
                content = json.loads(response.content)

                return {'lat' : int(content[0]['lat']), 'lon' : int(content[0]['lon'])}
                pass
            else :
                print(f"error : result empty {response.content}")
                return None
        else :
            print(f"error : {response.status_code}")
            return None


class ApiRequester:

    service_key = f''

    def __init__(self, service_key) -> None:
        self.service_key = service_key


    def make_prams(self, params) :
        params['appid'] = self.service_key
        return params
    
    
    def send_api(self, base_url, params, keys = None):
        params = self.make_prams(params)
        response = requests.get(base_url, params=params)
        print(response.status_code)
        if response.status_code == 200 :
            if response.text !='[]' :
                content = json.loads(response.content)

                if keys == None :
                    return content
                else :
                    ############################# 
                    result_list = []

                    # content가 리스트가 아닐 경우, 단일 항목을 처리
                    if not isinstance(content, list):
                        content = [content]  # 단일 항목을 리스트로 변환

                    # 모든 항목에 대해 키를 사용하여 ret_contents 생성
                    for con in content:
                        item_dict = {key: con[key] for key in keys}
                        result_list.append(item_dict)

                    return result_list
                # return {'lat' : int(content[0]['lat']), 'lon' : int(content[0]['lon'])}
                
            else :
                print(f"error : result empty {response.content}")
                return None
        else :
            print(f"error : {response.status_code}")
            return None       
        pass

    def nametogeocoordinates(cityname = None) :
        uri = f'https://api.openweathermap.org/geo/1.0/direct'
        params ={
            'q' : cityname, 
            'appid' : '39fb7b1c6d4e11e7483aabcb737ce7b0'
            }

        response = requests.get(uri, params=params)
        print(response.status_code)
        if response.status_code == 200 :
            if response.text !='[]' :
                content = json.loads(response.content)

                return {'lat' : int(content[0]['lat']), 'lon' : int(content[0]['lon'])}
                pass
            else :
                print(f"error : result empty {response.content}")
                return None
        else :
            print(f"error : {response.status_code}")
            return None       