from spyder import *
import threading
import datetime
import time
import multiprocessing

def myfunc(d):
    print(d)

# 计算日期
d1 = datetime.datetime.strptime('2023-6-18', '%Y-%m-%d')
d2 = datetime.datetime.today()
tmp = d1.month

pool = multiprocessing.Pool(processes=15)
while d1 <= d2:
    pool.apply_async(func=spy_news, args=(d1.year, d1.month, d1.day,))
    time.sleep(3)
    # spy_news(d1.year, d1.month, d1.day)
    d1 += datetime.timedelta(days=1)
pool.close()
pool.join()

