from math import floor
from operator import itemgetter

def readNums():
    return map(lambda x: int(x), input().split(" "))

n = int(input())
intervals = []
for i in range(n):
    s, f, w = readNums()
    intervals.append((s, f, w))

intervals.sort(key=itemgetter(1))

# Given {I0, I1, ...Ii}
# pindex(i) is the index of the "ceil": the max k
# such that Ik is compatible with Ii
def pindex(i):
    searching_lte_to = intervals[i][0]
    s = 0
    k = i
    t = floor((k+s)/2)
    while k-s>1:
        if intervals[t][1] <= searching_lte_to:
            s = t
        else:
            k = t
        t = floor((k+s)/2)
    if intervals[s][1] <= searching_lte_to:
        return s
    return None


wis_memo = {}
wis_memo[0] = 0
for i in range(1, n+1):
    _, _, wi = intervals[i-1]
    if pindex(i-1) == None:
        wis_memo[i] = max(wi, wis_memo[i-1])
        continue
    take = wi + wis_memo[pindex(i-1)+1]
    leave = wis_memo[i-1]
    wis_memo[i] = max(take, leave)

print(wis_memo[n])
