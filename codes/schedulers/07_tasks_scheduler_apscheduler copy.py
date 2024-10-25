
from get_classes import getfuctions as gf
from apscheduler.schedulers.background import BackgroundScheduler

import time

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
    
    scheduler.start()
    # 정지 예방
    count = 0
    while True:
        time.sleep(1)
        print(f'{message} : count - {count}')
        count += 1

        pass
    
    return True


if __name__ == '__main__':
    main(f'task forever!')
