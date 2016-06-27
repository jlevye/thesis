import timeit
import math
import csv
from operator import add
import copy

import numpy as np
import graph_tool.all as gt
from PIL import Image

import graph_scripts as gs

#Set up testing values
imname = "Testing/LescaThresholdCrop.png"
pointsname = "Testing/LescaPointsCrop.csv"
source = 32

image = gs.read_image(imname)
points = gs.read_points(pointsname)

#First few steps of init_graph function
disp = 600
dim = [image.shape[1], image.shape[0]]
g = gt.Graph()

gs.gen_graph_props(g)
gs.add_all_vertices(g, points, image, dim, disp)

cirDict = gs.make_all_circles(g, image)
im = image
a = points[34]
b = points[36]
thresh = 1

start = timeit.default_timer()
if a == b:
    print("False")
step1 = timeit.default_timer()

p = points[:]
p.remove(a)
step2 = timeit.default_timer()

height = im.shape[0] - 1
width = im.shape[1] - 1
step3 = timeit.default_timer()

#cir = copy.deepcopy(cirDict)
pass
step4 = timeit.default_timer()

keyA = "({x},{y})".format(x = int(a[0]), y = int(a[1]))
circle = cirDict[keyA]
step5 = timeit.default_timer()

del cirDict[keyA]
finish_setup = timeit.default_timer()

newpoint = a
minDist = 999999
for c in circle:
   if gs.distance(c, b) < minDist:
       minDist = gs.distance(c,b)
       newpoint = c
a = newpoint

adjust_a = timeit.default_timer()

for item in cirDict.values():
    for point in item:
        if point[0] > width: point[0] = width
        if point[1] > height: point[1] = height
        p.append(point)


endzone = gs.full_circle(b, gs.biggest_circle(b,im), im.shape)

setup_ending = timeit.default_timer()

h = -1 if a[0] > b[0] else 1 #Move left or right
v = -1 if a[1] > b[1] else 1 #Move up or down

end = a
stop = 0

count = 0
all_pre_main_loop = timeit.default_timer()

while stop == 0:
    count += 1
    #Have we hit b? Have we hit an edge?
    if end[0] == b[0] or end[0] == width: h = 0
    if end[1] == b[1] or end[1] == height: v = 0
    if [h,v] == [0,0]:
        stop = 1

    testX = end[0] + h
    testY = end[1] + v

    #Test the possible directions we can move.
    if h is not 0 and im[end[1]][testX] > thresh:
        end[0] = testX
        if end in p: stop=1
    elif v is not 0 and im[testY][end[0]] > thresh:
        end[1] = testY
        if end in p: stop=1
    elif im[testY][testX] > thresh:
        end = [testX,testY]
        if end in p: stop=1
    else:
        stop = 1

finished_loop = timeit.default_timer()

cirDict[keyA] = circle
if end in endzone:
    print("True")
else:
    print("False")

done = timeit.default_timer()

total = done - start
basic_setup = finish_setup - start
move_a = adjust_a - finish_setup
build_endzone = setup_ending - adjust_a
total_init = all_pre_main_loop - start
main_loop = finished_loop - all_pre_main_loop
single_loop = main_loop/count
check_return = done - finished_loop

print("Time report:\n")
# print("Number of steps: {}".format(count))
# print("Total run time: {} sec".format(total))
# print("Initialization: {} sec; {}% of total".format(total_init, (total_init/total)*100))
# print("\tFirst steps: {} sec; {}% of setup time".format(basic_setup, (basic_setup/total_init)*100))
# print("\tMove start to closest point: {}; {}% of setup ti".format(move_a, (move_a/total_init)*100))
# print("\tSet up end conditions: {}; {}% of setup ti".format(build_endzone, (build_endzone/total_init)*100))
# print("Main loop of function: {} sec; {}% of total".format(main_loop, (main_loop/total)*100))
# print("\tTime per loop: {}".format(single_loop))
# print("Time to report final value: {} sec; {}% of total".format(check_return, (check_return/total)*100))
print("First steps time breakdown:")
print("{}% of total runtime".format((basic_setup/total)*100))
print("Check if points are equal: {}%".format(((step1-start)/basic_setup)*100))
print("Copy point list: {}%".format(((step2-step1)/basic_setup)*100))
print("Set bounds: {}%".format(((step3-step2)/basic_setup)*100))
print("Deep copy dictionary: {}%".format(((step4-step3)/basic_setup)*100))
print("Get circle around start: {}%".format(((step5-step4)/basic_setup)*100))
print("Delete circle A from dict: {}%".format(((finish_setup-step5)/basic_setup)*100))
