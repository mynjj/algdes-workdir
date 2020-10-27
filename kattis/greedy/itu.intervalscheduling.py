n = int(input())
arr = []
i = 0
while i<n:
    line = input()
    [a, b] = line.split(" ")
    arr.append((int(a), int(b)))
    i+=1

def byEndTime(x):
    return x[1]
arr.sort(key=byEndTime)

i = 0
et = -1
count = 0

while i < n:
    if arr[i][0]>=et:
        count += 1
        et = arr[i][1]
    i += 1

print(count)
