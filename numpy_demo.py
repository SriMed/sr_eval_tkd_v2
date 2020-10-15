import numpy as np

# A demonstration of amazing things in numpy that make working with matrices soooooo easy!

x = np.array([[0, 3], [3, 4]])
print("Matrix x:")
print(x)
print()

y = np.array([[4, 5], [-1, -2]])
print("Matrix y:")
print(y)
print()

print("Dot product:")
print(x@y)
print()

print("Item-wise product:")  # DO NOT GET THIS CONFUSED WITH THE DOT PRODUCT!
print(x*y)
print()

print("Item-wise sum:")
print(x+y)
print()

print("Scalar multiplication:")
print(3*x)
print()

print("...or:")
print(x*3)
print()

print("Add a value to every value in a matrix:")
print(x + 3)
print()

print("Transpose:")
print(y.transpose())
print()

print("...or:")
print(y.T)
print()

print("Create an array of zeroes:")
print(np.zeros((2, 3)))
print()

print("Create an array of random values on the interval [0,1):")
print(np.random.rand(2, 3))  # Note this takes two integer args where "zeroes" takes a tuple
print()

print("Create an array of random values on the interval [-1,1):")
new_arr = 2 * np.random.rand(2, 3) - 1  # Why does this work?
print(new_arr)
print()

print("Find the magnitude of a vector:")
vec = np.array([3, -4])  # Note: one dimensional.
mag = np.linalg.norm(vec)
print("Magnitude of %s is %s." %(vec, mag))
print()

print("Vectorize a function:")
def f(n): return 1 if n > 0 else 0  # This is the step function, defined with a single numeric input and a single numeric output
#print(f(x))  # If you uncomment this, it will throw an error!  The original function cannot accept a matrix as an argument
new_f = np.vectorize(f)  # This creates a function that applies the original function to each element of a matrix individually
print(new_f(x))
print()

#
# x = np.array([2, 3])
# print(x)
# print(x.T)
#
# y = np.array([[2,3]])
# print(y)
# print(y.T)