start_number = int(input())
h = int(input())
for cur_row_num in range(h):
    row = ' '.join([str(i) for i in range(start_number, start_number + h - cur_row_num)])
    print(row)
