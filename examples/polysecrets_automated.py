#! /usr/bin/env python3
from os import environ
import time, sys
from polysecrets import PolySecrets

"""Example of Polysecrets automated. """


CONTINUE_LOOP = True


def defaults():
    """
    default parameters:

    dict(
        secret='rAnd0m_s3cr3t',
        length=10,
        interval=30,  # (only if you're using automated)
        uuid=True,
        mixcase=False,
        persistence={}
    )
    :return: secret generated with default parameters, attached to the environment variable `secret`
    """
    config = {}
    automated = PolySecrets(config, clear_on_exit=True)
    try:
        automated.automated()
        time.sleep(2)  # give environment time to setup
        while CONTINUE_LOOP:
            print('Automated - Secret: ', environ['secret'])
            time.sleep(3)  # this would be a combination of 5 seconds plus + 3 seconds until next secret
    except KeyError as ke:
        print(f'KeyError - {ke}')
    finally:
        automated.terminate()


def length_with_default_params():
    """
    :return: secret length of 20 characters
    """
    config = dict(
        length=10,
        interval=5,
    )
    automated = PolySecrets(config, clear_on_exit=True)
    try:
        automated.automated()
        time.sleep(2)  # give environment time to setup
        while CONTINUE_LOOP:
            print('Automated - Secret: ', environ['secret'], f' | Length: {len(environ["secret"])}')
            time.sleep(3)  # this would be a combination of 5 seconds plus + 3 seconds until next secret
    except KeyError as ke:
        print(f'KeyError - {ke}')
    finally:
        automated.terminate()


def mixcase_with_length():
    """
    :return: secret length of 20 characters, with various characters being uppercase or lowercase -
    ** NOT guaranteed to be a full mix **
    """

    config = dict(
        length=20,
        interval=5,
        mixcase=True
    )
    automated = PolySecrets(config, clear_on_exit=True)
    try:
        automated.automated()
        time.sleep(2)  # give environment time to setup
        while CONTINUE_LOOP:
            print('Automated - Secret: ', environ['secret'])
            time.sleep(3)  # this would be a combination of 5 seconds plus + 3 seconds until next secret
    except KeyError as ke:
        print(f'KeyError - {ke}')
    finally:
        automated.terminate()


def uuid_mixcase_length():
    """
    Alphanumeric characters with varying cases and a final output secret length of 20 characters
    :return:
    """
    config = dict(
        length=20,
        interval=5,
        uuid=False,
        mixcase=True
    )
    automated = PolySecrets(config)
    try:
        automated.automated()
        time.sleep(2)  # give environment time to setup
        while CONTINUE_LOOP:
            print('Automated - Secret: ', environ['secret'], f' | Length: {len(environ["secret"])}')
            time.sleep(3)  # this would be a combination of 5 seconds plus + 3 seconds until next secret
    except KeyError as ke:
        print(f'KeyError - {ke}')
    finally:
        automated.terminate()


if __name__ == '__main__':
    print('[!] Remember to press CTRL + C to continue to and exit. [!]')
    avail_funcs = [defaults, length_with_default_params, mixcase_with_length, uuid_mixcase_length]
    print('Available Tests:\n')
    try:
        for index, func in enumerate(avail_funcs):
            print(f'{index}: {func.__name__}')
        option = input(f'\nSelect option: 0 - {len(avail_funcs) - 1} > ')
        if not option.isnumeric():
            print('Selection must be an integer.')
            sys.exit(1)
    except KeyboardInterrupt:
        sys.exit()
    try:
        print(f'Running {avail_funcs[int(option)].__name__} function...')
        avail_funcs[int(option)]()
    except KeyboardInterrupt:
        print(f'{avail_funcs[int(option)].__name__} terminated.')
        CONTINUE_LOOP = False
    finally:
        sys.exit()
