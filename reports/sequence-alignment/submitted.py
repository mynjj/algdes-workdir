import sys
import math
import re

def formatMemory(A):
    ''' Pretty printing of memory produced '''
    for j in range(0, len(A[0])):
        for i in range(0, len(A)):
            print("%5s" % A[i][j])
        print("")

def penalties():
    ''' Produce penalties from input file BLOSUM62.txt format'''
    size = 24                                           # amount of chars at the top
    inSize = size + 1                                   # elements on the below lines
    
    # read penalties, removing comments (#) and then newlines:
    tmp = list(map(lambda x: re.sub(r'[\r|\n]', " ", re.sub(r'#.*', "", x)).split(), open("./data/BLOSUM62.txt")))
    l = sum(tmp, [])                                    # flatten the list

    # split characters from rest of output:
    chars = l[:size]
    l = l[size:]

    # produce desired mismatch dictionary:
    a = { chars[i]:{chars[j-1]:int(l[inSize * i + j]) for j in range(1, inSize)} for i in range(size)}
    return (a, a['*']['A'])                             # provide both alpha and delta (select arbitrary cost of matching with padding)

def opt(x, y):
    '''opt sequence alignment implemented according to p. 356 of KT, using MAX instead of MIN'''
    m = len(x) + 1 ; n = len(y) + 1                     # we add padding, otherwise we will miss elements
    A = [[0 for _ in range(n)] for _ in range(m)]       # simply setup memory in dimension m x n 

    # setup the two outer rows: (to be the index times the delta):
    for i in range(0, m):
        A[i][0] = d * i
    for j in range(0, n):
        A[0][j] = d * j

    # calculate the content of the memory array selecting the better option of the three possibilities:
    for i in range (1, m):
        for j in range (1, n):
            A[i][j] = max(a[x[i - 1]][y[j - 1]] + A[i-1][j-1],
                                              d + A[i-1][j],
                                              d + A[i][j-1])

    return (A[m - 1][n - 1], A)                         #provide  both result and the memory array

def trace(i, x, j, y, A):
    '''outputs a trace of the sequence alignment, building it recursively'''
    # helper functions for easier formatting and recursion:
    t = lambda i, j: trace(i,x,j,y,A)                   # simpler trace call
    c = lambda res, x, y: [res[0] + x, res[1] + y]      # a way of adding characters to the strings we are building.
    if i < 0 or j < 0:                                  # produce prefixes consisting of either dashes or rest of letters (depending on what is negative):
        return [(j + 1) * '-' + ''.join(x[:i +1]), 
                (i + 1) * '-' + ''.join(y[:j +1])]
    
    v = A[i+1][j+1]                                     # value we arre currently looking at
    xc = x[i]                                           # the current character of the sequence of X
    yc = y[j]                                           # the current character of the sequence of Y

    # depending on which move we made, we add the corresponding character:
    if v == A[i][j] + a[xc][yc]:                        # if it is the diagonal choice
        return c(t(i-1,j-1), xc, yc)
    if v == A[i][j + 1] + d:                            # if it is only j increasing
        return c(t(i - 1, j), xc, '-')
    else:                                               # if it is only i increasing
        return c(t(i, j - 1), '-', yc)


def parse():
    inputs = []
    # parse input:
    for line in sys.stdin.readlines():
        if line.startswith('>'):                        # create new sequence tuple of name and space for sequence
            inputs.append([line.replace('>','').split()[0], ""])
        else:                                           # insert associated sequence
            inputs[len(inputs) - 1][1] += line.strip() 
    return inputs


def run():
    inputs = parse()
    # for all pairs test and output both alignment and trace:
    for i in range(len(inputs)):
        x = inputs[i]                                   # access x
        for j in range(i + 1,len(inputs)):
            y = inputs[j]                               # access y

            # calculate result and memory table:
            (r, A) = opt(x[1], y[1])
            print("{}--{}: {}".format(x[0], y[0], r))   # print the names and result

            # get the sequence alignment and print it:
            i = len(x[1]) - 1                           # the starting value of i
            j = len(y[1]) - 1                           # the starting value of j
            (t1, t2) = trace(i, x[1], j, y[1], A)       # get the sequence alignments
            print (t1) 
            print (t2)

            # formatMemory(A) # debug output memory if needed

# load alpha and delta, which we have globally accessible:
(a, d) = penalties()
# start algorithm:
run()
