
import get_functions


def main(message):
    count = 0
    while True:
        print(f'{message} : count - {count}')
        count += 1

        get_functions.message_print()
        get_functions.job_print()
        print(f'{get_functions.message} : count - {count}')
        
        pass
    
    return True


if __name__ == '__main__':
    main(f'task forever!')
