
from get_classes import getfuctions as gf


def main(message):
    count = 0
    while True:
        print(f'{message} : count - {count}')
        count += 1

        gf.message_print()
        gf.job_print()
        print(f'message : {gf.message}')

        pass
    
    return True


if __name__ == '__main__':
    main(f'task forever!')
