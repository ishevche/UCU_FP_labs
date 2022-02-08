from math import exp, sqrt, pi

x = float(input())
u = float(input())
o = float(input())

f = exp(-((x - u)**2) / (2 * (o**2))) / sqrt(2 * pi * (o**2))

print(round(f, 10))
