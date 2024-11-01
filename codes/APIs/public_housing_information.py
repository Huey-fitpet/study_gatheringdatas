
# 조달청 표준 정보 수집
import requests
from bs4 import BeautifulSoup as bs
import json

# mongo DB 동작
from pymongo import MongoClient

from legal_district_query import legal_district_query as ldq
from insert_recode_in_mongo import connect_mongo as cm

#uri 소스에서 넣을 때 길이가 256자 이내로 
'''
b%2BuPtb%2FjY5AJJaFNhnoxKmcQ4GlZzKkUexWNoXgXGghltMzrUOMEGVG0bN%2FkTdkwOEWeXW6F6H8V%2Fkcc78hvdg%3D%3D
url = f'https://apis.data.go.kr/1230000/PubDataOpnStdService/getDataSetOpnStdBidPblancInfo?
serviceKey=b%2BuPtb%2FjY5AJJaFNhnoxKmcQ4GlZzKkUexWNoXgXGghltMzrUOMEGVG0bN%2FkTdkwOEWeXW6F6H8V%2Fkcc78hvdg%3D%3D&
pageNo=1&
numOfRows=10&
type=json&
bidNtceBgnDt=201712010000&
bidNtceEndDt=201712312359'
'''


'''
에러코드	에러메세지	          설명
1	        APPLICATION ERROR	어플리케이션 에러
4	        HTTP_ERROR	        HTTP 에러
12	        NO_OPENAPI_SERVICE_ERROR	해당 오픈 API 서비스가 없거나 폐기됨
20	        SERVICE_ACCESS_DENIED_ERROR	서비스 접근거부
22	        LIMITED_NUMBER_OF_SERVICE_REQUESTS_EXCEEDS_ERROR	서비스 요청제한횟수 초과에러
30	        SERVICE_KEY_IS_NOT_REGISTERED_ERROR	등록되지 않은 서비스키
31	        DEADLINE_HAS_EXPIRED_ERROR	활용기간 만료
32	        UNREGISTERED_IP_ERROR	등록되지 않은 IP
99	        UNKNOWN_ERROR	    기타에러


 C008E763-541C-3B93-B0E6-9C218A8C7038

'''
'''
b+uPtb/jY5AJJaFNhnoxKmcQ4GlZzKkUexWNoXgXGghltMzrUOMEGVG0bN/kTdkwOEWeXW6F6H8V/kcc78hvdg==
b%2BuPtb%2FjY5AJJaFNhnoxKmcQ4GlZzKkUexWNoXgXGghltMzrUOMEGVG0bN%2FkTdkwOEWeXW6F6H8V%2Fkcc78hvdg%3D%3D
'''
# url = f'https://data.myhome.go.kr:443/rentalHouseList'
# params ={
    
#     'serviceKey' : 'b%2BuPtb%2FjY5AJJaFNhnoxKmcQ4GlZzKkUexWNoXgXGghltMzrUOMEGVG0bN%2FkTdkwOEWeXW6F6H8V%2Fkcc78hvdg%3D%3D', 
#     'brtcCode' : '11', 
#     'signguCode' : '140', 
#     'numOfRows' : '10', 
#     'pageNo' : '1'
#     }

# url = f'http://api.vworld.kr/ned/data/admCodeList'
# params ={
#     'key' : 'C008E763-541C-3B93-B0E6-9C218A8C7038', 
#     'format' : 'json', 
#     'numOfRows' : '17', 
#     'pageNo' : '1', 
#     }

def run(sido_code, gugun_code) :
    url = f'http://apis.data.go.kr/B552061/frequentzoneBicycle/getRestFrequentzoneBicycle'
    params ={
        'ServiceKey' : 'b+uPtb/jY5AJJaFNhnoxKmcQ4GlZzKkUexWNoXgXGghltMzrUOMEGVG0bN/kTdkwOEWeXW6F6H8V/kcc78hvdg==', 
        'searchYearCd' : '2023', 
        'siDo' : sido_code, 
        'guGun' : gugun_code, 
        'type' : 'json',
        'numOfRows' : '10',
        'pageNo' : '1'
        }

    response = requests.get(url, params=params)
    if response.status_code == 200 :

        '''
        <OpenAPI_ServiceResponse>\n\t<cmmMsgHeader>\n\t\t<errMsg>SERVICE ERROR</errMsg>\n\t\t<returnAuthMsg>SERVICE_KEY_IS_NOT_REGISTERED_ERROR</returnAuthMsg>\n\t\t<returnReasonCode>30</returnReasonCode>\n\t</cmmMsgHeader>\n</OpenAPI_ServiceResponse>
        '''
        soup = bs(markup=response.text, features='xml')
        print(soup.prettify())
        return_auth_msg = soup.find('returnAuthMsg')
        if return_auth_msg != None :
            print(return_auth_msg.text)
            content = json.loads(response.content)
        else :
            # error return
            print(f'error : {return_auth_msg.text}')
        pass
    else :
        print(f'error : {response.status_code}')

    pass


def main():

    sido = f'서울특별시' #f'인천광역시'
    gugun = f'강남구' #f'계양구'
    sido_code = ldq.send_api(sido)
    gugun_code = ldq.send_api(gugun, sido_code)[2:]

    run(sido_code, gugun_code)


    # ip_add = f'mongodb://192.168.0.63:27017/'
    # db_name = f'youtube_db_sanghoonlee'
    # col_name = f'youtube_col_sanghoonlee'
    # # MongoDB 서버에 연결 : Both connect in case local and remote
    # client = MongoClient(ip_add)

    # try:
    #     result_list = cm.insert_recode_in_mongo(client, db_name, col_name, content_lists)
    # except Exception as e :
    #     print(e)
    # finally:
    #     client.close()
    # print(f'insert id list count : {len(result_list.inserted_ids)}')
    pass

    # city_list = ['도쿄','괌','모나코']

    # run(city_list)
    # send_api(base_url, params, keys = None):

    # base_url = f'https://api.openweathermap.org/geo/1.0/direct'
    # params ={
    #         'q' : '도쿄', 
    #         'appid' : '39fb7b1c6d4e11e7483aabcb737ce7b0'
    #         }
    # key_list = ['lat','lon']
    # temp = ar.send_api(base_url, params, key_list)
    pass

if __name__ == '__main__':
    main()
    pass