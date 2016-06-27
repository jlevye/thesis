import graph_scripts as gs
import heapq

def edge_tester2(points, image, circle, N, pct = False):
    if len(points) < 10: N = len(points)
    if pct:
        N = round(N/100*len(points))

    distances =  [[gs.distance(x, y) for x in points] for y in points]
    #used = []
    edges = []

    for start in points:
        index = points.index(start)
        row = distances[index]
        mins = heapq.nsmallest(N,row)

        neighbors = [points[row.index(x)] for x in mins]
        for end in neighbors:
            if start == end:
                continue
            else:
                try:
                    val = gs.is_edge(start, end, image, points, circle)
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
        #used.append(start)
    return edges
