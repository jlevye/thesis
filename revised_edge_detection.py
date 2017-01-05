#New way of defining point - object w/ a bunch of information
class Point:
    def __init__(self, index, x, y, g = None):
        self.i = index
        self.x = x
        self.y = y
        if g:
            try:
                self.v = g.vertices[index]
            except AttributeError:
                print("g is not a graph. Vertex not set.")
                pass
        else:
            self.v = None

def edge_finding(points, image, circleDict):
    N = len(points)
    pairs = [[j for j in range(N) if j > i] for i in range(N)]
    edges = []

    for s in range(N):
        s_coord = points[s]
        s_key = "({x},{y})".format(x = s_coord[0], y = s_coord[1])
        targets = pairs[s]

        #Set up our zone around the
        terminate =

    #Code that gets the vertex of the circle point we landed in
    endpoint_options = [list(eval(key)) for key, val in circleDict if p in val]
    if len(endpoint_options) > 1:
        #Get the closest one; this is a pretty edge case
        dist = 999999
        end = []
        for point in endpoint options:
            if distance(s, point) < dist:
                dist = distance(s,point)
                end_coord = point
    else:
        end_coord = endpoint_options[0]
    end = points.index(end_coord)


#To check very close edges, see if circles around them overlap on a black square
def overlap(intersection, image):
    for p in intersection:
        if image[p[1]][p[0]] > 0:
            return True
        else:
            return False


def step_between(start, end, image, terminate, pred = None):
    #Grab the options of pixels to move toward around our center
    circle = make_circle(start, 1)
    circle = dedup(circle)
    #Correct the ring: if it's not where we came from, not ineligible,
    ring = [[point, distance(point, end)] for point in circle if image[point[1]][point[0]] > 0 and (point not in terminate) and point != pred ]

    #Return when we're out of options and haven't yet returned true
    if ring == []:
        return False
    else:
        ring.sort(key = lambda x: x[1])
        for point_pair in ring:
            point = point_pair[0]
            if point == end:
                return True
            else:
                status = step_between(point, end, image, terminate, start)
                if status == True:
                    return True
    #If we haven't returned yet, make sure we can't follow this line again and return false:
    terminate.append(start)
    return False

def is_edge(a, b, image, points, circleDict, messages = False):
    """Uses recursive path-finding algorithm instead of original one. Assumes binary image with bad pixels 0."""

    terminate = [point for point in points if point != a and point != b]
    keyA = "({x},{y})".format(x = a[0], y = a[1])
    keyB = "({x},{y})".format(x = b[0], y = b[1])

    #Check if very close together
    intersection = [p for p in circleDict[keyA] if p in circleDict[keyB]]
    if len(intersection) > 0:
        if overlap(intersection, image):
            return True
        else:
            return False

    for key in circleDict.keys():
        if key != keyA and key != keyB:
            for point in circleDict[key]:
                terminate.append(point)

    terminate = dedup(terminate)

    try:
        if step_between(a, b, image, terminate):
            return True
        else:
            return False
    except RecursionError:
        if messages:
            print("Points {0},{1} give recursion error.".format(points.index(a), points.index(b)))
        else:
            pass

def edge_tester(points, image, circle):
    """Given a list of points, checks the possible edges between them. Slow!"""
    #Debug log
    #test 1: delete points as used - only lets one direction of edges get added.

    toTest = [[j for j in range(len(points)) if j > i] for i in range(len(points))]
    edges = []

    for start in points:
        for end in points:
            if start == end:
                continue
            else:
                try:
                    val = is_edge(start, end, image, points, circle)
                except IndexError:
                    print("Start = {}; End = {}".format(start, end))
                    print("Hit an out-of-bound index.")
                    continue
                except Exception as e:
                    print("Start = {}; End = {}".format(start, end))
                    print("Hit some other error: {}.".format(e))
                    continue
                else:
                    if val:
                        edges.append([points.index(start), points.index(end)])
    #    points.remove(start)
    return edges
