import matplotlib.pyplot as plt

MAX = 50

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __eq__(self, other) :
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False
    def to_tuple(self):
        return self.x, self.y

# DRAW BOARD (GRID)
def draw_board():
    # create a figure to draw the board (8inch x 8inch)
    fig = plt.figure(figsize=[8,8])

    # set the background color
    #fig.patch.set_facecolor((0.85,0.64,0.125))

    # add subplot (?????) (axis object?)
    ax = fig.add_subplot(111)
    # turn off the axes
    ax.set_axis_off()

    return fig, ax

#DRAWS GRIDS ON SUBPLOT
def draw_grids(ax):
    # draw the vertical lines - 50 in total
    for x in range(MAX):
        ax.plot([x, x], [0,MAX-1], color = '0.75', linestyle='dotted')

    # draw the horizontal lines
    for y in range(MAX):
        ax.plot([0, MAX-1], [y,y], color = '0.75', linestyle='dotted')
    ax.set_position([0,0.02,1,1])


# DRAW POINTS ---------------------------
# DRAW SOURCE POINT
def draw_source(ax, x, y):
    ax.plot(x,y,'o',markersize=4,
        markeredgecolor='b',
        markerfacecolor='b',
        markeredgewidth=1)
    # ARGUMENT EXPLANATION________
    # o - marker style (o is a circle)
    # markersize - size of marker (diameter in points) .... same with markeredgewidth
    # ='b' - blue

# DRAW DESTINATION POINT
def draw_dest(ax, x, y):
    ax.plot(x,y,'o',markersize=4,
        markeredgecolor='r',
        markerfacecolor='r',
        markeredgewidth=1)

# DRAW RED POINT (DUPLICATE REALLY)
def draw_red_point(ax, x, y):
    ax.plot(x,y,'o',markersize=4,
        markeredgecolor='r',
        markerfacecolor='r',
        markeredgewidth=1)

# USED FOR POLYGON DRAWING (ENCLOSURE)
def draw_black_point(ax, x, y):
    ax.plot(x,y,'o',markersize=4,
        markeredgecolor=(0,0,0),
        markerfacecolor='k',
        markeredgewidth=1)

# USED FOR POLYGON DRAWING (TURF)
def draw_green_point(ax, x, y):
    ax.plot(x,y,'o',markersize=4,
        markeredgecolor='g',
        markerfacecolor='g',
        markeredgewidth=1)
#----------------------------------------

# FOR DRAWING ENCLOSURE LINES
def draw_line(ax, xs, ys):
    ax.plot(xs, ys, color='k')

# FOR DRAWING OUR PATH'S LINES
def draw_result_line(ax, xs, ys):
    ax.plot(xs, ys, color='r')

# FOR DRAWING TURF LINES
def draw_green_line(ax, xs, ys):
    ax.plot(xs, ys, color='g')
