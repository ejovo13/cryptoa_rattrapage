"""Factory class for our hash function."""

from typing import Callable, Iterable
from .number_theory import *
import numpy as np
import itertools
import seaborn
from functools import cached_property, cache

class HashFn:
    """Implementation of schema 7."""

    def __init__(self, p: int):

        self.p = p
        self.p3 = pow(p, 3)

        self.prime = miller_rabin(p, 15)

        if self.prime:

            def fn(x: int, y: int) -> int:
                y_inv = self.inv_p3(y)
                return self.mod_p3(x, y_inv)

            self.fn = fn

        else:
            self.fn = fp_composite(p)

    def __call__(self, x: int, y: int) -> int:
        return self.fn(x, y)

    def multiplicative_group(self) -> Iterable[int]:
        """Return an _iterable_ across all elements in Zp*."""
        if self.prime:
            return range(1, self.p)
        else:
            return filter(
                lambda n: iscoprime(n, self.p),
                range(1, self.p)
            )

    @cached_property
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
        return (self.p * self.p) * self.totient_p()

    def inv_p3(self, y: int) -> int:
        """Return the multiplicative inverse of y in Zp3*."""
        return modular_inverse(self.totient_p3(), y, self.p3)

    def inv_p3_image(self) -> Iterable[int]:
        """Return the image of self.inv_p3 for all p in Zp*."""
        return (self.inv_p3(y) for y in self.multiplicative_group())

    def division_preimage(self) -> Iterable[int]:
        """Return (Zn* x Y^{-1}_p^3)"""
        zn = self.multiplicative_group_list
        return itertools.product(zn, self.inv_p3_image())

    def mod_p3(self, x, y_inv) -> int:
        """Retrun x * yinv mod p3"""
        return (x * y_inv) % self.p3

    @cached_property
    def inv_p3_image_list(self) -> list[int]:
        return list(self.inv_p3_image())

    @cached_property
    def inv_p3_image_reverse_dict(self) -> dict[int, int]:
        """Return the mapping y => yinv."""
        mapping = {}
        for y in self.multiplicative_group_list:
            mapping[self.inv_p3(y)] = y

        return mapping


    def grid(self) -> np.ndarray:

        FP = np.ones((self.p, self.p)) * np.nan
        zn = self.multiplicative_group_list
        for (i, j) in itertools.product(zn, zn):
            FP[i, j] = self.__call__(j, i)

        return FP

    def paint(self):
        return seaborn.heatmap(self.grid())

    @cached_property
    def image(self) -> set[int]:
        r"""Return the image of this function for all (x, y) in Zp* \times Zp*."""
        image = set()
        for (i, j) in self.preimage():
            image.add(self.__call__(j, i))

        return image


    def preimage(self) -> Iterable[tuple[int, int]]:
        return itertools.product(self.multiplicative_group_list, self.multiplicative_group_list)

    def preimage_list(self) -> list[tuple[int, int]]:
        return list(self.preimage())

    def cardinality_image(self) -> int:
        """Return the number of elements in this functions image."""
        return len(self.image)

    def cardinality_preimage(self) -> int:
        if self.prime:
            return (self.p - 1) ** 2
        else:
            return len(self.preimage_list())

    def rand(self) -> int:
        """Sample from (Zn*, Zn*) and compute self(a, b). Only valid for prime p."""
        x = random.randint(1, self.p - 1)
        y = random.randint(1, self.p - 1)
        return self(x, y)



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