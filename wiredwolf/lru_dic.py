from collections import OrderedDict
from time import time, sleep

"""
最近最少使用dict，定期删除元素
"""


class LruDic:
    def __init__(self, timeout: int):
        self.a = OrderedDict()
        self.timeout = timeout

    def _remove_old(self):
        removing = []
        for k, (v, t) in self.a.items():
            if time() - t >= self.timeout:
                removing.append(k)
            else:
                break
        print(self.a)
        for k in removing:
            del self.a[k]

    def _update(self, k):
        # 更新k
        if k not in self.a:
            return
        v, t = self.a[k]
        self.a[k] = (v, time())

    def set(self, k, v):
        self.a[k] = (v, time())
        self._update(k)
        self._remove_old()

    def get(self, k):
        if k not in self.a:
            return None
        self._update(k)
        return self.a[k][0]


if __name__ == '__main__':
    x = LruDic(timeout=3)
    x.set(3, 5)
    assert x.get(3) == 5
    sleep(4)
    x.set(4, 5)  # set操作会触发删除key=3的操作
    assert x.get(3) is None
    assert x.get(4) == 5
