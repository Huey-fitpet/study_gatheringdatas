
import get_classes


def main(message):
    count = 0
    while True:
        print(f'{message} : count - {count}')
        count += 1

        get_classes.getfuctions.message_print()
        get_classes.getfuctions.job_print()
        print(f'message : {get_classes.getfuctions.message}')

        pass
    
    return True


if __name__ == '__main__':
    main(f'task forever!')
