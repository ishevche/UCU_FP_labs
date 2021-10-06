x, y = input().split()
num = int(x) ^ int(y)
ans = 0
numCopy = num
while numCopy > 0:
    ans += (numCopy & 1)
    numCopy //= 2
print(ans)
