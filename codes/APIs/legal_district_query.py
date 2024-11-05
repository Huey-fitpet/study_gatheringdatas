

import requests
#uri 소스에서 넣을 때 길이가 256자 이내로 

'''
https://api.openweathermap.org/geo/1.0/direct?q=seoul&appid=39fb7b1c6d4e11e7483aabcb737ce7b0

http://api.openweathermap.org/geo/1.0/direct?q={city name}&appid={API key}
'''
import json
class legal_district_query:

    def send_api(cityname = None, admCode = None) :
        url = f'http://api.vworld.kr/ned/data/admCodeList'
        params ={
            'key' : 'C008E763-541C-3B93-B0E6-9C218A8C7038', 
            'format' : 'json', 
            'numOfRows' : '17', 
            'pageNo' : '1'
            }
        
        if admCode :
            url = f'http://api.vworld.kr/ned/data/admSiList'
            params ={
                'key' : 'C008E763-541C-3B93-B0E6-9C218A8C7038', 
                'admCode' : admCode, 
                'format' : 'json', 
                'numOfRows' : '17', 
                'pageNo' : '1'
            }

        '''
        서울 + 특별시
        인천 + 광역시
        제주 + 
        경북 경상북도
        전남 전라남도
        강원 + 도
        '''
        response = requests.get(url, params=params)
        print(response.status_code)
        if response.status_code == 200 :
            if response.text !='[]' :
                content = json.loads(response.content)
                find_code = None
                for city in content['admVOList']['admVOList'] :
                    if city['lowestAdmCodeNm'] == cityname :
                        find_code = city['admCode']
                return find_code
                # return {'lat' : int(content[0]['lat']), 'lon' : int(content[0]['lon'])}
            else :
                print(f"error : result empty {response.content}")
                return None
        else :
            print(f"error : {response.status_code}")
            return None


class ApiRequester:

    def make_prams() :
        params = {}
        return params
    
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
        


if __name__ == '__main__':
    # legal_district_query.send_api(f'인천광역시')
    # legal_district_query.send_api(f'계양구',  f'28')
    legal_district_query.send_api(f'강남구',  f'11')