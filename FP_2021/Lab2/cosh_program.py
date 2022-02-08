from math import cosh, exp, e

x = float(input())

cos = cosh(x)
ex = 0.5 * (exp(x) + exp(-x))
ee = 0.5 * (e ** x + e ** -x)

print(f"COS = {cos:.4f}")
print(f"EXP = {ex:.4f}")
print(f"E = {ee:.4f}")
