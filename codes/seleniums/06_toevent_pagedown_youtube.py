from selenium import webdriver
from selenium.webdriver.chrome.service import Service as CS
from webdriver_manager.chrome import ChromeDriverManager as CDM
from selenium.webdriver.chrome.options import Options # 정확히 뭐인지
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys # 내가 입력(input, 마치 마우스나 키보드 처럼) 할 것
from pymongo import MongoClient

import time # 내가 중간에 타임 슬립이나 이런걸 쓸 수도 있기에

client = MongoClient('mongodb://192.168.0.63:27017/') # 같은 주소에 갈거면 def 밖에 정해주고 쓰자 왜냐면 같은 곳으로 가니까


def insertDB(abcd): # 먼저 선언을 해야함, 왜냐하면 def를 먼저하고 해야지 아래의 것에서 올리기때문에, 아니 그렇게 어렵게 생각하기 어려우면 내가 왜 이거를 적었는지 확인해보자

    # 'mydatabase' 데이터베이스 선택 (없으면 자동 생성)
    db = client['joesDB']
    # 'users' 컬렉션 선택 (없으면 자동 생성)
    collection = db['YoutubeComments']

    DBresult = collection.insert_one(abcd) # insert_one과 many의 차이 또한 def는 그냥 선언이기에 안에 들어가는거는 위치를 나타내므로 아래 ()안에 있는 값이랑 같게 나와야함
    # 입력된 문서의 ID 출력
    print('Inserted user id:', DBresult.inserted_id)



# def insertDB_Many(abcd): 생각해보기.. one - 딕셔너리 > many는 one(딕셔너리)의 합 - 리스트
# 내가 몰랐던거: 스크롤은 바디 전체에 붙어있으니까 body라고 지정해야함, 그걸 어떻게 아느냐? 바디 줄이고 늘이면 바디에 따라 달라지기 때문에 댓글을 찾고 싶다고 댓글에서 뻘짓하지 말자.
# time.sleep을 안 걸었던거.. 이걸 어째 아나?

webdriver_manager_directory = CDM().install()

browser = webdriver.Chrome(service=CS(webdriver_manager_directory))

capabilities = browser.capabilities

browser.get("https://www.youtube.com/watch?v=XV81fqPTQhM")

html = browser.page_source
print(html)

time.sleep(5)

element_body = browser.find_element(by=By.CSS_SELECTOR, value='body') # 스크롤다운을 위한 body 전체


# for down_several_times in range(0,3):
#     element_body.send_keys(Keys.PAGE_DOWN)
#     time.sleep(1)  # 로딩 시간 대기

# 댓글 끝날 때 까지
# scroll 이전 값과 이후 값이 같으면 종료 
from selenium.webdriver import ActionChains as ac

current_height = 0
previous_height = 0
while True:
    # function chain 
    ac(browser).key_down(Keys.PAGE_DOWN).perform() # 브라우저를 선택해야해 # 탭별로 컨트롤 가능하기 때문
    # browser.implicitly_wait(50) # 로딩이 끝난걸 알아서 탐지 # sleep 보다 동작 느림 # handleless 방식도 있음
    time.sleep(1) 
    current_height = browser.execute_script(f'return document.documentElement.scrollTop')
    if previous_height == current_height:
        break
    previous_height = current_height #17604
    pass

pass
# results = []

# comment_body = browser.find_elements(by=By.CSS_SELECTOR, value='#main') #comments 요소

# for index, data_bundle in enumerate(comment_body):
#     comment_author_tag = f'#author-text > span'
#     comment_date_tag = f'#published-time-text > a'
#     comment_text_tag = f'#content-text > span'
#     comment_like_tag = f'#vote-count-middle'
#     time.sleep(5)
#     comment_author = data_bundle.find_element(By.CSS_SELECTOR, comment_author_tag)
#     comment_date = data_bundle.find_element(By.CSS_SELECTOR, comment_date_tag)
#     comment_text = data_bundle.find_element(By.CSS_SELECTOR, comment_text_tag)
#     comment_like = data_bundle.find_element(By.CSS_SELECTOR, comment_like_tag)
#     # indi_result = f'작성자 : {comment_author.text}, 
#     # 날짜 : {comment_date.text}, 내용 : 
#     # {comment_text.text}, 좋아요 수: 
#     # {comment_like.text}'
#     dic_result = {"Author" : comment_author.text, "Date" : comment_date.text, "Content" : comment_text.text, "Like" : comment_like.text}
    
#     results.append(dic_result)
#     print(results)
#     insertDB(dic_result)


pass
