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

# - 주소 입력(https://www.w3schools.com/)
target_url = f'https://www.w3schools.com/'
browser.get(target_url)

# - 가능 여부에 대한 OK 받음
pass

# - html 파일 받음(and 확인)
html = browser.page_source

from selenium.webdriver.common.by import By

element_value = f'body'

element_body = browser.find_element(by=By.CSS_SELECTOR, value=element_value)
# element_body.send_keys(f'demonic19@nate.com')
from selenium.webdriver.common.keys import Keys
import time
for num in range(10):
    element_body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    element_body.send_keys(Keys.PAGE_UP)
    time.sleep(1)
    
pass
