
from CoordinatesByLocationNameWithErrors import CoordiantesByLocationName as cn
from CoordinatesByLocationNameWithErrors import ApiRequester as ar
import requests
#uri 소스에서 넣을 때 길이가 256자 이내로 

'''
https://api.openweathermap.org/geo/1.0/direct?q=seoul&appid=39fb7b1c6d4e11e7483aabcb737ce7b0

https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}
"lat":37.5666791,"lon":126.9782914,
날씨 정보 수집(대상:도쿄, 괌, 모나코)

class ApiRequester:

    def send_api(base_url, params, keys = None):
'''

def run(city_list):

    for city_name in city_list:
        ret_dict = cn.nametogeocoordinates(city_name)
        uri = f'https://pro.openweathermap.org/data/2.5/weather'
        params ={
            'lat' : ret_dict['lat'], 
            'lon' : ret_dict['lon'], 
            'appid' : '39fb7b1c6d4e11e7483aabcb737ce7b0'
            }

        response = requests.get(uri, params=params)
        print(response.status_code)
        if response.status_code == 200 :
            if response.text !='[]' :
                import json
                content = json.loads(response.content)

                # mongoDB 저장
                from pymongo import MongoClient
                # mongodb에 접속 -> 자원에 대한 class
                mongoClient = MongoClient("mongodb://python_selenium_drive_mongo-db_mongodb_7-1:27017")
                # database 연결
                database = mongoClient["study_finance"]
                # collection 작업
                collection = database["coordinatesbylocationname"]

                # result = collection.insert_many([content])
                # print(result.inserted_ids)

                result = collection.insert_one(content)
                print(result.inserted_id)

                pass
            else :
                print(f"error : result empty {response.content}")
        else :
            print(f"error : {response.status_code}")

def main():
    city_list = ['도쿄','괌','모나코']
    # run(city_list)
    # send_api(base_url, params, keys = None):
    base_url = f'https://api.openweathermap.org/geo/1.0/direct'

        # params ={
        #     'q' : '도쿄', 
        #     'appid' : '39fb7b1c6d4e11e7483aabcb737ce7b0'
        #     }
    key_list = ['lat','lon']
    openweather = ar('39fb7b1c6d4e11e7483aabcb737ce7b0')
    for city in city_list:
        params ={
            'q' : city
        }
        temp = openweather.send_api(base_url, params, key_list)
    pass

if __name__ == '__main__':
    main()
    pass