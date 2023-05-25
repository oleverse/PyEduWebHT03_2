import logging
import multiprocessing
from multiprocessing import Pool
from time import time

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


def factorize_distinct(number):
    potential_divider = number
    result = list()
    while potential_divider >= 1:
        if not (number % potential_divider):
            result.insert(0, potential_divider)
        potential_divider -= 1

    return result


def factorize(*number, synch=False):
    result = list()

    if synch:
        # cpu_count() call is unnecessary, Pool uses all cores by default
        pool = Pool(multiprocessing.cpu_count())
        async_results = [pool.apply_async(factorize_distinct, (n,)) for n in number]

        for async_res in async_results:
            result.append(async_res.get())

        return tuple(result)

    else:
        for n in number:
            result.append(factorize_distinct(n))

        return tuple(result)


start = time()
a, b, c, d = factorize(128, 255, 99999, 10651060, synch=True)
logger.debug(f"Aynchronous time: {time() - start} s")

assert a == [1, 2, 4, 8, 16, 32, 64, 128]
assert b == [1, 3, 5, 15, 17, 51, 85, 255]
assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

start = time()
a, b, c, d = factorize(128, 255, 99999, 10651060)
logger.debug(f"Synchronous time: {time() - start} s")

assert a == [1, 2, 4, 8, 16, 32, 64, 128]
assert b == [1, 3, 5, 15, 17, 51, 85, 255]
assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
