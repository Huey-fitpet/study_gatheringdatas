

import requests
#uri 소스에서 넣을 때 길이가 256자 이내로 

'''
https://api.openweathermap.org/geo/1.0/direct?q=seoul&appid=39fb7b1c6d4e11e7483aabcb737ce7b0

http://api.openweathermap.org/geo/1.0/direct?q={city name}&appid={API key}
'''

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
                import json
                content = json.loads(response.content)

                # # mongoDB 저장
                # from pymongo import MongoClient
                # # mongodb에 접속 -> 자원에 대한 class
                # mongoClient = MongoClient("mongodb://python_selenium_drive_mongo-db_mongodb_7-1:27017")
                # # database 연결
                # database = mongoClient["study_finance"]
                # # collection 작업
                # collection = database["coordinatesbylocationname"]

                # result = collection.insert_many(content)

                # print(result.inserted_ids)
                return {'lat' : int(content[0]['lat']), 'lon' : int(content[0]['lon'])}
                pass
            else :
                print(f"error : result empty {response.content}")
                return None
        else :
            print(f"error : {response.status_code}")
            return None

        