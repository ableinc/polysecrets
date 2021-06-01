from uuid import uuid4
import random, time, sys, threading, platform
from os import environ
from datetime import datetime


class PolySecrets:
    def __init__(self, config: dict, clear_on_exit: bool = False):
        """
        A completely randomized order of secrets; built with security in mind.
        :param config: Configuration object
        """
        self.__os__()
        # Alpha
        self._alpha_numeric_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                                    'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6',
                                    '7', '8', '9']
        # variables
        self.config = self.__config__(config)
        self._clear_on_exit = clear_on_exit
        # automated process
        self._thread = threading.Thread(target=self.__automated, args=())
        self._thread.daemon = True
        self._RUN_THREAD = True
        # crypto secret
        self._one_uuid = str(uuid4())[:15]
        self._sec_phrase = self.config['secret']
        self._sec_arr = []

    @staticmethod
    def type_error_notifier(key, defaults):
        print('TypeError with parameters: ')
        print(f'{key} has invalid type. You should have {defaults[key]}, '
              f'but you have you {defaults[key]}.')
        sys.exit(1)

    def __config__(self, obj):
        if obj['symbols'] == True:
            self._alpha_numeric_list.append(['!', '@', '#', '$', '_', '+', '-'])
        
        _defaults = {'interval': int, 'length': int, 'uuid': str, 'mixcase': bool,
                     'secret': str, 'persist': bool, 'symbols': bool}
        ignore_keys = []
        for key in obj.keys():
            if not isinstance(obj[key], _defaults[key]):
                self.type_error_notifier(key, _defaults)
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
            print('MacOS, Linux or Windows running Python 3.5 or higher is required. Your Python version: ', platform.python_version())
            sys.exit(100)

    def __persistence(self, secret):
        from pymongo import MongoClient
        from pydotenvs import load_env
        load_env()
        try:
            persist = {'host': environ['HOST'],
                        'port': environ['PORT'] if environ['PORT'] != '' else 27017,
                        'db': environ['DB_NAME'] if environ['DB_NAME'] != '' else 'polysecrets',
                        'collection': environ['secrets'] if environ['secrets'] != '' else 'secrets',
                        'user': environ['DB_USER'],
                        'pass': environ['DB_PASS'],
                        'authSource': environ['AUTH_SOURCE'] if environ['AUTH_SOURCE'] != '' else 'admin'
                        }
            if 'mongod://' in persist['host']:
                client = MongoClient(persist['host'])
            else:
                client = MongoClient(host=persist['host'],
                                    port=persist['port'],
                                    username=persist['user'],
                                    password=persist['pass'],
                                    authSource=persist['authSource'])
            db = client[persist['db']]
            collection = db[persist['collection']]
            _prev_used_secret = collection.find_one({'secret': secret})
            if _prev_used_secret is not None:
                return False
            collection.insert_one({'secret': secret, 'createdAt': datetime.now()})
            return secret
        except KeyError as ke:
            print('Unable to parse .env file for MongoDB credentials. Error: ', ke, 'environment variable could not be found.')
            sys.exit(200)

    def __randomization(self, arr, lst, return_val: bool = False):
        switcher = ['upper', 'lower', 'upper', 'lower', 'upper', 'lower']  # increase probability
        random_item_from_list = str(random.choice(lst))
        case_state = random.choice(switcher)
        upper_case = ''
        if self.config['mixcase']:
            if not random_item_from_list.isnumeric() and case_state == 'upper':
                upper_case = random_item_from_list.upper()
        if upper_case is not '':
            if return_val:
                return arr.append(upper_case)
            arr.append(upper_case)
        else:
            arr.append(random_item_from_list)

    def __length_confirmation__(self, final_secret):
        if len(final_secret) < self.config['length']:
            for _ in range(self.config['length'] - len(final_secret)):
                self.__randomization(self._sec_arr, self._alpha_numeric_list)
            return str(''.join(self._sec_arr))[0:self.config['length']]
        return final_secret

    def __secret_generator(self):
        for _ in range(len(self._sec_phrase)):
            self.__randomization(self._sec_arr, self._sec_phrase)
            if self.config['uuid'] is 'yes':
                self.__randomization(self._sec_arr, self._one_uuid)
            elif self.config['uuid'] is 'no':
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
            if self.config['persist'] == True:
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
        try:
            if self.config['persist'] == True:
                while _INVALID_SECRET:
                    _secret = self.__persistence(self.__secret_generator())
                    if _secret: _INVALID_SECRET = False
                return _secret
            else:
                raise KeyError('Invalid key')
        except KeyError:
            return self.__secret_generator()

    def automated(self):
        try:
            self._thread.start()
        except threading.ThreadError:
            raise threading.ThreadError()
        except KeyError:
            print('Fatal error during thread.')
            sys.exit(1)

    def terminate(self):
        self._RUN_THREAD = False
        if self._clear_on_exit:
            environ.pop('secret')
