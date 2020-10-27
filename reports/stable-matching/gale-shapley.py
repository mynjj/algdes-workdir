# The given set of named elements is partitioned in 2 sets.
# According to the role they play in the algorithm, we'll name
# this sets as Proposers, or Receivers.

class Proposer:
    def __init__(self, index, name):
        self.index = index
        self.name = name
        self.preferences = []
    def bestUnproposedReceiver(self):
        return self.preferences.pop()
    # Used to initially set the preferences to indices:
    def setPreferences(self, preferences):
        self.preferences = preferences
    # When we later have created all the recievers, we can replace the indices with actual objects:    
    def setReceivers(self, receivers):
        def getReceiver(k):
            return receivers.collection[k]
        self.preferences = list(map(getReceiver, self.preferences))


class ProposerCollection:
    def __init__(self):
        self.available = []
        self.collection = {}
    def add(self, index, name):
        proposer = Proposer(index, name)
        self.collection[index] = proposer
        self.available.append(proposer)
    def includes(self, index):
        return index in self.collection
    def setReceivers(self, receivers):
        for proposer in self.collection.values():
            proposer.setReceivers(receivers)
    def getAvailable(self):
        return self.available[0]
    def get(self, index):
        return self.collection[index]
    def setPreferences(self, index, preferences):
        self.collection[index].setPreferences(preferences)
    def matchFirstAvailable(self):
        self.available.pop(0)


class Receiver:
    def __init__(self, index, name):
        self.match = None
        self.preferences = {}
        self.index = index
        self.name = name
    def setPreferences(self, preferences):
        for attractiveness, proposerIndex in enumerate(preferences):
            self.preferences[proposerIndex] = attractiveness
    def setMatch(self, proposer):
        self.match = proposer
    def attractiveness(self, proposer):
        return self.preferences[proposer.index]
    def likesMore(self, proposer1, proposer2):
        return self.attractiveness(proposer1)>self.attractiveness(proposer2)


class ReceiverCollection:
    def __init__(self):
        self.collection = {}
    def get(self, index):
        return self.collection[index]
    def add(self, index, name):
        self.collection[index] = Receiver(index, name)
    def setPreferences(self, index, preferences):
        self.collection[index].setPreferences(preferences)
    def setMatch(self, receiver, proposer):
        self.collection[receiver.index].setMatch(proposer)

class GaleShapley:
    def __init__(self, proposers, receivers):
        self.proposers = proposers
        self.receivers = receivers
        self.proposers.setReceivers(receivers)
    def getReceiver(self, receiverIndex):
        return self.receivers.get(receiverIndex)
    def getProposer(self, proposerIndex):
        return self.proposers.get(proposerIndex)
    def match(self, proposer, receiver):
        self.proposers.matchFirstAvailable()
        self.receivers.setMatch(receiver, proposer)
    def unmatch(self, proposer, receiver):
        self.proposers.available.append(proposer)
        self.receivers.setMatch(receiver, None)
    def matches(self):
        return map(lambda r: (r.match, r),
                   self.receivers.collection.values())
    def run(self):
        while self.proposers.available:
            proposer = self.proposers.getAvailable()
            receiver = proposer.bestUnproposedReceiver()

            currentMatch = receiver.match
            if currentMatch is None:
                self.match(proposer, receiver)
            elif receiver.likesMore(proposer, currentMatch):
                self.unmatch(currentMatch, receiver)
                self.match(proposer, receiver)

        return self.matches()



#######################################################
###  VARIABLES USED ALONG THE WAY
proposers = ProposerCollection()
receivers = ReceiverCollection()
n = 0

###  LOADING INPUT
def discardLine(line):
    if line.startswith('#') or line.isspace():
        return True
    else:
        return False

# First two lines or more are comments
n = input()
while discardLine(n):
    n = input()

# The next line is like "n=4"
n = int(n.split("=")[1])
# The next n lines list the index and the corresponding name like "index name"
def readNameLine(line):
    index, name = line.split(" ")
    return index, name
def nonEmptyString(s):
    return not len(s)==0

for i in range(0, n):
    index, name = readNameLine(input())
    proposers.add(index, name)

    index, name = readNameLine(input())
    receivers.add(index, name)

# There's an empty line
input()

# And then the preference list for everyone is given
for i in range(0, 2*n):
    index, preferences = input().split(": ")
    preferences = list(filter(nonEmptyString, preferences.split(" ")))
    preferences.reverse()
    if proposers.includes(index):
        proposers.setPreferences(index, preferences)
    else:
        receivers.setPreferences(index, preferences)

### RUNNING THE ALGORITHM
algorithm = GaleShapley(proposers, receivers)
matches = algorithm.run()

### OUTPUT
for proposer, receiver in matches:
    print(proposer.name+" -- "+receiver.name)
