from math import sqrt

c = 299792458.0
m = float(input())
v = float(input())

mr = m / sqrt(1 - (v / c)**2)
E = mr * c**2

print(E)
