"""Number theory functions needed to implement schema 7."""

from sympy.ntheory import factorint
import random

def gcd(p: int, q: int) -> int:
    # Euclids algorithm
    while q != 0:
        p, q = q, p % q
    return p


def iscoprime(a: int, b: int) -> bool:
    return gcd(a, b) == 1

def modular_inverse(totient: int, a: int, n: int) -> int:
    """Return the multiplicative inverse of an integer in Zn*."""
    return pow(a, totient - 1, n)


def totient(n: int) -> int:
    """Compute euler's totient function. Credit: https://stackoverflow.com/a/52263174

    Examples
    >>> totient(3)
    2
    >>> totient(9)
    6
    >>> totient(7)
    6
    """
    totient = n
    for factor in factorint(n):
        totient -= totient // factor
    return totient

def totient_prime_power(p: int, exponent: int = 3) -> int:
    """Compute totient(pow(p, exponent)) for primes."""
    return pow(p, exponent - 1) * (p - 1)

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

def gen_primes():
    """ Generate an infinite sequence of prime numbers.

    Taken from: https://stackoverflow.com/a/2212923
    """
    # Maps composites to primes witnessing their compositeness.
    # This is memory efficient, as the sieve is not "run forward"
    # indefinitely, but only as long as required by the current
    # number being tested.
    #
    D = {}

    # The running integer that's checked for primeness
    q = 2

    while True:
        if q not in D:
            # q is a new prime.
            # Yield it and mark its first multiple that isn't
            # already marked in previous iterations
            #
            yield q
            D[q * q] = [q]
        else:
            # q is composite. D[q] is the list of primes that
            # divide it. Since we've reached q, we no longer
            # need it in the map, but we'll mark the next
            # multiples of its witnesses to prepare for larger
            # numbers
            #
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]

        q += 1