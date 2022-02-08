from math import floor

try:
    grades = [int(input()) for i in range(5)]
    grades_sum = 0
    for grade in grades:
        if grade not in range(101):
            raise ValueError
        grades_sum += grade
    mean = grades_sum / 5
    if grades_sum % 5 != 0:
        print(f"Average grade = {mean:.1f} -> ", end='')
    else:
        print(f"Average grade = {int(mean)} -> ", end='')
    mean = floor(mean)
    if 0 <= mean <= 59:
        print('F')
    elif mean <= 66:
        print('E')
    elif mean <= 74:
        print('D')
    elif mean <= 81:
        print('C')
    elif mean <= 89:
        print('B')
    else:
        print('A')
except ValueError:
    print("None")
