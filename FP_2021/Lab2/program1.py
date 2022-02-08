from math import pi

r = float(input())
h = float(input())

v = pi * r * r * h
s = 2 * pi * r * h + 2 * pi * r * r

print("V = ", round(v, 3))
print("A = ", round(s, 3))
