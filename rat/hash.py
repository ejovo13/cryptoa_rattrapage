"""Hash function utilities."""

from .factory import HashFn
from dataclasses import dataclass


class Schwa:
    """Implementation of Schwa7.

    ə7, pronounced 'schwa seven', is a silly hash function based on Schema 7. Parameterized by a prime number $p$, ə7 returns values in Z_p^3

    Schwa7's name is a mixture of several elements: _sch_ema 7, SHA, a linguistic nod to [Schwa](https://en.wikipedia.org/wiki/Schwa)
    """

    def __init__(self, p: int):
        """Initialize a new fp."""
        self.fn = HashFn(p)

    def __call__(self, n: int) -> int:
        """Call the schwa hash function."""
        return self.hash(n)

    def split_bytes_to_int(self, bs: bytes) -> list[int]:
        return [n + 1 for n in split_bytes_to_int(bs, self.fn.p - 1)]

    def split_int(self, x: int) -> list[int]:
        return self.split_bytes_to_int(to_bytes(x))

    def condense(self, x: int, y: int) -> int:
        """Use f_p to condense (x, y) -> f_p(x, y) mod (p - 1) + 1"""
        return (self.fn(x, y) % (p - 1)) + 1

    def condense_ints(self, ints: list[int]) -> tuple[int, int]:
        """Reduce a list of ints"""
        n = len(ints)
        if n == 1: return 1, ints[0]
        if n == 2: return ints[0], ints[1]

        acc = self.condense(ints[0], ints[1])
        for i in range(2, n - 1):
            acc = self.condense(acc, ints[i])

        return acc, ints[-1]

    def hash(self, n: int) -> int:
        ints = self.split_int(n)
        x, y = self.condense_ints(ints)
        return self.fn(x, y)

    def hash_bytes(self, bs: bytes) -> bytes:
        ints = self.split_bytes_to_int(bs)
        x, y = self.condense_ints(ints)
        return self.fn(x, y)

    def suprememum(self) -> int:
        """Return the maximum value obtained."""
        return self.fn.p3 - 1


def bytes_to_zp(p: int, bs: bytes) -> int:
    """Convert bytes to an element in Zp*, assuming that p is prime."""
    int.from_bytes(bs)
    assert bs < p, "Input bytes larger than "


def n_bytes(n: int) -> int:
    """Return the number of bytes needed to represent an integer.

    Examples
    --------
    >>> n_bytes(0)
    0
    >>> n_bytes(1)
    1
    >>> n_bytes(255)
    1
    >>> n_bytes(256)
    2
    """
    if n == 0: return 0
    n_bits = n.bit_length()
    if n_bits % 8 == 0:
        return (n_bits // 8)
    else:
        return (n_bits // 8) + 1

def to_bytes(n: int) -> bytes:
    return n.to_bytes(n_bytes(n))

def extract_y(p: int, bs: bytes) -> int:
    """Extract y from a sequence of bytes."""
    n_bs = n_bytes(p)
    y_mask = p - 1
    return y_mask & int.from_bytes(bs[:n_bs])

def expand_bytes(p: int, bs: bytes) -> tuple[int, int]:
    """Separate bytes input (less then (p - 1) * (p - 1)) into (x, y)."""
    bs_as_int = int.from_bytes(bs)
    assert bs_as_int < (p - 1) * (p - 1)
    x = bs_as_int // (p - 1)
    y = bs_as_int % (p - 1)

    # Add one to be in Zp*
    return (x + 1, y + 1)

def split_bytes(p: int, bs: bytes) -> list[bytes]:
    """Break up bytes into units with radix (p - 1)(p - 1)."""
    z = int.from_bytes(bs)
    radix = (p - 1) * (p - 1)
    n_bytes_radix = n_bytes(radix)

    lst_bytes: list[bytes] = []
    while z >= radix:

        r = z % radix
        lst_bytes.append(r.to_bytes(n_bytes_radix))
        z = (z - r) // radix

    lst_bytes.append(z.to_bytes(n_bytes_radix))

    return lst_bytes

def split_bytes_to_int(bs: bytes, radix: int) -> list[int]:
    """Break up bytes into a list of base-radix digits."""
    z = int.from_bytes(bs)

    lst_int: list[int] = []
    while z >= radix:

        r = z % radix
        lst_int.append(r)
        z = (z - r) // radix

    lst_int.append(z)

    return lst_int

# def condense(x: int, y: int, )


def schwa7_unit(p: int, bs: bytes) -> bytes:
    """Apply schema 7 as a hash function."""
    x, y = expand_bytes(p, bs)
    assert x <= p - 1
    assert y <= p - 1
    out_bytes = n_bytes(pow(p, 3))

    fn = HashFn(p)
    out = fn(x, y)
    return out.to_bytes(out_bytes)

def schwa7_unit_int(p: int, x: int) -> int:
    x_bytes = n_bytes(x)
    digest = schwa7_unit(p, x.to_bytes(x_bytes))
    return int.from_bytes(digest)

def schwa7_int(p: int, x: int) -> int:
    """Apply schwa7, converting integers to bytes."""
    x_bytes = n_bytes(x)
    digest = schwa7(p, x.to_bytes(x_bytes))
    return int.from_bytes(digest)

def schwa7(p: int, bs: bytes) -> bytes:
    """Apply schema7 for any sized bytes."""
    split = split_bytes(p, bs)
    p3 = pow(p, 3)
    p3_bytes = n_bytes(p3)

    units = [schwa7_unit_int(p, int.from_bytes(bs)) for bs in split]
    digest = units[0]

    for u in units[1:]:
        digest = u ^ digest

    return digest.to_bytes(p3_bytes)

def schwa7_txt(p: int, s: str) -> bytes:
    """Apply schema7 for any input str."""
    bs = s.encode()
    return schwa7(p, bs)




from icecream import ic

if __name__ == '__main__':
    print(n_bytes(17))
    p = 17
    bs = p.to_bytes()
    print(bs)
    print(p.bit_length())

    # Make sure we can't use something that it 2 bytes long
    expand_bytes(17, int(242).to_bytes())
    expand_bytes(17, int(243).to_bytes(2))

    x, y = expand_bytes(17, int(255).to_bytes())
    ic(x, y)
    # expand_bytes(11, int(256).to_bytes(2))

    for i in range(0, 100):
        x, y = expand_bytes(11, i.to_bytes(2))
        # ic(bin(x), bin(y), bin(i))
        ic(x, y, i)


    ic(expand_bytes(5, int(15).to_bytes(1)))

    ic(split_bytes(5, int(16).to_bytes(1)))

    bs = split_bytes(5, int(16).to_bytes(1))
    bs = split_bytes(5, int(31).to_bytes(1))
    ic(bs)
    # ic(bs[0], int.from_bytes(bs[1]))







