from uuid import uuid4
import random, time
from os import environ


class PolySecrets:
    def __init__(self, secret: str, sl_time: int = 30):
        self.secret = secret
        self.sl_time = sl_time
        # crypto secret
        self._one_uuid = str(uuid4())[:10]
        self._sec_phrase = self.secret
        self._sec_arr = []

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
