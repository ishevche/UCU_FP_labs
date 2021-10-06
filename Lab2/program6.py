import math


def sales_prediction():
    sum_all = float(input())
    print(1.19 * sum_all)


def yard_to_meter():
    yard = float(input())

    print(yard * 914)
    print(yard * 0.914)
    print(yard * 0.000914)


def cashier():
    first = int(input())
    second = int(input())
    third = int(input())
    fourth = int(input())
    fifth = int(input())

    sum = first + second + third + fourth + fifth
    pdv = sum * 0.14
    sum_all = sum + pdv

    print(round(sum, 9))
    print(round(pdv, 9))
    print(round(sum_all, 9))


def odometer():
    v = float(input())
    a = float(input())
    t1 = float(input())
    t2 = float(input())

    tstop = - v / a
    if tstop > t1 or (tstop <= 0 and a > 0):
        s1 = v * t1 + 0.5 * a * t1 ** 2
    elif tstop >= 0 and a < 0:
        s1 = v * tstop + 0.5 * a * tstop ** 2
        s1 += 0.5 * (-a) * (t1 - tstop) ** 2
    v2 = v + a * t1
    s2 = abs(v2) * t2
    print(s1 + s2)


def payment_instalments():
    sum = float(input())
    sum_all = sum * 1.05
    n = int(input())
    print(sum_all)
    print(sum_all / n)


def miles_per_galon():
    driven = float(input())
    used = float(input())
    print(driven / used)


def cookie():
    n = float(input())
    sugar = n / 48 * 1.5
    butter = n / 48
    flour = n / 48 * 2.75
    print(sugar)
    print(butter)
    print(flour)


def vineyard():
    R = float(input())
    E = float(input())
    S = float(input())
    V = int((R - 2 * E) / S)
    print(V)


def compound_interest():
    P = float(input())
    r = float(input()) / 100
    n = float(input())
    t = float(input())
    A = P * (1 + r / n) ** (n * t)
    print(A)


if __name__ == "__main__":
    eval(input() + "()")
