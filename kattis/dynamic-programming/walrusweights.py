
n = int(input())
weights = []
for i in range(n):
    weights.append(int(input()))

t = sum(weights)
memo = {}
def can_get_sum(x, i):
    if x in memo:
        if i in memo[x]:
            return memo[x][i]
    else:
        memo[x] = {}
    if x < 0:
        return False
    if i == 1:
        memo[x][i] = x == weights[0] or x == 0
        return x == weights[0] or x == 0
    if x == 0:
        memo[x][i] = True
        return True
    memo[x][i] =  can_get_sum(x-weights[i-1], i-1) or can_get_sum(x, i-1)
    return memo[x][i]

v = 1000
k = 0
while not can_get_sum(v, n):
    k *= -1
    if k>=0:
        k += 1
    v = 1000+k
print(v)
