
# 각 기능별 func들 묶어놓은 class
from pagenations_lottemalls import ProductInfoScraper as ps
from insert_recode_in_mongo import connect_mongo as cm

# * 웹 크롤링 동작
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# mongo DB 동작
from pymongo import MongoClient

def main():

    ip_add = f'mongodb://192.168.0.91:27017/'
    db_name = f'lotte_db_sanghoonlee'
    col_name = f'lotte_col_sanghoonlee'

    webdriver_manager_directory = ChromeDriverManager().install()

    # ChromeDriver 실행
    browser = webdriver.Chrome(service=ChromeService(webdriver_manager_directory))

    # Chrome WebDriver의 capabilities 속성 사용
    capabilities = browser.capabilities

    # - 주소 입력(https://www.w3schools.com/)
    # 롯데몰 메인 페이지 
    target_url = f'https://www.lotteon.com/p/display/main/lotteon?mall_no=1'
    browser.get(target_url)

    # - 가능 여부에 대한 OK 받음
    try:
        content_lists = ps.get_product_info(browser)
    except Exception as e :
        print(e)
    finally:
        browser.quit()

    # MongoDB 서버에 연결 : Both connect in case local and remote
    client = MongoClient(ip_add)

    try:
        result_list = cm.insert_recode_in_mongo(client, db_name, col_name, content_lists)
    except Exception as e :
        print(e)
    finally:
        client.close()
    print(f'insert id list count : {len(result_list.inserted_ids)}')
    pass


if __name__ == '__main__':
    main()
    pass