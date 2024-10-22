from bs4 import BeautifulSoup # html 해석기

import requests # url 주소

# naver 검색어에 따른 타이틀 수집
# https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EA%B8%88%EC%9C%B5
# span.lnk_tit

# 검색어 받기
keyword = input('input search word : ')

# 브라우저 주소창
html_str = f'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={keyword}'
response = requests.get(html_str)

#Dom 구조화
soup = BeautifulSoup(markup=response.text, features='html.parser')

titles = soup.select('span.lnk_tit')

'''
len(titles) = 14
titles[10]
<span class="lnk_tit">300만원 대출 둥지대부에서</span>
'''
print(f'title count : {len(titles)}')
for title in titles :
    print(f'title : {title.text}')

pass
