
import requests
import json
from bs4 import BeautifulSoup as bs
import pandas as pd
import pydeck as pdk

from insert_recode_in_mongo import connect_mongo as cm
from config_reader import read_config # config read 용 

# mongo DB 동작
from pymongo import MongoClient
# from legal_district_query  import ApiRequester as ar


class naver_search:

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

    def send_api(url, params, headers):

        # target_uri = f'{url}{key}/json/bikeList/{start}/{end}/'
        response = requests.get(url=url, params=params, headers=headers)
    
        if response.status_code == 200:
            print(f'{response.text}')
            '''
            '{"errorMessage":"NID AUTH Result Invalid (1000) : Authentication failed. (인증에 실패했습니다.)",
            "errorCode":"024"}'
             '''
            soup = bs(markup=response.text, features='xml')
            print(soup.prettify())
            return_auth_msg = soup.find('CODE')
            if return_auth_msg != None :
                # error return
                print(f'error : {return_auth_msg.text}')
            else :
                content = json.loads(response.text) 
                '''
                {\n\t"lastBuildDate":"Tue, 05 Nov 2024 12:02:29 +0900",
                \n\t"total":4643122,\n\t"start":1,\n\t"display":10,\n\t"items":[\n\t\t{\n\t\t\t"title":"<b>진주<\\/b>이혼전문변호사 갈등 대변은",\n\t\t\t"link":"https:\\/\\/blog.naver.com\\/jmj7755\\/223646482171",\n\t\t\t"description":"<b>진주<\\/b>이혼전문변호사 갈등 대변은 법치주의 국가에서 살아가기 위해서는 확정된 생계 방법 및 규범을... 복잡하기에 <b>진주<\\/b>이혼전문변호사는 일부로 혐의 증명을 하지 않는 것은 안 된다고 조언했죠. 법조가는... ",
                '''
                # json 으로 요청해서 code가 json 으로 옴. xml 일때도 있고, json 일 수도 있어서 모두 고려해야 함.
                if f'CODE' in content:
                    print(f'error : {content["CODE"]}')
                else :
                    item_data = {
                            "title" : [],
                            "link" : [],
                            "lprice" : [],
                            "hprice" : [],
                            "productId" : []
                        }
                    
                    for item in content["items"]:
                        # title : 상품페이지 이름
                        # link : 상품페이지 링크
                        # lprice, hprice: 최대 최소 가격
                        # productId : 상품 id 
                        # 1회 최대 1000건 
                        item_data['title'].append(item['title'].strip())
                        item_data['link'].append(item['link'])
                        # item_data['lprice'].append(int(item['lprice']))
                        # item_data['hprice'].append(int(item['hprice']))
                        item_data['lprice'].append(int(item['lprice']) if item['lprice'] != '' else 0)  # 빈 문자열인 경우 0 추가
                        item_data['hprice'].append(int(item['hprice']) if item['hprice'] != '' else 0)  # 빈 문자열인 경우 0 추가
                        item_data['productId'].append(item['productId'])
                        pass
                    return pd.DataFrame(item_data)
            pass
        else :
            pass

        return


def main():

    config = read_config()
    # uri = f'http://openapi.seoul.go.kr:8088/{key}/json/bikeList/{start}/{end}/'
    serviceid = f'shop'
    uri = f'https://openapi.naver.com/v1/search/{serviceid}'
    params = {
        'query' : '진주',
        'display' : '100'
    }
    headers = {
        'X-Naver-Client-Id' : config['Naver_Key']['X-Naver-Client-Id'],
        'X-Naver-Client-Secret' : config['Naver_Key']['X-Naver-Client-Secret']
    }
    
    data_items = naver_search.send_api(uri, params, headers)

    # MongoDB 서버에 연결 : Both connect in case local and remote
    ip_add = f'mongodb://192.168.0.91:27017/'
    db_name = f'study_finance_shl'
    info_col_name = f'search_shop_info'
    list_col_name = f'search_shop_list'
    client = MongoClient(ip_add)

    try:
        # 두 컬렉션에 넣어야함. 상품 먼저 insert 하고 list insert list insert 시 id 연결?
        result_list = cm.insert_recode_in_mongo(client, db_name, info_col_name, data_items)
        print(f'insert id list count : {len(result_list.inserted_ids)}')
        list_dataframe = data_items[['title', 'link']] # 기억을 위해 이름, link 씀
        list_dataframe['goods_id'] = result_list.inserted_ids # 상세정보 데이터의 id를 list col에 저장
        result_list = cm.insert_recode_in_mongo(client, db_name, list_col_name, list_dataframe)
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