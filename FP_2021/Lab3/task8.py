n = int(input())
answer = 1
for i in range(1, n + 1):
    if i % 7 != 0:
        answer *= i
print(answer)
