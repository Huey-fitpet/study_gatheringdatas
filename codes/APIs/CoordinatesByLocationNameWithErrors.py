

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

    def send_api(base_url, params, keys = None):
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
        

if __name__ in '__main__':
    
    city_list = ['도쿄','괌','모나코']
    # run(city_list)
    # send_api(base_url, params, keys = None):
    
    key_list = ['lat', 'lon']
    pub_key = '39fb7b1c6d4e11e7483aabcb737ce7b0'
    for city in city_list:
        base_url = f'https://api.openweathermap.org/geo/1.0/direct'
        
        params={}
        params['q'] = city
        params['appid'] = pub_key

        result_geo = ApiRequester.send_api(base_url, params, key_list)

        base_url = f'https://pro.openweathermap.org/data/2.5/weather'
        
        params_w = {}
        for geo in result_geo:
            for key in key_list:
                params_w[key] = geo[key]
        params_w['appid'] = pub_key
        result_cont = ApiRequester.send_api(base_url, params_w)

        print(result_cont)


    pass