
'''
http://underkg.co.kr/news

https://underkg.co.kr/news/2941893
https://underkg.co.kr/news/2941889

#board_list > div > div:nth-child(1) > div > h1 > a[href]
#board_list > div > div:nth-child(1) > div > h1 > [href]

리스트에서 링크와 제목, 날짜, 읽은 횟수 묶음 가져오기

기사 타이틀 부분  .col-inner
기사 제목, 링크   h1 > a
기사 날짜         new_info > span > span
기사 내용 확인용 URI [href]

body > div.user_layout > div.body > div.content > div > div.docInner > div.read_body

기사 안의 내용
div.docInner > div.read_body



'''

import requests
from bs4 import BeautifulSoup
url = f'http://underkg.co.kr/news'



def main() :
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    news_list = soup.select('.col-inner') # 되도록 짧은게 좋아 => 추후 프론트엔드 개발자에 의해 변경가능성 있어서

    for news in news_list:
        title_link = news.select_one('h1 > a')
        print(f'title: {title_link.text}')
        date = news.select_one('span.time > span')
        read_num = news.select_one('span.readNum > span')
        print(f'date: {date.text}, read_num: {read_num.text}, link: {title_link.attrs["href"]}')
        news_content_url = title_link.attrs["href"]
        # 기사 내용 가져오기
        news_response = requests.get(news_content_url)
        news_soup = BeautifulSoup(news_response.text,'html.parser')
        content = news_soup.select_one('div.docInner > div.read_body') 
        print(f'content : {content.text}')
        print(f'--'*30)
    return

if __name__ == '__main__':
    main()
    pass