"""Test that our multiplicative inverse function is working as planned."""

# from ..deal import *
# import pytest

# Prime = int


# def test_hello():

#     def assert_inverses(p: Prime):
#         p3 = pow(p, 3)
#         totient = tot3(p)
#         xs = list(range(1, p))

#         for x in xs:
#             assert ((x * modular_inverse(totient, x, p3)) % p3) == 1

#     for p in [3, 5, 7, 11, 13, 17, 19]:
#         assert_inverses(p)



# def test_natural():

#     N = NaturalNumber(8)
#     N.totient
#     assert N.mul_group_list() == [1, 3, 5, 7]

#     # Now test that each element has an inverse.
#     for el in N.mul_group():

#         E = NaturalNumber(el)
#         assert(iscoprime(el, N.n))
#         assert (E.mul_inv(N) * el) % N.n == 1


# @pytest.mark.parametrize('n', [7, 6, 15])
# def test_inverse_prime(n: int):

#     N = NaturalNumber(n)
#     N.totient

#     zn = N.mul_group_list()
#     print(zn)

#     for el in N.mul_group_list():

#         E = NaturalNumber(el)
#         N3 = N.cubed()

#         print((E.n, E.mul_inv(N3), E.mul_inv(N3) * el, N3.n))

#         assert iscoprime(N3.n, el)
#         assert (E.mul_inv(N3) * el) % N3.n == 1



