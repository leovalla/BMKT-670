import numpy as np

matrix = np.zeros((3, 4))
print(matrix)
# Output:
# [[0. 0. 0. 0.]
 
matrix[0,1] = 7
print(matrix)
print(matrix.shape)
print(matrix.size)

ones = np.ones((1, matrix.shape[0]))
print(ones)
#output:
# [[1. 1. 1.]]

matrix_new = np.matmul(ones, matrix)
print(matrix_new)

matrix_identity = np.eye(5) 
print(matrix_identity)

print("\n How to create sets with arange and linspace")

print("\n Set of numbers from 1 to 10 with a step of 0.5, using arange")
idx = np.arange(1, 10, 0.5)
print(idx)

print("\n Set of 20 numbers from 1 to 10, using linspace")
ldx2 = np.linspace(1, 10, 20)
print(ldx2)

print("\n How to stack arrays")
matrix_a = np.array([[1, 2, 3], [3, 5, 8]])
print("\n Matrix A:")
print(matrix_a)
matrix_b = np.array([[0, -2, 3], [4, -5, 1]])
print("\n Matrix B:")
print(matrix_b)
print("\n Horizontal stack")


matrix_h = np.hstack((matrix_a, matrix_b))
print(matrix_h)

print("\n Vertical stack")
matrix_v = np.vstack((matrix_a, matrix_b))
print(matrix_v)

print("\n How to use Ravel and Flatten")
matrix_c = np.array([[1, 2, 3], [4, 5, 6]])
print("\n Matrix C:")
print(matrix_c)
print("\n Ravel C:")
rav = matrix_c.ravel()
falt = matrix_c.flatten()
rav[1] = 7
print(rav)
print(matrix_c)

print("\n Flatten C:")
print(falt)

print("\n Any changes to flat do not affect the original matrix, but changes to rav do affect the original matrix")
print("\n there is no connection between flat and the original matrix")