


from bs4 import BeautifulSoup # html 해석기

import requests # url 주소


# 환율 변동 가격 찾기 
#https://finance.naver.com/marketindex/?tabSel=materials#tab_section
#head_info point_
#<span class="value">1,374.80</span> => f12에서 span.value로 검색 가능

html_str = 'https://finance.naver.com/marketindex/?tabSel=materials#tab_section'

# 브라우저 주소창
response = requests.get(html_str)

#Dom 구조화
# BeautifulSoup(markup=response.text, features='html.parser')
soup = BeautifulSoup(markup=response.text, features='html.parser')
type(soup)
# <class 'bs4.BeautifulSoup'>

currency_prices = soup.select('td.tit')
type(currency_prices) # <class 'bs4.element.ResultSet'> 

print(f'Material Count : {len(currency_prices)}') 
for num, cp in enumerate(currency_prices,start=1):
    # print(f'Tag : {cp}, Currency Price : {cp.text}') # type(cp) = <class 'bs4.element.Tag'>
    print(f'{num}. Material Name : {cp.text}') # type(cp) = <class 'bs4.element.Tag'>
    pass

"""
결과 출력
Material Count : 20
1. Material Name : 가스오일
2. Material Name : 난방유
3. Material Name : 천연가스
4. Material Name : 구리
5. Material Name : 납
6. Material Name : 아연
7. Material Name : 니켈
8. Material Name : 알루미늄합금
9. Material Name : 주석
10. Material Name : 옥수수
11. Material Name : 설탕
12. Material Name : 대두
13. Material Name : 대두박
14. Material Name : 대두유
15. Material Name : 면화
16. Material Name : 소맥
17. Material Name : 쌀
18. Material Name : 오렌지주스
19. Material Name : 커피
20. Material Name : 코코아
"""

pass