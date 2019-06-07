CONTINUE_LOOP = True

config = dict(
        secret='rAnd0m_s3cr3t',  # default
        length=10,  # default
        interval=30,  # default (only if you're using automated)
        uuid=True,  # default
        mixcase=False,  # default
        persist={}  # default
    )


def automated_example():
    """
    Example of Polysecrets automated. We're creating a new secret every 5 seconds,
    while we are getting the creating secret every 3 seconds. You will notice after
    5 seconds the secret will change. Lines 15, 17 and 24 are all you need in your
    actual application, the rest is for this example.
    :return:
    """
    from os import environ
    import time
    from polysecrets import PolySecrets

    automated = PolySecrets(config)
    try:
        automated.automated()
        time.sleep(2)  # give environment time to setup
        while CONTINUE_LOOP:
            print('Automated - Secret: ', environ['secret'])  # confirm secret is available
            time.sleep(3)
    except KeyError as ke:
        print(f'KeyError - {ke}')
    finally:
        automated.stop_automated()


def manual_example():
    """
    Example of Polysecrets manually. We're creating a one time secret from the provided
    secret string.
    :return:
    """
    from polysecrets import PolySecrets

    secret = PolySecrets(config).manual()
    print('Manual - Secret: ', secret)  # confirm secret is available


if __name__ == '__main__':
    try:
        automated_example()
    except KeyboardInterrupt:
        CONTINUE_LOOP = False
    manual_example()
