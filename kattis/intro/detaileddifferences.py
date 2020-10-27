# https://open.kattis.com/problems/detaileddifferences
testCases = int(input())

def comparisonString(first, second):
    result = ""
    comparing = 0
    while comparing<len(first):
        if first[comparing] != second[comparing]:
            result += "*"
        else:
            result += "."
        comparing += 1
    return result

casesRead = 0
while casesRead<testCases:
    first = input()
    second = input()
    print(first)
    print(second)
    print(comparisonString(first, second))
    print("")
    casesRead += 1
