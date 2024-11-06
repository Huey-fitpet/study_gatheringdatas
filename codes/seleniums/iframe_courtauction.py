
# * 웹 크롤링 동작
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import time
import re
import pandas as pd
from pymongo import MongoClient

from insert_recode_in_mongo import connect_mongo

'''
target url = f'https://www.courtauction.go.kr/'
title tag = f'div.board-list > div > a'
indexFrame
#contents > div.table_contents > form > table > tbody > tr > td

한 레코드
#contents > div.table_contents > form > table > tbody > tr

한 레코드 사건번호
#contents > div.table_contents > form > table > tbody > tr > td > input[type=hidden]
#contents > div.table_contents > form:nth-child(1) > table > tbody > tr > td:nth-child(2)

한 레코드 소재지 내역
#contents > div.table_contents > form > table > tbody > tr > td:nth-child(4)

한 레코드 감정 평가액 
#contents > div.table_contents > form > table > tbody > tr > td.txtright

메인페이지 빠른 검색 리스트 
#idJiwonNm1

메인페이지 빠른 검색 버튼 
#main_btn > a

'''


webdriver_manager_directory = ChromeDriverManager().install() # 딱 한번 수행이라 밖에

class iframe_test : 
    # 쓸 때 browser 관리 
    def run(browser):

        target_url = f'https://www.courtauction.go.kr/'
        case_id_tag = f'#contents > div.table_contents > form:nth-child(1) > table > tbody > tr > td:nth-child(2)'
        property_address_tag = f'#contents > div.table_contents > form > table > tbody > tr > td:nth-child(4)'
        estimated_value_tag = f'#contents > div.table_contents > form > table > tbody > tr > td.txtright'
        btn_tag = f'#main_btn > a'
        sel_list_tag = f'#idJiwonNm1'

        # Chrome WebDriver의 capabilities 속성 사용
        capabilities = browser.capabilities

        # - 주소 입력(https://www.w3schools.com/)
        browser.get(target_url)
        
        # frame 선택 - 이게 되야 element 접근 가능
        browser.switch_to.frame("indexFrame")
        time.sleep(1)

        # 리스트 선택
        element_select = browser.find_element(by=By.CSS_SELECTOR, value=sel_list_tag)
        # Select 객체 생성
        select = Select(element_select)
        index = 8 # 인천 지방 법원
        select.select_by_index(index)
        time.sleep(1)

        # 클릭 넣기 
        element_btn = browser.find_element(by=By.CSS_SELECTOR, value=btn_tag)
        element_btn.click()
        time.sleep(1)
        
        case_id_list = browser.find_elements(by=By.CSS_SELECTOR, value=case_id_tag)
        property_address_list = browser.find_elements(by=By.CSS_SELECTOR, value=property_address_tag)
        estimated_value_list = browser.find_elements(by=By.CSS_SELECTOR, value=estimated_value_tag)
        
        case_data = {
            "case_id" : [],
            "property_address" : [],
            "estimated_value" : []
        }


        for number, row in enumerate(case_id_list):
            print(f'number:{number}, title : {row.accessible_name}')
            case_data["case_id"].append(row.accessible_name)
        
        for number, row in enumerate(property_address_list): # 한 번호당 여러개
            print(f'number:{number}, title : {row.accessible_name}')
           # 정규 표현식을 사용하여 데이터 자르기
            # 대괄호([])로 묶인 부분을 기준으로 자르기
            pattern = r'([^\[]*\[[^\]]*\])'
            matches = re.findall(pattern, row.accessible_name)

            # 결과를 리스트에 담기
            result_list = [match.strip() for match in matches]
            case_data["property_address"].append(result_list)

        for number, row in enumerate(estimated_value_list): # 한 번호당 여러개
            print(f'number:{number}, title : {row.accessible_name}')
            case_data["estimated_value"].append(row.accessible_name)

        return pd.DataFrame(case_data)


if __name__ == "__main__" :
    # ChromeDriver 실행
    browser = webdriver.Chrome(service=ChromeService(webdriver_manager_directory))
    # try - finally 자원 관리 필요 
    try:
        case_data = iframe_test.run(browser)
    except Exception as e :
        print(e)
    finally:
        browser.quit()

    # MongoDB 서버에 연결 : Both connect in case local and remote
    ip_add = f'mongodb://192.168.0.91:27017/'
    db_name = f'study_finance_shl'
    col_name = f'case_collection'
    client = MongoClient(ip_add)

    try:
        result_list = connect_mongo.insert_recode_in_mongo(client, db_name, col_name, case_data)
        print(f'insert id list count : {len(result_list.inserted_ids)}')
    except Exception as e :
        print(e)
    finally:
        client.close()
    pass