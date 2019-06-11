from os import environ
from polysecrets import PolySecrets
import time

CONTINUE_LOOP = True


def automated_example():
    """
    Final output: secret length of 20 characters, with various characters being uppercase or lowercase -
    ** NOT guaranteed to be a full mix **
    :return:
    """
    config = dict(
        length=20,  # default
        interval=5,  # default (only if you're using automated)
        mixcase=True
    )
    automated = PolySecrets(config)
    try:
        automated.automated()
        time.sleep(2)  # give environment time to setup
        while CONTINUE_LOOP:
            print('Automated - Secret: ', environ['secret'], f' | Length: {len(environ["secret"])}')  # confirm secret is available
            time.sleep(3)
    except KeyError as ke:
        print(f'KeyError - {ke}')
    finally:
        automated.terminate()


def manual_example():
    """
    Final output: secret length of 20 characters, with various characters being uppercase or lowercase -
    ** NOT guaranteed to be a full mix **
    :return:
    """
    config = dict(
        length=20,
        mixcase=True
    )
    secret = PolySecrets(config).manual()
    print('Manual - Secret: ', secret, f' | Length: {len(secret)}')  # confirm secret is available


if __name__ == '__main__':
    try:
        automated_example()
    except KeyboardInterrupt:
        CONTINUE_LOOP = False
    manual_example()
