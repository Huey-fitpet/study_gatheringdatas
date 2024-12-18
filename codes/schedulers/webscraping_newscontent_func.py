import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

url = f'http://underkg.co.kr/news'


def do_scrapping():
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    news_list = soup.select('.col-inner') # 되도록 짧은게 좋아 => 추후 프론트엔드 개발자에 의해 변경가능성 있어서

    results = [] 
    for news in news_list:
        title_link = news.select_one('h1 > a')
        print(f'title: {title_link.text}')
        date = news.select_one('span.time > span')
        read_num = news.select_one('span.readNum > span')
        print(f'date: {title_link.text}, read_num: {read_num.text}, link: {title_link.attrs["href"]}')
        news_content_url = title_link.attrs["href"]
        # 기사 내용 가져오기
        news_response = requests.get(news_content_url)
        news_soup = BeautifulSoup(news_response.text,'html.parser')
        content = news_soup.select_one('div.docInner > div.read_body') 
        print(f'content : {content.text}')
        print(f'--'*30)

        # 결과를 딕셔너리 로 저장
        news_data = {
            'title': title_link.text,
            'link': news_content_url,
            'date': date.text,
            'readnum': read_num.text,
            'content': content.text
        }
        results.append(news_data)

    return results

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

def main(args_list) :

    ip_add = args_list[0]
    db_name = args_list[1]
    col_name = args_list[2]
    #folder = args_list[3]
    #url = args_list[4]

    news_datas = do_scrapping()

    result_ids = insert_recode_in_mongo(ip_add, db_name, col_name, news_datas)
    # 입력된 문서의 ID 출력
    print('Inserted user id num:', len(result_ids.inserted_ids))
    return

if __name__ == '__main__':
    
    ip_add = f'mongodb://192.168.0.207:27017/'
    db_name = f'news_database_sanghoonlee'
    col_name = f'news_collection_sanghoonlee'
    #folder = f'./downloads'
    #url = f'https://www.yna.co.kr/economy/all'
    #args_list = [ip_add,db_name,col_name,folder,url]
    args_list = [ip_add,db_name,col_name]
    main(args_list)
    pass