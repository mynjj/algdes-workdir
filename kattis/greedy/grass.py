from operator import itemgetter
import math
import sys

def getNums(str):
    return map(lambda x: int(x), str.split(" "))

def readNums():
    return getNums(input())

nIntervals = 0
l = 0
w = 0

def readConf():
    global nIntervals, l, w
    out = sys.stdin.readline()
    if not out:
        return False
    nIntervals, l, w = getNums(out)
    return True

running = readConf()

while running:
    sprinklers = []
    for i in range(0, nIntervals):
        x, r = readNums()
        t = 4*r*r - w*w
        if(t>0):
            rp = math.sqrt(t)/2
            sprinklers.append((x-rp, x+rp))

    nIntervals = len(sprinklers)
    sprinklers.sort(key=itemgetter(1))
    coveredTil = 0
    count = 0

    while coveredTil < l:
        j = nIntervals - 1
        while j>=0 and sprinklers[j][0] > coveredTil:
            j -= 1
        if j < 0:
            count = -1
            break
        if coveredTil == sprinklers[j][1]:
            count = -1
            break
        coveredTil = sprinklers[j][1]
        count += 1

    print(count)

    running = readConf()
