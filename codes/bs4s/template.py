






def main() :
    first = 30 
    second = 0

    try:
        result = first / second
        pass
    except Exception as e:
        result = first / 1
        print(e)
        pass

    return result

if __name__ == '__main__':
    main()
    pass