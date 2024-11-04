
import requests
import json
from bs4 import BeautifulSoup as bs
import pandas as pd
import pydeck as pdk
from insert_recode_in_mongo import connect_mongo as cm
# mongo DB 동작
from pymongo import MongoClient
# from legal_district_query  import ApiRequester as ar


class seoul_bike_list:

    def print_graph(df):
        # Scatter plot 그리기
        layer = pdk.Layer(
            "ScatterplotLayer",
            df,
            get_position = ["stationLongitude", "stationLatitude"],
            get_fill_color = ["255", "255-parkingBikeTotCnt", "255-parkingBikeTotCnt"],
            get_radius = "60 * parkingBikeTotCnt / 100",
            pickable = True,
        )
        # 서울의 중심점 좌표 구해 지도 만들기
        lat_center = df["stationLatitude"].mean()
        lon_center = df["stationLongitude"].mean()
        initial_view = pdk.ViewState(latitude=lat_center, longitude=lon_center, zoom=10)
        map = pdk.Deck(layers=[layer], initial_view_state=initial_view, tooltip={"text":"대여소 : {stationName}\n현재 주차 대수 : {parkingBikeTotCnt}"})
        map.to_html("./seoul_bike.html")
        pass 

    def send_api(url, key, start, end):

        target_uri = f'{url}{key}/json/bikeList/{start}/{end}/'
        response = requests.get(url=target_uri)
    
        if response.status_code == 200:
            print(f'{response.text}')
            '''
            <?xml version="1.0" encoding="utf-8"?>
            <RESULT>
            <CODE>
            INFO-100
            </CODE>
            <MESSAGE>
            인증키가 유효하지 않습니다.
            인증키가 없는 경우, 열린 데이터 광장 홈페이지에서 인증키를 신청하십시오.
            </MESSAGE>
            </RESULT>
             '''
            soup = bs(markup=response.text, features='xml')
            print(soup.prettify())
            return_auth_msg = soup.find('CODE')
            if return_auth_msg != None :
                # error return
                print(f'error : {return_auth_msg.text}')
            else :
                content = json.loads(response.content)
                '''
                    data = {
                    'name': ["Choi", "Choi", "Choi", "Kim", "Park"], 
                    'year': [2013, 2014, 2015, 2016, 2017], 
                    'points': [1.5, 1.7, 3.6, 2.4, 2.9]
                    } 
                '''
                # json 으로 요청해서 code가 json 으로 옴. xml 일때도 있고, json 일 수도 있어서 모두 고려해야 함.
                if f'CODE' in content:
                    print(f'error : {content["CODE"]}')
                else :
                    data_bikes = {
                            "stationName" : [],
                            "parkingBikeTotCnt" : [],
                            "stationLatitude" : [],
                            "stationLongitude" : []
                        }
                    
                    for station in content["rentBikeStatus"]["row"]:
                        # stationName : 대여소 이름
                        # parkingBikeTotCnt : 대여된 갯수
                        # stationLatitude, stationLongitude: 대여소 위경도
                        # 1회 최대 1000건 
                        data_bikes['stationName'].append(station['stationName'])
                        data_bikes['parkingBikeTotCnt'].append(int(station['parkingBikeTotCnt']))
                        data_bikes['stationLatitude'].append(float(station['stationLatitude']))
                        data_bikes['stationLongitude'].append(float(station['stationLongitude']))
                        pass
                    return pd.DataFrame(data_bikes)
            pass
        else :
            pass

        return


def main():

    # uri = f'http://openapi.seoul.go.kr:8088/{key}/json/bikeList/{start}/{end}/'
    uri = f'http://openapi.seoul.go.kr:8088/'
    key = f'445551536d64656d3438576f436178'
    data_bikes = pd.DataFrame()
    
    # (대여소 수 : '18.11월말기준 1,471개소)
    escape_cnt = -1
    prev_item = 1
    increment_value = 999
    while True:
        data_bikes = pd.concat([data_bikes, seoul_bike_list.send_api(uri, key, prev_item, prev_item + increment_value)], ignore_index=True)
        if escape_cnt != len(data_bikes) :
            escape_cnt = len(data_bikes)
        else :
            break
        prev_item += increment_value
     
    # seoul_bike_list.print_graph(data_bikes)

    # MongoDB 서버에 연결 : Both connect in case local and remote
    ip_add = f'mongodb://192.168.0.91:27017/'
    db_name = f'study_finance'
    col_name = f'bike_col_sanghoonlee'
    client = MongoClient(ip_add)

    try:
        result_list = cm.insert_recode_in_mongo(client, db_name, col_name, data_bikes)
        print(f'insert id list count : {len(result_list.inserted_ids)}')
    except Exception as e :
        print(e)
    finally:
        client.close()
    pass


    # imon 
    return


if __name__ == '__main__':
    main()
    pass