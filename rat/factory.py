"""Factory class for our hash function."""

from typing import Callable, Iterable
from .number_theory import *

class HashFn:
    """Implementation of schema 7."""

    def __init__(self, p: int):

        self.p = p
        self.p3 = pow(p, 3)

        self.prime = miller_rabin(p, 15)

        if self.prime:
            self.__call__ = fp_prime(p)
        else:
            self.__call__ = fp_composite(p)


    def multiplicative_group(self) -> Iterable[int]:
        """Return an _iterable_ across all elements in Zp*."""
        if self.prime:
            return range(1, self.p)
        else:
            return filter(
                lambda n: iscoprime(n, self.p),
                range(1, self.p)
            )

    def multiplicative_group_list(self) -> list[int]:
        """Return Zp* as a list."""
        return list(self.multiplicative_group())

    def totient_p(self) -> int:
        """Return Euler's totient function for `self.p`."""
        if self.prime:
            return self.p - 1
        else:
            return totient(self.p)

    def totient_p3(self) -> int:
        """Return the value of the totient function of p3."""
        totient_p = self.totient_p()
        return pow(totient_p, 2) * totient_p

    def inv_p3(self, y: int) -> int:
        """Return the multiplicative inverse of y in Zp3*."""
        return modular_inverse(self.totient_p3(), y, self.p3)

    def inv_p3_image(self) -> Iterable[int]:
        """Return the image of self.inv_p3 for all p in Zp*."""
        return (self.inv_p3(y) for y in self.multiplicative_group())

    def inv_p3_image_list(self) -> list[int]:
        return list(self.inv_p3_image())


# ---------------------------------------------------------------------------- #
#                               Utility Functions                              #
# ---------------------------------------------------------------------------- #
def fp_prime(p: int) -> Callable[[int, int], int]:
    """Function factory for f: (x, y) ==> x / y mod p^3"""
    if p == 3:
        pass
    elif not miller_rabin(p, 15):
        raise Exception(f"P: {p} not prime! (probably)")
    p3 = pow(p, 3)
    def f(x: int, y: int) -> int:
        return moddiv_p3_prime(x, y, p, p3)

    return f

def fp_composite(p: int) -> Callable[[int, int], int]:
    """Function factory for f: (x, y) ==> x / y mod p^3"""
    p3 = pow(p, 3)
    tot = totient(p3)
    def f(x: int, y: int) -> int:
        inv = modular_inverse(tot, y, p3)
        return (x * inv) % p3

    return f


def moddiv_p3_prime(x: int, y: int, p: int, p3: int = None) -> int:
    """Compute (x, y) ==> x / y mod p^3 where p is a prime."""
    if p3 is None:
        p3 = pow(p, 3)

    totient = totient_prime_power(p, 3)
    inv = modular_inverse(totient, y, p3)
    return (x * inv) % p3

def moddiv(x: int, y: int, n: int) -> int:
    """Compute x / y mod n."""
    tot = totient(n)
    inv = modular_inverse(tot, y, n)
    return (x * inv) % n