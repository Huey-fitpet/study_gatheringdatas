from bs4 import BeautifulSoup # html 해석기

import requests # url 주소

# https://news.naver.com/section/101
'''
li > div > div > div.sa_text > [href]
li > div > div > div.sa_text > a
#dic_area
'''

'''
출력결과
title count : 46
title : 부광약품, 3분기 영업익 32억…전년比 흑자 전환
content : [서울=뉴시스] 박은비 기자 = 부광약품은 연결재무제표...
'''

def search_naver(selector, url = None) :

    # 브라우저 주소창
    html_str = url
    response = requests.get(html_str)

    #Dom 구조화
    soup = BeautifulSoup(markup=response.text, features='html.parser')

    titles = soup.select(selector)

    return titles


def main():
    naver_url = f'https://news.naver.com/section/101'
    reault_list = search_naver(f'li > div > div > div.sa_text > [href]', naver_url)

    print(f'title count : {len(reault_list)}')
    for title in reault_list :
        print(f'title : {title.text.strip()}')
        sub_list = search_naver(f'#dic_area', title.attrs['href'])
        for sub_title in sub_list: # 1개 나옴 
            print(f'content : {sub_title.text.strip()}')
        print(f'--'*30)
        

if __name__ == '__main__':
    main()
