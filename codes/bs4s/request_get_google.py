from bs4 import BeautifulSoup # html 해석기

import requests # url 주소

# 브라우저 주소창
response = requests.get('https://www.google.co.kr/')

print(response.text)

# 환율 변동 가격 찾기 
# https://finance.naver.com/marketindex/
#head_info point_
#<span class="value">1,374.80</span> => f12에서 span.value로 검색 가능
pass
