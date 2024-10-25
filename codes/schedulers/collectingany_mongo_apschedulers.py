
from get_classes import getfuctions as gf
from apscheduler.schedulers.background import BackgroundScheduler

import time

import webscraping_imglink_func as wf_img
import webscraping_newscontent_func as wf_news

def main(message):

    # 스케쥴러 등록 
    scheduler = BackgroundScheduler()
    scheduler.add_job(gf.message_print, 
                      trigger='interval', 
                      seconds=1, 
                      coalesce=True, 
                      max_instances=1 )

    scheduler.add_job(gf.job_print, 
                      trigger='interval', 
                      seconds=1, 
                      coalesce=True, 
                      max_instances=1 )
    

    ip_add = f'mongodb://192.168.0.63:27017/'
    db_name = f'img_database_sanghoonlee'
    col_name = f'img_collection_sanghoonlee'
    folder = f'./downloads'
    url = f'https://www.yna.co.kr/economy/all'

    args_list = [ip_add,db_name,col_name,folder,url]

    scheduler.add_job(wf_img.main, 
                      trigger='interval', 
                      seconds=5, 
                      coalesce=True, 
                      max_instances=1,
                      args=[args_list]
                      )
    
    ip_add = f'mongodb://192.168.0.63:27017/'
    db_name = f'news_database_sanghoonlee'
    col_name = f'news_collection_sanghoonlee'
    #folder = f'./downloads'
    #url = f'https://www.yna.co.kr/economy/all'

    args_list = [ip_add,db_name,col_name,folder,url] # wf_news는 folder,url 적용 안됨

    scheduler.add_job(wf_news.main, 
                      trigger='interval', 
                      seconds=5, 
                      coalesce=True, 
                      max_instances=1,
                      args=[args_list]
                      )
    
    scheduler.start()
    # 정지 예방
    count = 0
    while True:
        #time.sleep(3)
        #print(f'{message} : count - {count}')
        #count += 1

        pass
    
    return True


if __name__ == '__main__':
    main(f'task forever!')
