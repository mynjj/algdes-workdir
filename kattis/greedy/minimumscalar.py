nCases = int(input())

def getNums(str):
    return map(lambda x: int(x), str.split(" "))

def readNums():
    return getNums(input())

def solveCase(case):
    n = int(input())
    a = sorted(readNums())
    b = sorted(readNums())

    s = 0
    for j in range(0, n):
        s += a[j] * b[n-1-j]

    print("Case #"+str(case)+": "+str(s))

for case in range(1, nCases+1):
    solveCase(case)
