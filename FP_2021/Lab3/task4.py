string_input = input()
print(string_input[0], end='')
prev_symbol = string_input[0]
for i in range(1, len(string_input)):
    if string_input[i] == prev_symbol:
        print(0, end='')
        prev_symbol = '0'
    else:
        print(1, end='')
        prev_symbol = '1'
print()
