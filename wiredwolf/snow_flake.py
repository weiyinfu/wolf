import hashlib
import os
import socket
import threading
import time

"""
snowflake算法要点： 
* 记录lastTime，防止系统时钟错乱导致重复ID，如果发现lastTime大于当前时间则及时报警
* 记录currenttime，防止并发量太大导致产生重复ID，单位时间内产生的ID个数是有限的
* ID不要用64位，只用63位，因为Java中没有无符号整数。

UUID整合了时间、空间、ID信息，它的长度是128位，有点太长了。
snowflake可以看做精简版的UUID，它也包含时间、空间、ID三项信息。

"""
# 最高位空置
TIME = 32  # 32位的时间戳，以秒为单位，占据高32位（31~63），初始纪元为unix纪元（1970年，大约在2036年到期）
SPACE = 16  # 空间标识符，md5(机器域名+进程ID+线程ID)得到128位，取其前两个字节
ID = 15  # 可用的ID空间


def get_worker_id():
    worker_str = (
        socket.getfqdn() + str(os.getpid()) + str(threading.current_thread().ident)
    )
    md5 = hashlib.md5()
    md5.update(bytes(worker_str, "utf8"))
    res = md5.digest()
    return (res[0] << 8) | res[1]


class SnowFlake:
    def __init__(self):
        self.last_time = 0
        self.used = 0
        self.worker_id = get_worker_id()

    def get_id(self):
        # 时间差部分
        while 1:
            now = int(time.time())
            assert now >= self.last_time, "time run back"
            if now == self.last_time:
                if self.used == (1 << ID) - 1:  # 序列号满了就要睡一觉
                    time.sleep(0.1)
                    continue
                self.used += 1  # 同一时间差，序列号自增
            else:
                self.used = 0  # 不同时间差，序列号重新置为0
                self.last_time = now
            break
            # 自增序列号部分
        id_part = self.used  # 释放锁之前记录一下获取到的id号
        ans = 0
        ans |= now << (ID + SPACE)
        ans |= self.worker_id << ID
        ans |= id_part
        return ans
