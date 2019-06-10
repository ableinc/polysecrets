from uuid import uuid4
import random, time, sys, threading, atexit
from os import environ
from datetime import datetime


class PolySecrets:
    def __init__(self, config: dict, clear_on_exit: bool = False):
        """
        A completely randomized order of secrets; built with security in mind.
        :param config: Configuration object
        """
        self.__os__()
        # variables
        self.config = self.__config__(config)
        # automated process
        self._thread = threading.Thread(target=self.__automated, args=())
        self._thread.daemon = True
        self._RUN_THREAD = True
        # crypto secret
        self._one_uuid = str(uuid4())[:15]
        self._alpha_numeric_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                                    'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6',
                                    '7', '8', '9']
        self._sec_phrase = self.config['secret']
        self._sec_arr = []
        if clear_on_exit and isinstance(clear_on_exit, bool):
            atexit.register(environ.clear)

    @staticmethod
    def __config__(obj):
        _defaults = {'automated': False, 'interval': 30, 'length': 10, 'uuid': True, 'mixcase': False,
                     'secret': 'rAnd0m_s3cr3t', 'verbose': True, 'persistence': {'host': 'localhost', 'port': 27017,
                                                                                 'db': 'polysecrets',
                                                                                 'collection': 'secrets'}}
        bad = False
        last_key = None
        for key in _defaults.keys():
            try:
                last_key = key
                if obj[key]:
                    if not isinstance(obj[key], type(_defaults[key])):
                        print(f'{obj[key]} has invalid type. You should have {type(_defaults[key])}, '
                              f'but you have you {type(_defaults[key])}.')
                        return bad
            except KeyError:
                obj[last_key] = _defaults[last_key]
                # for key, value in _defaults.items():
                #     obj[key] = value
        if len(obj['persistence'].keys()) > 0:
            for _key in _defaults['persistence'].keys():
                if obj['persistence'][_key]:
                    if not isinstance(obj['persistence'][_key], type(_defaults['persistence'][_key])):
                        print(f'{obj[_key]} has invalid type. You should have {type(_defaults[_key])}, '
                              f'but you have you {type(_defaults[_key])}.')
                        return bad
        else:
            obj['persistence'] = False
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

    def __persistence(self, secret):
        from pymongo import MongoClient

        client = None
        if 'mongod://' in self.config['persistence']['host']:
            client = MongoClient(self.config['persistence']['host'])
        else:
            client = MongoClient(host=self.config['persistence']['host'], port=self.config['persistence']['port'])
        db = client[self.config['persistence']['db']]
        collection = db[self.config['persistence']['collection']]
        _prev_used_secret = collection.find_one({'secret': secret})
        collection.insert_one({'secret': secret, 'createdAt': datetime.now()})
        if _prev_used_secret is not None:
            return False
        return secret

    def __randomization(self, arr, lst, return_val: bool = False):
        switcher = ['upper', 'lower', 'upper', 'lower', 'upper', 'lower']  # increase probability
        random_item_from_list = str(random.choice(lst))
        case_state = random.choice(switcher)
        upper_case = ''
        if self.config['mixcase']:
            if not random_item_from_list.isnumeric() and case_state == 'upper':
                upper_case = random_item_from_list.upper()
        if return_val:
            if upper_case is not '':
                return arr.append(upper_case)
            else:
                return arr.append(random_item_from_list)
        if upper_case is not '':
            arr.append(upper_case)
        else:
            arr.append(random_item_from_list)

    def __length_confirmation__(self, final_secret):
        if len(final_secret) < self.config['length']:
            for _ in range(self.config['length'] - len(final_secret)):
                self.__randomization(self._sec_arr, self._alpha_numeric_list)
            return str(''.join(self._sec_arr))[:self.config['length']]
        return final_secret

    def __secret_generator(self):
        for _ in range(len(self._sec_phrase)):
            self.__randomization(self._sec_arr, self._sec_phrase)
            if self.config['uuid'] is True:
                self.__randomization(self._sec_arr, self._one_uuid)
            elif self.config['uuid'] is False:
                self.__randomization(self._sec_arr, self._alpha_numeric_list)
            else:
                self.__randomization(self._sec_arr, self._one_uuid)
                self.__randomization(self._sec_arr, self._alpha_numeric_list)
        _final_secret = self.__length_confirmation__(str(''.join(self._sec_arr))[:self.config['length']])
        self._sec_arr.clear()
        return _final_secret

    def __automated(self):
        _secret = None
        _INVALID_SECRET = True
        while self._RUN_THREAD:
            self._one_uuid = str(uuid4())[:15]
            if self.config['persistence'] is not False:
                while _INVALID_SECRET:
                    _secret = self.__persistence(self.__secret_generator())
                    if _secret: _INVALID_SECRET = False
                environ['secret'] = _secret
                time.sleep(self.config['interval'])
                _INVALID_SECRET = True
            else:
                environ['secret'] = self.__secret_generator()
                time.sleep(self.config['interval'])

    def manual(self):
        _INVALID_SECRET = True
        _secret = None
        if self.config['persistence'] is not False:
            while _INVALID_SECRET:
                _secret = self.__persistence(self.__secret_generator())
                if _secret: _INVALID_SECRET = False
            return _secret
        else:
            return self.__secret_generator()

    def automated(self):
        self._thread.start()

    def stop_automated(self):
        self._RUN_THREAD = False
