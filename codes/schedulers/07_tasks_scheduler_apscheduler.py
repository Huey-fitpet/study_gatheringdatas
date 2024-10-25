
from get_classes import getfuctions as gf
from apscheduler.schedulers.background import BackgroundScheduler

def main(message):

    # 스케쥴러 등록 
    


    # 정지 예방
    count = 0
    while True:
        print(f'{message} : count - {count}')
        count += 1

        pass
    
    return True


if __name__ == '__main__':
    main(f'task forever!')
