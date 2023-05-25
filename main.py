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


def factorize(*number):
    result = list()

    for n in number:
        result.append(factorize_distinct(n))

    return tuple(result)


def is_divided(arg_pair):
    number, divider = arg_pair
    if not number % divider:
        return divider


def factorize_async(*number):
    result = list()

    pool = Pool(50)
    for n in number:
        res = pool.map(is_divided, [(n, divider) for divider in range(1, n+1)])
        result.append(list(filter(lambda r: r is not None, res)))

    return tuple(result)


if __name__ == "__main__":
    start = time()
    a, b, c, d = factorize_async(128, 255, 99999, 10651060)
    logger.debug(f"Aynchronous time: {time() - start} s")

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                 1521580, 2130212, 2662765, 5325530, 10651060]

    start = time()
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    logger.debug(f"Synchronous time: {time() - start} s")

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                 1521580, 2130212, 2662765, 5325530, 10651060]
