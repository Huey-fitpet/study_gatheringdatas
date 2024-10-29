
# from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class content_youtube:
    def run_content_from_youtube(browser):

        '''

        - 수집 데이터 mongodb에 insert
        - 항목 : 작성자, 작성일, 댓글, 좋아요와 싫어요 갯수
        - github, remote mongo uri 공유


        작성자 : #author-text > span
        작성일 : #published-time-text > a
        댓글 : #content-text > span
        좋아요 : #vote-count-middle
        싫어요 : 싫어요 갯수 출력하는 태그 없는 듯?

        '''

        # - html 파일 받음(and 확인)
        html = browser.page_source

        time.sleep(5)
        element_value = f'body'
        element_body = browser.find_element(by=By.CSS_SELECTOR, value=element_value)



        for num in range(15):
            time.sleep(1)
            element_body.send_keys(Keys.PAGE_DOWN)

        id_tag = f'#author-text > span'
        date_tag = f'#published-time-text > a'
        content_tag = f'#content-text > span'
        vote_cnt_tag = f'#vote-count-middle'

        ls_id = browser.find_elements(by=By.CSS_SELECTOR, value=id_tag)
        ls_date = browser.find_elements(by=By.CSS_SELECTOR, value=date_tag)
        ls_content = browser.find_elements(by=By.CSS_SELECTOR, value=content_tag)
        ls_vote_cnt = browser.find_elements(by=By.CSS_SELECTOR, value=vote_cnt_tag)

        ret_dict_list = []
        for num, (id, date, content, vote_cnt) in enumerate(zip(ls_id, ls_date, ls_content, ls_vote_cnt),start=1):

            # 각 댓글 정보를 딕셔너리로 저장
            comment_data = {
                'comment_count': num,
                'author': id.text,
                'date': date.text,
                'content': content.text,
                'vote_count': vote_cnt.text,
                'dislike_count' : f'0'
            }
            
            # 딕셔너리를 리스트에 추가
            ret_dict_list.append(comment_data)

            pass
        
        return ret_dict_list
pass
