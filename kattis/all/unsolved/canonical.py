from math import ceil, inf
import sys

sys.setrecursionlimit(10**6)

# https://math.stackexchange.com/questions/3121896/what-property-of-a-coin-system-makes-it-canonical
# In order to decide whether the coin system c1=1<c2<c3<… is canonical, it suffices to check only for each m whether the greedy solution for ⌈c_{m+1}/c_m⌉c_m is optimal.

n = int(input())
coins = [int(x) for x in input().split()]

memo={}
def store(x, y, v):
    global memo, coins
    if x not in memo:
        memo[x] = {}
    memo[x][y] = v
def get_optimal(v, using):
    print(v, using)
    global memo
    if v in memo and using in memo[v]:
        print("AWB", v, using, memo[v][using])
        return memo[v][using]
    if v == 0:
        store(v, using, 0)
        return 0
    if v < 0 or using == 0:
        store(v, using, inf)
        return inf
    # We either don't use using-1 coin or we use it
    optimal = min(get_optimal(v, using-1), 1+get_optimal(v-coins[using-1], using))
    store(v, using, optimal)
    return optimal

greedy_memo = {}
def get_greedy(v, from_index):
    global greedy_memo, coins
    if v in greedy_memo:
        print("usefil")
        return greedy_memo[v]
    if v == 0:
        greedy_memo[v] = 0
        return 0
    if coins[from_index-1] <= v:
        greedy_memo[v] = 1+get_greedy(v-coins[from_index-1], from_index)
        return greedy_memo[v]
    greedy_memo[v] = get_greedy(v, from_index-1)
    return greedy_memo[v]


# " A useful fact (due to Dexter Kozen and Shmuel Zaks) is that if S is non-canonical, then the smallest counterexample is less than the sum of the two largest denominations."
cap = coins[n-1]+coins[n-2]
to_check = list(filter(lambda v: v<cap, [ceil(coins[m + 1] / coins[m]) * coins[m] for m in range(0, n - 1)]))
for v in reversed(to_check):
    print("*")
    if get_greedy(v, n) != get_optimal(v, n):
        print("non-canonical")
        exit(0)
print("canonical")
