"""Prototype for analyzing Subject 7"""

from typing import Callable
import random

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


def miller_rabin(z: int, number_trials: int) -> bool:
    """Test if a number is (probably) prime.

    Parameters
    ----------
    z : int
        The integer for which we test primality
    number_trials: int
        The number of rounds of testing to perform

    Returns
    -------
    bool
        True if the integer z is probably prime
    """


f_3 = one_way_function_factory(3)
print(f_3(10, 10))

# Ideas:
# - visualize f_p for a low value of p.
# - figure out if p is prime



