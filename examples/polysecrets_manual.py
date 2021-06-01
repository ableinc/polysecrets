#! /usr/bin/env python3
from polysecrets import PolySecrets
import sys, time

"""Example of Polysecrets manually. """


def defaults():
    """
    Get secret with default parameters:

    dict(
        secret='rAn!d0m_@s3cr#3t+',
        length=10,
        interval=30,  # (only if you're using automated)
        uuid=True,
        mixcase=False,
        persistence={}
    )
    :return:
    """
    config = {}
    secret = PolySecrets(config).manual()
    print('[!] Secret: ', secret)  # confirm secret is available


def length_with_default_params():
    """
    :return: secret length of 20 characters; with default params
    """
    config = dict(
        length=20,
    )
    secret = PolySecrets(config).manual()
    print('[!] Secret: ', secret, f'Length: {len(secret)}')  # confirm secret is available


def mixcase_with_length():
    """
    :return: secret with length of 20 and mix of upper and lowercase lettering
    """
    config = dict(
        length=20,
        mixcase=True
    )
    secret = PolySecrets(config).manual()
    print('[!] Secret: ', secret, f' | Length: {len(secret)}')  # confirm secret is available


def uuid_mixcase_length():
    """
    :return: Alphanumeric characters & UUIDs, with varying cases and a final output secret length of 20 characters
    """
    config = dict(
        length=20,
        uuid='Both',
        mixcase=True
    )
    secret = PolySecrets(config).manual()
    print('[!] Secret: ', secret, f' | Length: {len(secret)}')  # confirm secret is available


if __name__ == '__main__':
    print('[!] press CTRL + C to terminate process [!]')
    for func in [defaults, length_with_default_params, mixcase_with_length, uuid_mixcase_length]:
        try:
            print(f'Running {func.__name__} function...')
            func()
            time.sleep(3)
        except KeyboardInterrupt:
            print(f'{func.__name__} terminated.')
            if input('exit ? (y/n) ').lower() == 'y':
                sys.exit()
            else:
                continue

