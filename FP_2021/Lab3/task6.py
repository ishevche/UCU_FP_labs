h = int(input())
base_symbol = '*'
separator_symbol = ' '
print(base_symbol)
if h != 1:
    for i in range(2, h):
        print(base_symbol, end='')
        print(separator_symbol * (i - 2), end='')
        print(base_symbol)
    print(base_symbol * h)
