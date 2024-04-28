# """Prototype for analyzing Subject 7"""

# from typing import Callable
# import random
# import polars as pl
# import numpy as np

# from .exceptions import *

# # p is 32 hexadecimal digits <=> 16 bytes <=> 128 bits
# p = 0xd2bf071417608219223ad076131586a9
# # z is 96 hexadecimal digits <=> 48 bytes <=>
# z = 0x4520670aac4c7f5af9f86bed585d6066dcb73b9ec8c9b88536b46e252e64a1d28da6f8cf0d8bbf60fa6a4f8ee9854909

# print(p)
# print(z)


# def one_way_function_factory(p: int) -> Callable[[int, int], int]:
#     """Generate the one-way function f_p, as defined in subject 7."""
#     p_cubed = p * p * p
#     def f_p(x: int, y: int) -> int:
#         if x % y == 0:
#             assert isinstance(x // y, int), "Not an int!"
#             return (x // y) % p_cubed
#         else:
#             raise Exception(f"x: {x}, y: {y}, Not divisible")

#     return f_p

# def modified_function_factory(p: int) -> Callable[[int, int], int]:
#     """Generate a new one-way function f_p := (x, y) |-> (x^y) mod p^3"""
#     p_cubed = p * p * p
#     def f_p(x: int, y: int) -> int:
#         return pow(x, y, p_cubed)

#     return f_p





# f_3 = one_way_function_factory(3)
# print(f_3(10, 10))

# # Ideas:
# # - visualize f_p for a low value of p.
# # - figure out if p is prime


# big_prime = 762515890128057700236061562369
# # print(miller_rabin_pretreatment(big_prime))
# # print(miller_rabin(big_prime, 10))

# # print(miller_rabin(p, 100))


# def explore_fp(p: int) -> pl.DataFrame:
#     """Exhaustively compute the value of f_p for small values of p."""
#     if p == 3:
#         pass
#     elif not miller_rabin(p, 10):
#         raise NotPrimeError(p)

#     f_p = one_way_function_factory(p)

#     # Now we want to generate all possible inputs
#     p_cubed = p**3

#     xs = []
#     ys = []
#     fp = []

#     for x in range(1, p_cubed):
#         for y in range(1, p_cubed):
#             xs.append(x)
#             ys.append(y)
#             try:
#                 fp.append(f_p(x, y))
#             except Exception:
#                 fp.append(None)
#                 # raise Exception(f"x: {x}, y: {x}")

#     return pl.DataFrame(dict(
#         x=xs,
#         y=ys,
#         z=fp
#     ))

# def visualize_fp(p: int) -> np.ndarray:
#     return visualize_factory(p, one_way_function_factory)

# def visualize_custom(p: int) -> np.ndarray:
#     return visualize_factory(p, modified_function_factory)

# import itertools

# def visualize_factory(p: int, factory: Callable[[int], Callable[[int, int], int]]):
#     if p == 3:
#         pass

#     f_p = factory(p)

#     fp = np.ones((p, p)) * np.nan

#     zn = multiplicative_integers_mod_n(p)

#     for (i, j) in itertools.product(zn, zn):
#         try:
#             fp[i, j] = f_p(j, i)
#         except Exception:
#             fp[i, j] = np.nan

#     return fp

# def get_map_as_tuples(p: int) -> list[tuple[int, int]]:
#     matrix = visualize_fp(p)
#     # p_cubed = p**3
#     # n = p
#     indices = []
#     for i in range(1, p):
#         for j in range(1, p):
#             if not np.isnan(matrix[i, j]):
#                 indices.append((i, j))

#     return indices


# import seaborn

# def paint_custom(p: int):
#     return seaborn.heatmap(visualize_custom(p))

# def paint_fp(p: int):
#     return seaborn.heatmap(visualize_fp(p))




# def output_set_custom(p: int) -> set[int]:
#     s = set()
#     zn = multiplicative_integers_mod_n(p)
#     fp = modified_function_factory(p)
#     for (x, y) in itertools.product(zn, zn):
#         s.add(fp(x, y))
#     return s

# import polars as pl

# def f_df(p: int) -> pl.DataFrame:
#     data = visualize_fp(p)
#     xs = []
#     ys = []
#     zs = []
#     zn = multiplicative_integers_mod_n(p)

#     for (x, y) in itertools.product(zn, zn):
#         if not np.isnan(data[x, y]):
#             xs.append(x)
#             ys.append(y)
#             zs.append(int(data[x, y]))

#     return pl.DataFrame(dict(
#         x=xs,
#         y=ys,
#         z=zs
#     ))

# def custom_df(p: int) -> pl.DataFrame:
#     data = visualize_custom(p)
#     xs = []
#     ys = []
#     zs = []
#     zn = multiplicative_integers_mod_n(p)

#     for (x, y) in itertools.product(zn, zn):
#         xs.append(x)
#         ys.append(y)
#         zs.append(int(data[x, y]))

#     return pl.DataFrame(dict(
#         x=xs,
#         y=ys,
#         z=zs
#     ))

# def num_collisions_f(p: int) -> pl.DataFrame:
#     # determine the number of times we collide
#     collisions = 0
#     df = f_df(p)
#     s = set()
#     for i in df['z']:
#         if i in s:
#             collisions += 1
#         else:
#             s.add(i)
#     return collisions


# def custom_dist(p: int):
#     seaborn.histplot(custom_df(p), x='z')

# def f_dist(p: int):
#     seaborn.histplot(f_df(p), x='z')
