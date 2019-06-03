from uuid import uuid4
import random, time,sys
from os import environ


class PolySecrets:
    def __init__(self, secret: str, sl_time: int = 30):
        self.__os__()
        self.secret = secret
        self.sl_time = sl_time
        # crypto secret
        self._one_uuid = str(uuid4())[:10]
        self._sec_phrase = self.secret
        self._sec_arr = []

    @staticmethod
    def __os__():
        platforms = {
            'darwin': (3, 6),
            'linux': (3, 6),
            'windows': (3, 6)
        }
        platform_version = platforms.get(sys.platform, 'N/A')
        if platform_version == 'N/A':
            print('MacOS, Linux or Windows running Python 3.6 or higher is required.')
            sys.exit()

        if not sys.version_info >= platform_version:
            print('MacOS, Linux or Windows running Python 3.6 or higher is required.')
            sys.exit()

    def __randomization(self, automated: bool = False):
        for _ in range(len(self._sec_phrase)):
            self._sec_arr.append(random.choice(self._sec_phrase))
            self._sec_arr.append(random.choice(self._one_uuid))
        if not automated:
            return ''.join(self._sec_arr)
        environ['secret'] = ''.join(self._sec_arr)

    def __automated(self):
        while True:
            self._one_uuid = str(uuid4())[:10]
            self.__randomization(True)
            time.sleep(self.sl_time)

    def manual(self):
        return self.__randomization()

    def automated(self):
        self.__automated()
