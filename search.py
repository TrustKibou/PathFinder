import matplotlib.pyplot as plt
import matplotlib.animation as animation
from shapely.geometry import Point as ShapelyPoint
from shapely.geometry.polygon import Polygon as ShapelyPolygon
import numpy as np
import time

from utils import *
from grid import *

#pip install shapely



######################################### BOARD-RELATED
# READ FILE FOR ENCLOSURES/TURFS
def gen_polygons(worldfilepath):
    polygons = []
    with open(worldfilepath, "r") as f:
        lines = f.readlines()
        lines = [line[:-1] for line in lines]
        for line in lines:
            polygon = []
            pts = line.split(';')
            for pt in pts:
                xy = pt.split(',')
                polygon.append(Point(int(xy[0]), int(xy[1])))
            polygons.append(polygon)
    return polygons


# CREATE BOARD
def create_board():

    global listOfEnclosures, listOfTurfs, fig, ax

    # CREATE BOARD (fig) AND SUBPLOT (ax)
    fig, ax = draw_board()

    # DRAW ACTUAL GRID
    draw_grids(ax)

    # DRAW STARTING & ENDING POINTS
    draw_source(ax, source.x, source.y)  # source point
    draw_dest(ax, dest.x, dest.y)  # destination point

    # DRAW POLYGONS

    enclosureCoordinates = [] # keep track of enclosure coordinates for each enclosure
    i = 0

    ### ENCLOSURES
    for polygon in epolygons:
        enclosureCoordinates.append([]) # add new sublist
        for p in polygon:
            draw_black_point(ax, p.x, p.y)
            enclosureCoordinates[i].append((p.x, p.y)) # add coordinates to sublist
        i += 1
    for polygon in epolygons:
        for i in range(0, len(polygon)):
            draw_line(ax, [polygon[i].x, polygon[(i + 1) % len(polygon)].x], # the modulus operator ensures that the last point in polygon loops back to the original point
                      [polygon[i].y, polygon[(i + 1) % len(polygon)].y])

    # ADD INITIAL POINT TO END FOR EACH ENCLOSURE & CREATE POLYGON
    for sublist in enclosureCoordinates:
        sublist.append(sublist[0])
        listOfEnclosures.append(ShapelyPolygon(sublist))



    turfCoordinates = []
    i = 0

    ### TURFS
    for polygon in tpolygons:
        turfCoordinates.append([])
        for p in polygon:
            draw_green_point(ax, p.x, p.y)
            turfCoordinates[i].append((p.x, p.y))
        i += 1
    for polygon in tpolygons:
        for i in range(0, len(polygon)):
            draw_green_line(ax, [polygon[i].x, polygon[(i+1)%len(polygon)].x], [polygon[i].y, polygon[(i+1)%len(polygon)].y])

    for sublist in turfCoordinates:
        sublist.append(sublist[0])
        listOfTurfs.append(ShapelyPolygon(sublist))


# DRAW PATH LINE
def draw_path_line(node):

    if (node == None):
        print("No possible path can be made")
    else:
        while (node.pastNode is not None):
            pastNode = node.pastNode
            draw_result_line(ax, [node.x, pastNode.x], [node.y, pastNode.y])
            node = pastNode

    # DISPLAY
    plt.show()




######################################### SEARCH ALGORITHMS
numOfExpanded = 0

# BREADTH FIRST SEARCH
def breadth_first_search():

    global numOfExpanded

    node = Node(source.x, source.y, 0, None)

    # if (agentPosition == dest):
    #     return agentPosition

    frontier = Queue()
    frontier.push(node)
    reached = {(node.x, node.y)}


    while (not frontier.isEmpty()):
        node = frontier.pop()
        numOfExpanded += 1
        for child in expandNodes(node):
            if (child.x == dest.x and child.y == dest.y): return child
            if (not reached.__contains__((child.x,child.y))):
                reached.add((child.x, child.y))
                frontier.push(child)
    return None # failure


# DEPTH FIRST SEARCH
def depth_first_search():

    global numOfExpanded
    node = Node(source.x, source.y, 0, None)

    frontier = Stack()
    frontier.push(node)
    reached = {(node.x, node.y)}

    while (not frontier.isEmpty()):
        node = frontier.pop()
        numOfExpanded += 1
        if (node.x == dest.x and node.y == dest.y): return node
        for child in expandNodes(node):
            if (not reached.__contains__((child.x, child.y))):
                frontier.push(child)
                reached.add((child.x, child.y))
    return None # failure


# GREEDY BEST FIRST SEARCH
def greedy_first_search():

    global numOfExpanded
    node = Node(source.x, source.y, 0, None)

    frontier = PriorityQueue()
    frontier.push(node, node.heuristic)
    reached = {(node.x, node.y):node}

    while (not frontier.isEmpty()):
        node = frontier.pop()
        numOfExpanded += 1
        if (node.x == dest.x and node.y == dest.y): return node
        for child in expandNodes(node):
            state = (child.x, child.y)

            if (not reached.__contains__(state)
                    or (child.heuristic < reached.get(state).heuristic)):
                reached[state] = child
                frontier.push(child, child.heuristic)
    return None # failure


# A* SEARCH
def a_star_search():

    global numOfExpanded

    node = Node(source.x, source.y, 0, None)

    frontier = PriorityQueue()
    frontier.push(node, node.pathCost + node.heuristic)
    reached = {(node.x, node.y):node}

    while (not frontier.isEmpty()):
        node = frontier.pop()
        numOfExpanded += 1
        if (node.x == dest.x and node.y == dest.y): return node
        for child in expandNodes(node):
            state = (child.x, child.y)

            if (not reached.__contains__(state)
                    or ((child.pathCost + child.heuristic < reached.get(state).pathCost + reached.get(state).heuristic))):
                reached[state] = child
                frontier.push(child, child.pathCost + child.heuristic)
    return None # failure



######################################### SEARCH ASSISTANTS
# NODE CLASS
class Node:
    def __init__(self, x, y, pathCost, pastNode):
        self.x = x
        self.y = y
        self.pathCost = pathCost
        self.pastNode = pastNode
        self.heuristic = ShapelyPoint(x,y).distance(ShapelyPoint(dest.x, dest.y))

    def __hash__(self):
        return hash((self.x, self.y))


# GET CHILDREN NODES OF PARENT NODES
def expandNodes(node):

    up, right, down, left = agent_actions(node)

    # INSTEAD OF LOOP, WE JUST HARDCODE 4 ACTIONS
    if (up):
        yield Node(node.x, node.y+1, node.pathCost + action_cost(node, "up"), node) #action_cost(node, "up", chkStandardCost, chkHeuristicCost)
    if (right):
        yield Node(node.x+1, node.y, node.pathCost + action_cost(node, "right"), node)
    if (down):
        yield Node(node.x, node.y-1, node.pathCost + action_cost(node, "down"), node)
    if (left):
        yield Node(node.x-1, node.y, node.pathCost + action_cost(node, "left"), node)


# CALCULATE ACTION COST
def action_cost(node, action):

    cost = 0

    # CHECK IF EITHER CURRENT NODE POSITION OR FUTURE NODE POSITION INTERSECT TURF
    for turf in listOfTurfs:
        if ((action == "up" and turf.intersects(ShapelyPoint(node.x, node.y+1)))
        or (action == "right" and turf.intersects(ShapelyPoint(node.x+1, node.y)))
        or (action == "down" and turf.intersects(ShapelyPoint(node.x, node.y-1)))
        or (action == "left" and turf.intersects(ShapelyPoint(node.x-1, node.y)))):
            cost = 1.5
            break
        else:
            cost = 1.0
            break

    return cost


# GET AVAILABLE ACTIONS FOR A NODE
def agent_actions(agentPosition):
    # BOOLEAN VALUES FOR MOVEMENT ACTIONS
    up = True
    right = True
    down = True
    left = True

    upPosition = ShapelyPoint(agentPosition.x, agentPosition.y+1)
    rightPosition = ShapelyPoint(agentPosition.x+1, agentPosition.y)
    downPosition = ShapelyPoint(agentPosition.x, agentPosition.y-1)
    leftPosition = ShapelyPoint(agentPosition.x-1, agentPosition.y)


    for enclosure in listOfEnclosures:
        # UP
        if (enclosure.intersects(upPosition) or (upPosition.y == 50)):
            up = False
        # RIGHT
        if (enclosure.intersects(rightPosition) or (rightPosition.x == 50)):
            right = False
        # DOWN
        if (enclosure.intersects(downPosition) or (downPosition.y == -1)):
            down = False
        # LEFT
        if (enclosure.intersects(leftPosition) or (leftPosition.x == -1)):
            left = False

    return up, right, down, left


######################################### MAIN PROGRAM
# GLOBAL VARIABLES
listOfEnclosures = []   # keep a list of all points in each enclosure
listOfTurfs = []        # keep a list of all points in each enclosure
fig = None              # figure for board
ax = None               # axis for board

# ONLY EXECUTE WHEN MAIN FILE
if __name__ == "__main__":

    # ENABLE INTERACTIVE
    # plt.ion()

    # SET POLYGON FILES - USES FILE READER FUNCT
    epolygons = gen_polygons('TestingGrid/world1_enclosures.txt')
    tpolygons = gen_polygons('TestingGrid/world1_turfs.txt')

    # SET STARTING/ENDING PT
    # source = Point(8, 10) to 43,45
    source = Point(8,10)
    dest = Point(43,45)

    # EXECUTION LOOP
    while (True):
        print("Which search algorithm would you like the agent to use?:", "1 - Depth First Search", "2 - Breadth First Search", "3 - Greedy Best First Search", "4 - A*", "5 - Quit Program", sep="\n")
        choice = input("")

        # CREATE BOARD
        create_board()

        # DEPTH FIRST SEARCH OPTION
        if (choice == "1"):
            numOfExpanded = 0
            node = depth_first_search()
            # print(numOfExpanded-1) # LAST NODE IS NOT EXPANDED
            draw_path_line(node)


        # BREADTH FIRST SEARCH OPTION
        elif (choice == "2"):
            numOfExpanded = 0
            node = breadth_first_search()
            # print(numOfExpanded)
            draw_path_line(node)


        # GREEDY BEST FIRST SEARCH OPTION
        elif (choice == "3"):
            numOfExpanded = 0
            node = greedy_first_search()
            # print(numOfExpanded-1) # LAST NODE IS NOT EXPANDED
            draw_path_line(node)


        # A* SEARCH OPTION
        elif (choice == "4"):
            numOfExpanded = 0
            node = a_star_search()
            # print(numOfExpanded-1) # LAST NODE IS NOT EXPANDED
            draw_path_line(node)


        # EXIT OPTION
        elif (choice == "5"):
            print("Thanks for visiting!")
            exit(0)

        # ERROR CATCHER
        else:
            print("You entered an incorrect value. Please try again")










