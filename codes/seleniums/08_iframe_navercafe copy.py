
# * 웹 크롤링 동작
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

'''
target url = f'https://cafe.naver.com/sbabellows?iframe_url=/MyCafeIntro.nhn%3Fclubid=26638342'
target url = f'https://cafe.naver.com/sbabellows'
title tag = f'div.board-list > div > a'

'''

webdriver_manager_directory = ChromeDriverManager().install() # 딱 한번 수행이라 밖에

class iframe_test : 
    # 쓸 때 browser 관리 
    def run():

        target_url = f'https://cafe.naver.com/sbabellows'
        title_tag = f'div.board-list > div > a'

        # ChromeDriver 실행
        browser = webdriver.Chrome(service=ChromeService(webdriver_manager_directory))

        # Chrome WebDriver의 capabilities 속성 사용
        capabilities = browser.capabilities

        # - 주소 입력(https://www.w3schools.com/)
        browser.get(target_url)
        
        # 나중에 클릭 넣기 

        browser.switch_to.frame("cafe_main")
        time.sleep(2)
        cafe_list = browser.find_elements(by=By.CSS_SELECTOR, value=title_tag)
        
        for number, row in enumerate(cafe_list):
            print(f'number:{number}, title : {row.text}')
            
        pass


if __name__ == "__main__" :
    iframe_test.run()
    pass