from rat import *



s7 = Schwa(P_CHALLENGE)

print(s7.hash_str(''))
print(s7.hash_str(' '))
print(s7.hash_str('Hello world'))
print(s7.hash_str('Hello borld'))



# Let's start printing our bytes.


# def boolean_map(n: int) -> np.ndarray[int]:
#     p = nth_prime(n)
#     pp2 = (p - 1) * (p - 1)
#     p3 = pow(p, 3)
#     schwa = Schwa(p)
#     list_arrays = [int_to_boolean(schwa(i)) for i in range(pp2)]

#     # Convert our list of arrays to a numpy matrix
#     out_matrix = np.zeros((pp2, p3.bit_length()), dtype=int)

#     for i, array in enumerate(list_arrays):
#         out_matrix[i,-len(array):] = np.array(array, dtype=int)

#     return out_matrix




# n = 3
# print(nth_prime(n))
# print(boolean_map(n))
# print(80 * "=")
# print(boolean_map(7))

# seaborn.heatmap(boolean_map(7))


