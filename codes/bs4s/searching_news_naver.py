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
title : 
원-달러 환율 1,380원대 상승...7월 말 이후 최고

content : 
                        원-달러 환율이 장 초반부터 큰 폭으로 오르며 1,380원을 돌파했습니다....

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
        print(f'title : {title.text}')
        sub_list = search_naver(f'#dic_area', title.attrs['href'])
        for sub_title in sub_list: # 1개 나옴 
            print(f'content : {sub_title.text}')
        print(f'--'*30)



if __name__ == '__main__':
    main()
