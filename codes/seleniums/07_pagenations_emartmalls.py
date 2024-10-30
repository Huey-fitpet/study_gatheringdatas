# * 웹 크롤링 동작
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
import requests
webdriver_manager_directory = ChromeDriverManager().install()

# ChromeDriver 실행
browser = webdriver.Chrome(service=ChromeService(webdriver_manager_directory))

# Chrome WebDriver의 capabilities 속성 사용
capabilities = browser.capabilities

# - 주소 입력(https://www.w3schools.com/)
# f'https://accounts.kakao.com/login/?continue=https%3A%2F%2Fwww.daum.net#login'
browser.get(f'https://emart.ssg.com/disp/category.ssg?dispCtgId=6000214033')

# - 가능 여부에 대한 OK 받음
pass
# - html 파일 받음(and 확인)
html = browser.page_source
# print(html)
element_path = f'#swiper-wrapper-01f169110cf10240e3 > li.mnemitem_grid_item.swiper-slide.swiper-slide-active > div > div > div.mnemitem_detailbx > div.mnemitem_tx_thmb > a > div.mnemitem_tit > span.mnemitem_goods_tit'

from selenium.webdriver.common.by import By

# #loginId--1
# #password--2
# button.btn_g.highlight.submit

'''
상품을 페이지 이동하며 정보 수집
1~12 까지 페이지
#area_itemlist > div.paginate > div > strong
#area_itemlist > div.paginate > div > a
11번 stop 키워드 
#area_itemlist > div.paginate > div > a.btn_next

상품 리스트
#ty_thmb_view div.mnemitem_thmb_v2 > a
'''

import time 
element_selector_detail = f'#ty_thmb_view div.mnemitem_thmb_v2 > a'



# css 조합 셀렉트 사용 가능
page_list_tag = f'#area_itemlist > div.paginate > div > a, #area_itemlist > div.paginate > div > strong'
page_list = browser.find_elements(by=By.CSS_SELECTOR, value=page_list_tag)


for index in range(1,len(page_list))[8:]:
    time.sleep(1)
    pagination_list = browser.find_elements(by=By.CSS_SELECTOR, value=page_list_tag)
    
    pagination_tag = pagination_list[index]

    btn_next = pagination_tag.get_attribute('class')
    if btn_next == f'btn_next':
        break
    pagination_tag.click()

    time.sleep(2)
    # 상세 정보 수집
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    detail_list = soup.select(element_selector_detail)
    for detail in detail_list:
        detail_url = detail.attrs['href']
        detail_url = f'https://emart.ssg.com{detail_url}'
        response = requests.get(detail_url) 
        # response.content
        pass
    pass
pass