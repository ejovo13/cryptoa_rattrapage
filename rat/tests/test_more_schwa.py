from ..hash import *


import random

def test_ints_to_bytes():

    n = 100

    for _ in range(n):

        v = random.randint(0, 512)
        v_as_bytes = to_bytes(v)

        v_recreated = int.from_bytes(v_as_bytes)
        assert v_recreated == v

def test_split():

    s = Schwa(5)

    for i in range(16):
        ic(s.split_bytes_to_int(i.to_bytes(20)))
        # ic(s.split_int(i))
    for i in range(16):
        ic(s.split_int(i))
    # Figure out why split int is behaving so weirdly.

    for i in range(16):
        ic(s(i))

    ic(s.suprememum())

