
from datetime import datetime


message = f'in get functions'

def message_print():
    # 현재 시간을 UTC로 출력
    current_utc_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    print(f'message_print() : {current_utc_time}')
    return

def job_print():
    # 현재 시간을 UTC로 출력
    current_utc_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    print(f'job_print() : {current_utc_time}')
    return

pass