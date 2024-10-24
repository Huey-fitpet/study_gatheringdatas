
import requests
from bs4 import BeautifulSoup
import os
import urllib.request as req
from pymongo import MongoClient

'''
이미지 다운로드
target tag : #container > div > div > div.section01 > section > div.list-type038 > ul > li > div 
div.news-con > a > strong
div.news-con > p
figure > a
div.info-box01 > span.txt-time

저장 위치 
./downloads/

mongodb ip
mongodb://192.168.0.207:27017/

'''

def do_scrapping(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')

    target_tag = f'#container > div > div > div.section01 > section > div.list-type038 > ul > li > div ' # #majorList.list > li > div

    news_list = soup.select(target_tag)

    results = [] 
    for news in news_list:
        title_link = news.select_one('.news-con > a > strong')
        if title_link == None: # 광고가 중간에 있어서 넘김
            continue
        print(f'title: {title_link.text}') 
             
        summary = news.select_one('.news-con > p.lead')
        print(f'summary: {summary.text}')

        date = news.select_one('.info-box01 > .txt-time')
        img_link = news.select_one('figure > a > img')
        if img_link == None: # 이미지가 없는 기사가 있어서 넘김
            continue
        print(f'date: {date.text}, link: {img_link.attrs["src"]}')

        img_url = img_link.attrs["src"]
        
        # # 기사 내용 가져오기
        # news_response = requests.get(news_content_url)
        # news_soup = BeautifulSoup(news_response.text,'html.parser')
        # content = news_soup.select_one('div.docInner > div.read_body') 
        # print(f'content : {content.text}')
        # print(f'--'*30)

        # 결과를 딕셔너리 로 저장
        news_data = {
            'title': title_link.text,
            'img_link': img_url,
            'date': date.text,
            'sumary': summary.text
        }
        results.append(news_data)

    return results

def img_write_file(folder_name, news_content_list):

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    for num, news_content in enumerate(news_content_list, start=1):
        img_url = news_content["img_link"]
        req.urlretrieve(img_url,f'{folder_name}/{num}.jpg')

    return

def insert_recode_in_mongo(dbip, dbname, collectionname, input_list):

    # MongoDB 서버에 연결 : Both connect in case local and remote
    client = MongoClient(dbip)
    # 'mydatabase' 데이터베이스 선택 (없으면 자동 생성)
    db = client[dbname]
    # 'users' 컬렉션 선택 (없으면 자동 생성)
    collection = db[collectionname]

    # 데이터 입력
    results = collection.insert_many(input_list)

    return results


def main() :

    ip_add = f'mongodb://192.168.0.207:27017/'
    db_name = f'news_database_sanghoonlee'
    col_name = f'news_collection_sanghoonlee'

    folder = f'./downloads'

    url = f'https://www.yna.co.kr/economy/all'

    news_content_list = do_scrapping(url)

    img_write_file(folder, news_content_list)

    result_ids = insert_recode_in_mongo(ip_add, db_name, col_name, news_content_list)
    # 입력된 문서의 ID 출력
    print('Inserted user id num:', len(result_ids.inserted_ids))
    return

if __name__ == '__main__':
    main()
    pass