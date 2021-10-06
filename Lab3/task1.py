a = int(input())
num = 5 ** a
ans = 0
numCopy = num
while numCopy > 0:
    ans += (numCopy & 1)
    numCopy //= 2
"Number 5 is evil number. Its hamming weight is 2."
if ans % 2 == 0:
    print(f"Number {num} is evil number. Its hamming weight is {ans}.")
else:
    print(f"Number {num} is odious number. Its hamming weight is {ans}.")
