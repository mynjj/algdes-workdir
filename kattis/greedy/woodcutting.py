n = int(input())

def readTotalPiece():
    return sum(map(lambda x: int(x), input().split(" ")[1:]))

def solveCase():
    customers = int(input())
    pieces = []
    for i in range(0, customers):
        pieces.append(readTotalPiece())
    pieces.sort()
    s = 0
    w = customers
    for piece in pieces:
        s += w*piece
        w -= 1
    print(s/customers)


for i in range(0, n):
    solveCase()
