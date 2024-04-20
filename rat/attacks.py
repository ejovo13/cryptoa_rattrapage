"""Add attacks using p and z."""

# from .deal import *
from .factory import HashFn

def exhaustive_attack(z: int, p: int) -> list[tuple[int, int]]:
    """Retrieve a list of (x, y) tuples that satisfy fp(x, y) = z."""

    fn = HashFn(p)

    # Now let's iterate through all possible inputs.


