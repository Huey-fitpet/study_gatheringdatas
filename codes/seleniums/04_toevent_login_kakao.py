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
target_url = f'https://accounts.kakao.com/login/?continue=https%3A%2F%2Fwww.daum.net#login'
browser.get(target_url)

# - 가능 여부에 대한 OK 받음
pass

# - html 파일 받음(and 확인)
html = browser.page_source

from selenium.webdriver.common.by import By

# input : #loginId--1
# input : #password--2
# click or not : #recaptcha-anchor > div.recaptcha-checkbox-border
# click : button.btn_g.highlight.submit

id_tag = f'#loginId--1'
pw_tag = f'#password--2'
btn_tag = f'button.btn_g.highlight.submit'
is_robot_tag = f'#recaptcha-anchor > div.recaptcha-checkbox-border'

element_id = browser.find_element(by=By.CSS_SELECTOR, value=id_tag)
element_id.send_keys(f'demonic19@nate.com')

element_pw = browser.find_element(by=By.CSS_SELECTOR, value=pw_tag)
element_pw.send_keys(f'1111')

element_btn = browser.find_element(by=By.CSS_SELECTOR, value=btn_tag)
element_btn.click()

try:
    element_is_robot = browser.find_element(by=By.CSS_SELECTOR, value=is_robot_tag)
    element_is_robot.click()
    pass
except Exception as e:
    pass

element_btn = browser.find_element(by=By.CSS_SELECTOR, value=btn_tag)
element_btn.click()

pass
