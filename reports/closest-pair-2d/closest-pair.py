import sys
import re
from math import floor, sqrt

BOUND = 7
n = 0

def distance(p1, p2):
    return sqrt((p1.x-p2.x)*(p1.x-p2.x) + (p1.y-p2.y)*(p1.y-p2.y))

class Point:
    def __init__(self, name, x, y):
        self.x = x
        self.y = y
        self.name = name
        self.x_sorted_index = None
        self.y_sorted_index = None

class Pair:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.distance = distance(p1, p2)
    def __lt__(self, pair):
        """
        We define an order between pair of points, as the order between the distances.
        The best solution will be the minimum of such an order
        """
        return self.distance < pair.distance

def re_index(v):
    index, point = v
    copy = Point(point.name, point.x, point.y)
    copy.x_sorted_index = point.x_sorted_index
    copy.y_sorted_index = index
    return copy

class SortedPoints:
    def __init__(self, points=None, skip_sorting=False):
        if(skip_sorting):
            return

        self.x_sorted = sorted(points, key=lambda p: p.x)
        for i, point in enumerate(self.x_sorted):
            point.x_sorted_index = i
        self.y_sorted = sorted(points, key=lambda p: p.y)
        for i, point in enumerate(self.y_sorted):
            point.y_sorted_index = i

    def __len__(self):
        return len(self.x_sorted)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.get_slice(key.start, key.stop)
        return self.x_sorted[key]

    def get_slice(self, start, stop):
        if stop is None:
            stop = len(self)

        # Here we build the slice, another SortedPoints
        # that only has the points as sliced by x, but creates
        # accordingly its sorted_y

        # This is linear on k = stop-start
        sliced = SortedPoints(skip_sorting=True)
        sliced.x_sorted = self.x_sorted[start:stop] # O(k)
        sliced.y_sorted = [None]*len(self)
        # O(k)
        for point in sliced.x_sorted:
            sliced.y_sorted[point.y_sorted_index] = point
            # For re-indexing x-sorted coords
            point.x_sorted_index -= start
        sliced.y_sorted = filter(lambda y: y is not None, sliced.y_sorted)
        # For re-indexing y-sorted coords
        # O(k)
        sliced.y_sorted = list(map(re_index, enumerate(sliced.y_sorted)))
        # O(k)
        for p in sliced.y_sorted:
            sliced.x_sorted[p.x_sorted_index].y_sorted_index = p.y_sorted_index
        return sliced

def best_for_element(strip, delta):
    def fn(x):
        index, point = x
        best = None

        # The following loops are guaranteed to be bounded by BOUND (so they're constant in complexity),
        # but they may end earlier, taking advantage of y-sortedness of strip,
        # and the fact that we know how close we are looking values (delta)
        against = index+1
        while against < len(strip) and against-index < BOUND and strip[against].y - strip[index].y < delta:
            currentPair = Pair(strip[against], strip[index])
            if best is None:
                best = currentPair
            else:
                best = min(best, currentPair)
            against += 1

        return best
    return fn

def closest_on_strip(strip, delta):
    cs = list(map(best_for_element(strip, delta), enumerate(strip)))
    return None if not any(cs) else min(c for c in cs if c is not None)

def x_close_to(p, distance):
    def fn(q):
        return abs(p.x - q.x) < distance
    return fn

def get_closest_pair_sorted(points, debug=False):
    # Recursion base cases
    if len(points) == 3:
        return min(Pair(points[0], points[1]),
                   Pair(points[1], points[2]),
                   Pair(points[0], points[2]))
    if len(points) == 2:
        return Pair(points[0], points[1])
    if len(points) <= 1:
        raise Exception("Finding the closest pair requires at least 2 points.")
    nFirstHalf = floor(len(points)/2)

    # points is not a list, the following is not a regular slice
    # but it's linear on the size of the slice and ensures
    # the lists it contains, remain sorted.
    firstHalf = points[0: nFirstHalf]

    s1 = get_closest_pair_sorted(firstHalf, debug=True)
    s2 = get_closest_pair_sorted(points[nFirstHalf:])
    sr = min(s1, s2)

    split_element = firstHalf[-1]
    delta = sr.distance

    strip = list(filter(x_close_to(split_element, delta), points.y_sorted))

    ss = closest_on_strip(strip, delta)

    if ss is None or ss > sr:
        return sr
    return ss


def get_closest_pair(points):
    global n
    n = len(points)
    return get_closest_pair_sorted(SortedPoints(points))

points = []
isDataRegex = r"([^ \n]+) +(\-*[\d.e\+]+) +(\-*[\d.e\+]+)"
for line in sys.stdin:
    line = line.strip()
    match = re.search(isDataRegex, line)
    if match is None:
        continue
    name = match.group(1)
    x = float(match.group(2))
    y = float(match.group(3))
    points.append(Point(name, x, y))
solution = get_closest_pair(points)
print(f'{solution.p1.name} - {solution.p2.name}: {solution.distance}')
