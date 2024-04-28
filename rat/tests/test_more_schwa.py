from ..hash import *
import pytest
from ..number_theory import nth_prime

import random

def test_ints_to_bytes():

    n = 100

    for _ in range(n):

        v = random.randint(0, 512)
        v_as_bytes = to_bytes(v)

        v_recreated = int.from_bytes(v_as_bytes)
        assert v_recreated == v

@pytest.mark.parametrize('p', [nth_prime(7), 5])
def test_split(p: int):

    n = (p - 1) * (p - 1)

    s = Schwa(p)

    # for i in range(16):
    #     ic(s.split_bytes_to_int(i.to_bytes(20)))
    #     # ic(s.split_int(i))
    # for i in range(16):
    #     ic(s.split_int(i))
    # Figure out why split int is behaving so weirdly.

    for i in range(n):
        ic(s(i))




    ic(s.suprememum())

