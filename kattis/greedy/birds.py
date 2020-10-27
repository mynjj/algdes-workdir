def readNums():
    return map(lambda x: int(x), input().split(" "))

l, d, n = readNums()
if n==0:
    print(((l-12) // d) + 1)
    exit(0)

birds = []

for i in range(0, n):
    birds.append(int(input()))

birds.sort()

total = (birds[0]-6)//d
for i in range(0, n-1):
    total += ((birds[i+1]-birds[i])//d) - 1
total += ((l-6)-birds[-1])//d

print(total)
