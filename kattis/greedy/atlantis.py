from operator import itemgetter
from heapq import heappush, heappop, heapreplace

def readNums():
    return map(lambda x: int(x), input().split(" "))

n = int(input())
stores = []
for i in range(0, n):
    t, h = readNums()
    stores.append((t, h))

stores.sort(key=itemgetter(1), reverse=True)


scheduled = 0
candidateStores = []

for i in range(0, n):
    # Back in time, at store i deadline...
    # now we may schedule store i
    heappush(candidateStores, stores[i][0])
    prevTime = 0 if i+1>=n else stores[i+1][1]
    timeBeforeNewCandidates = stores[i][1] - prevTime
    while timeBeforeNewCandidates > 0 and len(candidateStores)>0:
        candidate = candidateStores[0]
        if candidate <= timeBeforeNewCandidates:
            heappop(candidateStores)
            timeBeforeNewCandidates -= candidate
            scheduled += 1
        else:
            heapreplace(candidateStores, candidate-timeBeforeNewCandidates)
            timeBeforeNewCandidates = 0

print(scheduled)
