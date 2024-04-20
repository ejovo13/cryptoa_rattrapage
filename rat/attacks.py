"""Add attacks using p and z."""

# from .deal import *
from .factory import HashFn
from itertools import product

def exhaustive_attack(z: int, p: int) -> list[tuple[int, int]]:
    """Retrieve a list of (x, y) tuples that satisfy fp(x, y) = z."""

    fn = HashFn(p)
    out: list[tuple[int, int]] = []

    # Now let's iterate through all possible inputs.
    for (x, y) in fn.preimage():
        print(x, y, fn(x, y))

        if fn(x, y) == z:
            out.append((x, y))


    return out

def exhaustive_attack_improved(z: int, p: int) -> list[tuple[int, int]]:
    """Retrieve a list of (x, y) tuples that satisfy fp(x, y) = z.

    This time, instead of iterating the regular preimage of (Zn* x Zn*), we iterate
    the primage (Zn* x Y^{-1}_p^3)
    """

    fn = HashFn(p)
    out: list[tuple[int, int]] = []

    for (x, y_inv) in fn.division_preimage():
        print(x, y_inv, fn.mod_p3(x, y_inv))

        if fn.mod_p3(x, y_inv) == z:
            out.append((x, fn.inv_p3_image_reverse_dict[y_inv]))

    return out


