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



def main() :
    # MongoDB 서버에 연결 : Both connect in case local and remote
    client = MongoClient('mongodb://192.168.0.207:27017/')
    # 'mydatabase' 데이터베이스 선택 (없으면 자동 생성)
    db = client['news_database_sanghoonlee']
    # 'users' 컬렉션 선택 (없으면 자동 생성)
    collection = db['news_collection_sanghoonlee']

    news_datas = do_scrapping()

    # 데이터 입력
    result = collection.insert_many(news_datas)

    # 입력된 문서의 ID 출력
    print('Inserted user id:', result.inserted_ids)
    return

if __name__ == '__main__':
    main()
    pass