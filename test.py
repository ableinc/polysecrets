CONTINUE_LOOP = True


def automated_example():
    from os import environ
    import time
    from polysecrets import PolySecrets

    PolySecrets('rAnd0m_s3cr3t', 15).automated()  # default time is set to 30 seconds
    while CONTINUE_LOOP:
        print('Automated - Secret: ', environ['secret'])  # confirm secret is available
        time.sleep(3)


def manual_example():
    from polysecrets import PolySecrets

    secret = PolySecrets('rAnd0m_s3cr3t').manual()
    print('Manual - Secret: ', secret)  # confirm secret is available


if __name__ == '__main__':
    try:
        automated_example()
    except KeyboardInterrupt:
        CONTINUE_LOOP = False
    manual_example()
