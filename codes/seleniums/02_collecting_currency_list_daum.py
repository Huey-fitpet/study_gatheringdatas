# * 웹 크롤링 동작
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

webdriver_manager_directory = ChromeDriverManager().install()

# ChromeDriver 실행
browser = webdriver.Chrome(service=ChromeService(webdriver_manager_directory))

# Chrome WebDriver의 capabilities 속성 사용
capabilities = browser.capabilities

# - 주소 입력(https://finance.daum.net/domestic/exchange)
browser.get("https://finance.daum.net/domestic/exchange")

# - 가능 여부에 대한 OK 받음
pass
# - html 파일 받음(and 확인)
html = browser.page_source
print(html)

# daum exchange 환율 가져오기
# #boxForexes table > tbody > tr : element bundle
# #boxForexes table > tbody > tr > td.pL > a    : country_curreny
# #boxForexes table > tbody > tr > td:nth-child(3) > span  : country_price
from selenium.webdriver.common.by import By
currency_list = browser.find_elements(by=By.CSS_SELECTOR, value='#boxForexes table > tbody > tr')

for index, element_bundle in enumerate(currency_list):
    country_curreny_tag = f'td.pL > a'
    country_curreny = element_bundle.find_element(By.CSS_SELECTOR, country_curreny_tag)
    country_price_tab = f'td:nth-child(3) > span'
    country_price = element_bundle.find_element(By.CSS_SELECTOR, country_price_tab)

    result = f'curreny : {country_curreny.text}, price : {country_price.text}'
    print(result)
    pass
pass