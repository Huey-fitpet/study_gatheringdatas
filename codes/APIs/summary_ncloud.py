
import requests
import json
from bs4 import BeautifulSoup as bs
import pandas as pd
import pydeck as pdk
from insert_recode_in_mongo import connect_mongo as cm
# mongo DB 동작
from pymongo import MongoClient
# from legal_district_query  import ApiRequester as ar
from config_reader import read_config # config read 용 

class summary_ncloud:

    def make_body():
        return 

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

    def send_api(url, headers):

        bodys = {
                "document": {
                    "title": "'금투세 폐지'…국내증시 날개 달까",
                    "content": "[서울=뉴시스] 배요한 기자 = 동학개미(국내 개인투자자)들의 숙원이었던 금융투자소득세(금투세)가 마침내 폐지로 가닥이 잡혔다. 야당이 장고 끝에 금투세 폐지에 '동의'하면서, 금투세는 유예 기간 종료를 2개월 앞두고 4년 만에 사라지게 됐다. 투자자들은 너무 늦었다는 반응과 함께 이제라도 폐지된다는 점에서 대부분 긍정적인 평가가 나온다. 5일 한국거래소에 따르면 코스피는 전 거래일(2582.96)보다 46.61포인트(1.83%) 오른 2588.97에 장을 마쳤다. 특히 코스닥 지수는 3.43% 급등하며, 금투세 폐지에 대한 기대감이 더 크게 반영됐다. 이날 코스닥 시가총액 상위 종목인 알테오젠(9.26%), 에코프로비엠(7.25%), 에코프로(7.37%), HLB(4.86%), 리가켐바이오(8.96%), 엔켐(6.62%), 휴젤(7.48%), 삼천당제약(4.90%), 클래시스(4.15%) 등은 일제히 초강세를 나타냈다. 하지만 이 대표의 발언에 국내 증시가 즉각 반응하면서 금투세는 증시를 억눌러왔던 악재라는 것을 증명하게 됐다. 이미 그동안 금투세는 증시를 발목잡는 복병으로 각인돼왔다. 미국과 유럽, 일본 등의 증시가 사상 최고치를 경신한 가운데 코스피는 지난 2021년 6월 고점(3316.08)을 찍은 이후 2100~2900선 사이에서 움직이며 상대적으로 소외돼 왔기 때문이다. 같은 기간 국내 증시가 하락해 박스권에서 움직이는 동안 미국을 대표하는 S&P500 지수와 일본 니케이255 지수, 유로스톡스50 등 해외 지수는 국내와 디커플링(탈동조화) 모습을 보이며 사상 최고가를 경신했다."
                },
                "option": {
                    "language": "ko",
                    "model": "news",
                    "tone": 3,
                    "summaryCount": 6
                }
            }
        # target_uri = f'{url}{key}/json/bikeList/{start}/{end}/'
        response = requests.post(url=url, headers=headers, data=json.dumps(bodys))
    
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
    uri = f'https://naveropenapi.apigw.ntruss.com/text-summary/v1/summarize'
    # params = {
    #     'query' : '진주',
    #     'display' : '100'
    # }
    headers = {
        'X-NCP-APIGW-API-KEY-ID' : config['Ncloud_Key']['X-NCP-APIGW-API-KEY-ID'],
        'X-NCP-APIGW-API-KEY' : config['Ncloud_Key']['X-NCP-APIGW-API-KEY'],
        'Content-Type' : 'application/json'
    }
    
    data_items = summary_ncloud.send_api(uri, headers)

    # # key = f'445551536d64656d3438576f436178'
    # data_bikes = pd.DataFrame()
    
    # # (대여소 수 : '18.11월말기준 1,471개소)
    # escape_cnt = -1
    # prev_item = 1
    # increment_value = 999
    # while True:
    #     data_bikes = pd.concat([data_bikes, naver_search.send_api(uri, headers, prev_item, prev_item + increment_value)], ignore_index=True)
    #     # 최댓값이 변하지 않으면 탈출
    #     if escape_cnt != len(data_bikes) :
    #         escape_cnt = len(data_bikes)
    #     else :
    #         break
    #     prev_item += increment_value
     
    # # seoul_bike_list.print_graph(data_bikes)

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
        list_dataframe['goods_id'] = result_list.inserted_ids
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