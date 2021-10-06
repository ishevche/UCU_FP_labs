from math import sqrt


def is_prime(num: int) -> bool:
    sqrt_num = int(sqrt(num)) + 1
    for check_num in range(2, sqrt_num):
        if num % check_num == 0:
            return False
    return True


try:
    inputNum = int(input())
except:
    print('Error')
    exit()

if inputNum < 3:
    print('Error')
    exit()


for check_prime in range(2, inputNum):
    if is_prime(check_prime) and inputNum % check_prime != 0:
        print(check_prime)
        exit()
