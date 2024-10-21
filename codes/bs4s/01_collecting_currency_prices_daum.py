from bs4 import BeautifulSoup # html 해석기

import requests # url 주소


# 환율 변동 가격 찾기 
# https://finance.naver.com/marketindex/
#head_info point_
#<span class="value">1,374.80</span> => f12에서 span.value로 검색 가능

# https://finance.daum.net/domestic/exchange
html_str = 'https://finance.daum.net/domestic/exchange'
# 브라우저 주소창
response = requests.get(html_str)

#Dom 구조화
# BeautifulSoup(markup=response.text, features='html.parser')
soup = BeautifulSoup(markup=response.text, features='html.parser')
type(soup)
# <class 'bs4.BeautifulSoup'>

'''

<span class="num down">-2.05%</span>

'''
#currency_prices = soup.select('div#boxCommodities.tableB.mt>div.box_contents>div>table>tbody>tr.first>td.pR>span.num.down')
currency_prices = soup.select('#boxCommodities.tableB.mt .box_contents div table tbody tr td.pR span.num')# div.box_contents')
#currency_prices = soup.select('span.num')
type(currency_prices) # <class 'bs4.element.ResultSet'> 
print(currency_prices)

for cp in currency_prices:
    print(f'Tag : {cp}, Currency Price : {cp.text}') # type(cp) = <class 'bs4.element.Tag'>
    pass

"""
    
Tag : <span class="value">1,377.80</span>, Currency Price : 1,377.80
Tag : <span class="value">919.97</span>, Currency Price : 919.97
Tag : <span class="value">1,495.26</span>, Currency Price : 1,495.26
Tag : <span class="value">193.34</span>, Currency Price : 193.34
Tag : <span class="value">149.5400</span>, Currency Price : 149.5400
Tag : <span class="value">1.0876</span>, Currency Price : 1.0876
Tag : <span class="value">1.3053</span>, Currency Price : 1.3053
Tag : <span class="value">103.3000</span>, Currency Price : 103.3000
Tag : <span class="value">68.69</span>, Currency Price : 68.69
Tag : <span class="value">1592.94</span>, Currency Price : 1592.94
Tag : <span class="value">2730.0</span>, Currency Price : 2730.0
Tag : <span class="value">120776.12</span>, Currency Price : 120776.12
"""

