n = int(input())
def readNums():
    return map(lambda x: int(x), input().split(" "))

sticks = sorted(map(lambda x: int(x), input().split(" ")), reverse = True)

for i in range(0, n - 2):
    if sticks[i]-sticks[i+1] < sticks[i+2]:
        print("possible")
        exit(0)

print("impossible")
