from operator import itemgetter
from heapq import heappush, heappop

def readNums():
    return map(lambda x: int(x), input().split(" "))

n = int(input())
jobs = []

for i in range(0, n):
    deadline, amount = readNums()
    jobs.append((deadline, -amount))

jobs.sort(key=itemgetter(0), reverse = True)
schedulableJobs = []
total = 0
for i in range(0, n):
    heappush(schedulableJobs, jobs[i][1])
    previousJobDeadline = 0 if i+1>=n else jobs[i+1][0]
    timeBeforeNewCandidates = jobs[i][0] - previousJobDeadline
    nJobs = len(schedulableJobs)
    if nJobs <= timeBeforeNewCandidates:
        total += -sum(schedulableJobs)
        schedulableJobs = []
    else:
        for j in range(0, timeBeforeNewCandidates):
            total -= heappop(schedulableJobs)

print(total)
