def readNums():
    return map(lambda x: int(x), input().split(" "))

nSocks, capacity, maxDif = readNums()

socks = sorted(readNums(), reverse=True)

initialSock = 0
against = 1
usedMachines = 0
while initialSock < nSocks:
    while against < nSocks and socks[initialSock] - socks[against] <= maxDif and against-initialSock < capacity:
        against += 1
    usedMachines += 1
    initialSock = against
    against = initialSock + 1

print(usedMachines)
