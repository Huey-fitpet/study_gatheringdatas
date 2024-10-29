
# 각 기능별 func들 묶어놓은 class
from toevent_pagemove_youtube import content_youtube as cy
from insert_recode_in_mongo import connect_mongo as cm

# * 웹 크롤링 동작
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# mongo DB 동작
from pymongo import MongoClient

def main():

    ip_add = f'mongodb://192.168.0.63:27017/'
    db_name = f'youtube_db_sanghoonlee'
    col_name = f'youtube_col_sanghoonlee'

    webdriver_manager_directory = ChromeDriverManager().install()

    # ChromeDriver 실행
    browser = webdriver.Chrome(service=ChromeService(webdriver_manager_directory))

    # Chrome WebDriver의 capabilities 속성 사용
    capabilities = browser.capabilities

    # - 주소 입력(https://www.w3schools.com/)
    target_url = f'https://www.youtube.com/watch?v=iQZCVbseEMQ'
    browser.get(target_url)

    # - 가능 여부에 대한 OK 받음

    content_lists = cy.run_content_from_youtube(browser)

    if content_lists: # 값이 있다면 돌았을 것, 돌았는데 값이 없는 경우 처리만 더 생각하면 됨.
        browser.quit()

    # MongoDB 서버에 연결 : Both connect in case local and remote
    client = MongoClient(ip_add)

    result_list = cm.insert_recode_in_mongo(client, db_name, col_name, content_lists)

    client.close()
    print(f'insert id list count : {len(result_list.inserted_ids)}')
    pass


if __name__ == '__main__':
    main()
    pass