import random
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation

# generate arbitrary matrix
class CustomGrid:
    def __init__(self, InputGrid):
        self.InputGrid = InputGrid
        self.rows = len(InputGrid)
        self.cols = len(InputGrid[0])

        self.grid = [[Node(x, y, InputGrid[x][y]) for y in range(self.cols)] for x in range(self.rows)]
        self.empty = [[0 for j in range(self.cols)] for i in range(self.rows)]

    def printGrid(self):
        print(self.grid)

    def printEmpty(self):
        plt.matshow(self.empty)
        plt.show()

    def getNode(self, x, y):
        return self.grid[x][y]


class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "({},{})".format(self.x, self.y)


class Node(Point2D):
    # class constructor, initializes the node's coordinates and its value in the matrix
    def __init__(self, x, y, value):
        super().__init__(x, y)
        self.value = value

    def __repr__(self):
        return "{}".format(self.value)

    def printCoordValue(self):
        print("Node of value: {} at coordinates ({},{})".format(self.value, self.x, self.y))


# simulates a queue
class Queue:
    def __init__(self):
        self.size = 0
        self.queue = []

    # queues an object of type Node
    def enqueue(self, node):
        self.queue.append(node)
        self.size += 1
        return node

    # dequeues (removes the first element of the queue) and returns the element removed
    def dequeue(self):
        if (self.size > 0):
            cur = self.queue.pop(0)
            self.size -= 1
            return cur
        
        else:
            raise IndexError("Queue has no elements, cannot pop")

    # gets node at index i
    def get(self, i):
        if (i >= 0 and i < self.size):
            return self.queue[i]
        
        else:
            raise IndexError("List index out of range")

    # prints out the entire queue
    def printQueue(self):
        for i in range(self.size):
            print("({},{}) -> {} at index {}".format(self.queue[i].x, self.queue[i].y, self.queue[i].value, i))

class LeastResistance:
    # BFS implementation
    def __init__(self, grid, x_input, y_input):
        self.grid = grid
        self.x_input = x_input
        self.y_input = y_input
        self.travelled = []

    def canMove(self, x, y):
        if (x >= 0 and x < self.grid.rows and y >= 0 and y < self.grid.cols):
            return True
        
        else:
            return False

    # finds the minimum nodes around the root node
    def findMin(self, node, minima):
        # order of preferred travel direction
        directions = [[1, 1], [1, 0], [0, 1], [1, -1], [-1, 1], [-1, 0]] # [0, -1], [-1, -1] directions were excluded for aesthetic purposes

        for direction in directions:
            new_x = node.x + direction[0]
            new_y = node.y + direction[1]
            
            if (self.canMove(new_x, new_y) == True and self.grid.empty[new_x][new_y] != -1):
                minima.append(self.grid.getNode(new_x, new_y))
                
            else:
                continue

        return len(minima)

    def updateOrder(self):
        root = self.grid.grid[self.x_input][self.y_input]
        self.BFS_Traversal(root)
        return self.grid

    def BFS_Traversal(self, root):
        q = Queue()
        q.enqueue(root)
        
        while q.size > 0:
            minima = []
            cur = q.dequeue()
            point = Point2D(cur.x, cur.y)

            self.grid.empty[cur.x][cur.y] = -1
            self.travelled.append(point)
            
            if (cur.value != 0):
                found = self.findMin(cur, minima)

            # if the algorithm reaches an entry of zero, it terminates
            else:
                found = 0

            if found > 0:
                minima.sort(key=lambda c: c.value)

                for i in range(1, len(minima)):
                    if minima[i].value != minima[i - 1].value:
                        minima = minima[:i]
                        break

                for mins in minima:
                    q.enqueue(mins)
                    self.grid.empty[mins.x][mins.y] = -1

            else:
                continue

# user inputs
print('Enter a number of rows, e.g.: 100:')
x_row = int(input())

print('Enter a number of columns, e.g.: 100:')
y_col = int(input())

print('Enter a minimum resistance value, e.g.: 1:')
min_res = float(input())

print('Enter a maximum resistance value, e.g.: 200:')
max_res = float(input())

print('Enter a starting position, e.g.: 0, 0:')
x_input, y_input = input().split(",")
x_input = int(x_input)
y_input = int(y_input)

# algorithm initialization
grid = CustomGrid(np.random.randint(min_res, max_res, size=(x_row, y_col)))
current = LeastResistance(grid, x_input, y_input)
current.updateOrder()
print(current.travelled)


# creation of empty matrix
empty = [[0 for j in range(current.grid.cols)] for i in range(current.grid.rows)]

#animation function
def animate(i): 
    try:
        print(i)
        x = current.travelled[i].x
        y = current.travelled[i].y
        empty[x][y] = i + 100
        ax.clear()
        ax.matshow(empty, cmap='Blues')

    except IndexError:
        print("EZ")
        return empty

fig, ax = plt.subplots()

ani = FuncAnimation(fig, animate, frames = len(current.travelled), interval = 0.0001, repeat = False)
# ani.save('Least_Resistance.gif', writer='pillow', fps=120, dpi=100)
plt.show()
