from uuid import uuid4
import random, time, sys, threading, atexit
from os import environ
from pymongo import MongoClient


class PolySecrets:
    def __init__(self, config: dict, interval: int = 30):
        """
        A completely randomized order of secrets; built with security in mind.
        :param config: Configuration object
        """
        self.__os__()
        self.__reqs__(config['secret'], config['length'])
        # variables
        _config = dict(
            secret=config['secret'],
            interval=interval,
            length=config['length'],
            uuids=config['uuids'],
            mix_case=config['mixcase'],
            persist=config['persist']
        )
        self.config = self.__config__(_config)
        # automated process
        self._thread = threading.Thread(target=self.__automated, args=())
        self._thread.daemon = True
        self._RUN_THREAD = True
        # crypto secret
        self._one_uuid = str(uuid4())[:15]
        self._alpha_numeric_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                                    'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6',
                                    '7', '8', '9']
        self._sec_phrase = config['secret']
        self._sec_arr = []
        atexit.register(environ.clear)

    @staticmethod
    def __config__(obj):
        if not isinstance(obj, dict):
            print(f'Configs must be an object. You have {type(obj)}, which is invalid.')
            return
        _uuids = {
            0: False,
            1: True,
            2: 'Both'
        }.get(obj['_uuid'], 'N/A')
        if _uuids is 'N/A': return
        obj['_uuid'] = _uuids
        return obj

    @staticmethod
    def __os__():
        platforms = {
            'darwin': (3, 5),
            'linux': (3, 5),
            'windows': (3, 5)
        }
        platform_version = platforms.get(sys.platform, 'N/A')
        if platform_version == 'N/A' or not sys.version_info >= platform_version:
            print('MacOS, Linux or Windows running Python 3.5 or higher is required.')
            return

    @staticmethod
    def __reqs__(secret, length):
        if len(secret) < 10:
            print(f'A secret of 10 characters or more is required. You secret has {len(secret)} characters.')
            return
        elif length < 10:
            print(f'The length of the secret must be of 10 or more. You set your length to {length}, '
                  f'this is invalid.')
            return

    def __randomization(self, arr, lst, return_val: bool = False):
        switcher = ['upper', 'lower', 'upper', 'lower', 'upper', 'lower']  # increase probability
        random_item_from_list = str(random.choice(lst))
        case_state = random.choice(switcher)
        if self.config['mix_case']:
            if not random_item_from_list.isnumeric() and case_state == 'upper':
                random_item_from_list.upper()
        if return_val:
            return arr.append(random_item_from_list)
        arr.append(random_item_from_list)

    def __length_confirmation__(self, final_secret):
        if len(final_secret) < self.config['length']:
            for _ in range(self.config['length'] - len(final_secret)):
                self.__randomization(self._sec_arr, self._alpha_numeric_list)
            return str(''.join(self._sec_arr))[:self.config['length']]
        return final_secret

    def __secret_generator(self, automated: bool = False):
        for _ in range(len(self._sec_phrase)):
            self.__randomization(self._sec_arr, self._sec_phrase)
            if self.config['uuids'] is True:
                self.__randomization(self._sec_arr, self._one_uuid)
            elif self.config['uuids'] is False:
                self.__randomization(self._sec_arr, self._alpha_numeric_list)
            else:
                self.__randomization(self._sec_arr, self._one_uuid)
                self.__randomization(self._sec_arr, self._alpha_numeric_list)
        _final_secret = str(''.join(self._sec_arr))[:self.config['length']]
        if not automated:
            return self.__length_confirmation__(_final_secret)
        environ['secret'] = self.__length_confirmation__(_final_secret)
        self._sec_arr.clear()

    def __automated(self):
        while self._RUN_THREAD:
            self._one_uuid = str(uuid4())[:15]
            self.__secret_generator(True)
            time.sleep(self.config['interval'])

    def manual(self):
        return self.__secret_generator()

    def automated(self):
        self._thread.start()

    def stop_automated(self):
        self._RUN_THREAD = False
