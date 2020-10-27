# https://open.kattis.com/problems/different
import sys

for line in sys.stdin:
    values = line.split(" ")
    print(abs(int(values[0])-int(values[1])))
