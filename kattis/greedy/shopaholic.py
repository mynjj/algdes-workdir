n = int(input())

prices = sorted(map(lambda x: int(x), input().split(" ")), reverse = True)
sum = 0
for i in range(2, n, 3):
    sum += prices[i]

print(sum)
