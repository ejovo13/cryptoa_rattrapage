"""Test our hash function"""

from ..hash import *

def test_schwa():

    p = 5
    ic(schwa7_txt(p, ''))

    def print_schwa(p: int, s: str):

        if isinstance(s, bytes):
            bs = s
        else:
            bs = schwa7_txt(p, s)

        i = int.from_bytes(bs)
        print(i)


    # print_schwa(p, b'\00')
    # print_schwa(p, b'\01')
    # print_schwa(p, b'\32')
    # print_schwa(p, b'\33')
    for i in range(100):
        ic(schwa7_int(p, i))


    ic(split_bytes(p, int(15).to_bytes(1)))




