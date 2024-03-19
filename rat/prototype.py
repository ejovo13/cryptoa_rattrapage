"""Prototype for analyzing Subject 7"""

from typing import Callable
import random
import polars as pl
import numpy as np

from .exceptions import *

# p is 32 hexadecimal digits <=> 16 bytes <=> 128 bits
p = 0xd2bf071417608219223ad076131586a9
# z is 96 hexadecimal digits <=> 48 bytes <=>
z = 0x4520670aac4c7f5af9f86bed585d6066dcb73b9ec8c9b88536b46e252e64a1d28da6f8cf0d8bbf60fa6a4f8ee9854909

print(p)
print(z)


def one_way_function_factory(p: int) -> Callable[[int, int], int]:
    """Generate the one-way function f_p, as defined in subject 7."""
    p_cubed = p * p * p
    def f_p(x: int, y: int) -> int:
        return (x // y) % p_cubed

    return f_p

def miller_rabin_pretreatment(n: int) -> tuple[int, int]:
    """Compute two integers s and d such that n - 1 = 2**s * d.

    Returns
    -------
    (s, d) : tuple[int, int]
        A tuple of integers satisfying the equality n - 1 = 2**s * d

    Examples
    --------
    >>> miller_rabin_pretreatment(11)
    (1, 5)
    >>> miller_rabin_pretreatment(99)
    (1, 49)
    >>> miller_rabin_pretreatment(257)
    (8, 1)
    """
    n = n - 1
    s = 0

    while n % 2 == 0:
        n = n // 2
        s += 1

    return s, n


def miller_rabin(n: int, number_trials: int) -> bool:
    """Test if a number is (probably) prime.

    Adapted from https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test

    Parameters
    ----------
    n : int
        The integer for which we wish to test primality
    number_trials: int
        The number of rounds of testing to perform

    Returns
    -------
    bool
        True if the integer z is _probably_ prime

    Examples
    --------
    >>> miller_rabin(10, 5)
    False
    >>> miller_rabin(762515890128057700236061562369, 1)
    True
    >>> miller_rabin(93, 10)
    False
    >>> miller_rabin(97, 10)
    True
    """
    s, d = miller_rabin_pretreatment(n)
    for _ in range(number_trials):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        for _ in range(s):
            y = pow(x, 2, n)
            if y == 1 and x != 1 and x != n - 1:
                return False
            x = y
        if x != 1:
            return False
    return True


f_3 = one_way_function_factory(3)
print(f_3(10, 10))

# Ideas:
# - visualize f_p for a low value of p.
# - figure out if p is prime


big_prime = 762515890128057700236061562369
print(miller_rabin_pretreatment(big_prime))
print(miller_rabin(big_prime, 10))

print(miller_rabin(p, 100))


def explore_fp(p: int) -> pl.DataFrame:
    """Exhaustively compute the value of f_p for small values of p."""
    if p == 3:
        pass
    elif not miller_rabin(p, 10):
        raise NotPrimeError(p)

    f_p = one_way_function_factory(p)

    # Now we want to generate all possible inputs
    p_cubed = p**3

    xs = []
    ys = []
    fp = []

    for x in range(1, p_cubed):
        for y in range(1, p_cubed):
            xs.append(x)
            ys.append(y)
            fp.append(f_p(x, y))

    return pl.DataFrame(dict(
        x=xs,
        y=ys,
        z=fp
    ))

def visualize_fp(p: int) -> np.ndarray:
    if p == 3:
        pass
    elif not miller_rabin(p, 10):
        raise NotPrimeError(p)

    f_p = one_way_function_factory(p)

    # Now we want to generate all possible inputs
    p_cubed = p**3

    # xs = np.arange(1, p_cubed)
    # ys = np.arange(1, p_cubed)
    # xs, ys = np.meshgrid(xs, ys)
    fp = np.zeros((p_cubed - 1, p_cubed - 1))

    for i in range(1, p_cubed):
        for j in range(1, p_cubed):
            fp[i - 1, j - 1] = f_p(i, j)

    return fp