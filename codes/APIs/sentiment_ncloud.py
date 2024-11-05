
import requests
import json
from bs4 import BeautifulSoup as bs
import pandas as pd
import pydeck as pdk

# 만든 class
from insert_recode_in_mongo import connect_mongo as cm # insert mongo
from config_reader import read_config # config read 용 


# mongo DB 동작
from pymongo import MongoClient

# * 웹 크롤링 동작
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


# from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


class content_youtube:
    def run_content_from_youtube(browser):

        '''
        - 수집 데이터 mongodb에 insert
        - 항목 : 작성자, 작성일, 댓글, 좋아요와 싫어요 갯수
        - github, remote mongo uri 공유


        작성자 : #author-text > span
        작성일 : #published-time-text > a
        댓글 : #content-text > span
        좋아요 : #vote-count-middle
        싫어요 : 싫어요 갯수 출력하는 태그 없는 듯?

        '''

        # - html 파일 받음(and 확인)
        html = browser.page_source

        time.sleep(5)
        element_value = f'body'
        element_body = browser.find_element(by=By.CSS_SELECTOR, value=element_value)

        for num in range(15):
            time.sleep(1)
            element_body.send_keys(Keys.PAGE_DOWN)

        id_tag = f'#author-text > span'
        date_tag = f'#published-time-text > a'
        content_tag = f'#content-text > span'
        vote_cnt_tag = f'#vote-count-middle'

        ls_id = browser.find_elements(by=By.CSS_SELECTOR, value=id_tag)
        ls_date = browser.find_elements(by=By.CSS_SELECTOR, value=date_tag)
        ls_content = browser.find_elements(by=By.CSS_SELECTOR, value=content_tag)
        ls_vote_cnt = browser.find_elements(by=By.CSS_SELECTOR, value=vote_cnt_tag)

        ret_dict_list = []
        for num, (id, date, content, vote_cnt) in enumerate(zip(ls_id, ls_date, ls_content, ls_vote_cnt),start=1):

            # 각 댓글 정보를 딕셔너리로 저장
            comment_data = {
                'comment_count': num,
                'author': id.text,
                'date': date.text,
                'content': content.text,
                'vote_count': vote_cnt.text,
                'dislike_count' : f'0'
            }
            
            # 딕셔너리를 리스트에 추가
            ret_dict_list.append(comment_data)

            pass
        
        return ret_dict_list
pass

class sentiment_ncloud:

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

    def send_api(url, headers, comment):

        bodys = {
                "content": comment
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
                    return content # 어떤 데이터 써야 될 지 몰라서 일단 내보내서 저장
            pass
        else :
            pass

        return


def main():

    webdriver_manager_directory = ChromeDriverManager().install()

    # ChromeDriver 실행
    browser = webdriver.Chrome(service=ChromeService(webdriver_manager_directory))

    # Chrome WebDriver의 capabilities 속성 사용
    capabilities = browser.capabilities

    # - 주소 입력(https://www.w3schools.com/)
    target_url = f'https://www.youtube.com/watch?v=iQZCVbseEMQ'
    browser.get(target_url)

    # - 가능 여부에 대한 OK 받음

    try:
        content_lists = content_youtube.run_content_from_youtube(browser)
    except Exception as e :
        print(e)
    finally:
        browser.quit()

    uri = f'https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze'
    # params = {
    #     'query' : '진주',
    #     'display' : '100'
    # }

    config = read_config()

    headers = {
        'X-NCP-APIGW-API-KEY-ID' : config['Ncloud_Key']['X-NCP-APIGW-API-KEY-ID'],
        'X-NCP-APIGW-API-KEY' : config['Ncloud_Key']['X-NCP-APIGW-API-KEY'],
        'Content-Type' : 'application/json'
    }
    
    data_items = []
    for comment in content_lists:
         data_items.append(sentiment_ncloud.send_api(uri, headers, comment['content']))

    # MongoDB 서버에 연결 : Both connect in case local and remote
    ip_add = f'mongodb://192.168.0.91:27017/'
    db_name = f'study_finance_shl'
    sentiment_col_name = f'comment_sentiment'
    comment_col_name = f'comment_data'
    client = MongoClient(ip_add)

    try:
        # 두 컬렉션에 넣어야함. 상품 먼저 insert 하고 list insert list insert 시 id 연결?
        result_list = cm.insert_recode_in_mongo(client, db_name, comment_col_name, content_lists)
        # inserted_ids 처리해야해 
        print(f'insert id list count : {len(result_list.inserted_ids)}')
        result_list = cm.insert_recode_in_mongo(client, db_name, sentiment_col_name, data_items)
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