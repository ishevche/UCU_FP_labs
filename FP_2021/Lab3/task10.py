input_number = int(input())
rows_amount = 0
for i in range(1, 8):
    if i * (i + 1) / 2 >= input_number:
        rows_amount = i
        break
cur_letter = ord('A')
for i in range(1, rows_amount + 1):
    print(' ' * (rows_amount - i) * 2, end='')
    for j in range(min(i, input_number) - 1):
        print(chr(cur_letter), end=' ')
        cur_letter += 1
        input_number -= 1
    print(chr(cur_letter))
    cur_letter += 1
    input_number -= 1
