n = int(input())
if n != 0:
    print("1/2", end='')
    for cur_fraction in range(1, n):
        if cur_fraction % 2 == 0:
            print(' + ', end='')
        else:
            print(' - ', end='')
        print(f'{2 * cur_fraction + 1}/{2 * cur_fraction + 2}', end='')
print()
