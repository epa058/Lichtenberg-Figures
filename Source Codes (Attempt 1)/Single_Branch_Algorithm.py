import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

# list of visited entries
travelled = [(0, 0)]
    
class LeastResistance:
    def __init__(self):

        # number of rows
        self.rows = len(grid)

        # number of columns
        self.columns = len(grid[0])

        # all 8 directions
        self.directions = [[1, 1], [1, 0], [0, 1], [1, -1], [-1, 1], [0, -1],  [-1, 0]] # [-1, -1] direction was excluded for aesthetic purposes

    def updateOrder(self, grid, row, col):
        global travelled
        
        # dictionary of all possible neighbouring entries of (row, col)
        coords = {}

        # searches all directions using for loop
        for x, y in self.directions:
            new_row, new_col = row + x, col + y

            # records the direction travelled (key) and new grid entry value (value) into dictionary
            if (0 <= new_row < self.rows and 0 <= new_col < self.columns and tuple([new_row, new_col]) not in travelled):
                coords[tuple([x, y])] = grid[new_row][new_col] 

            # does not record the coordinates into the dictionary coords
            else:
                continue

        # if the dictionary is empty, the algorithm can't go anywhere and terminates
        if bool(coords.values()) == False:
            return True

        else:
            # key of minimum entry in coords
            get_min = min(coords, key = coords.get)
            
            new_row, new_col = row + get_min[0], col + get_min[1]
            travelled.append(tuple([new_row, new_col]))

            # if the algorithm reaches an entry of zero, it terminates
            if grid[new_row][new_col] == 0:
                return True

            # recursively calls itself
            else:
                return self.updateOrder(grid, new_row, new_col)


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
grid = np.random.randint(min_res, max_res, size = (x_row, y_col))
current = LeastResistance()
current.updateOrder(grid, x_input, y_input)
print(travelled)


# creation of empty matrix
empty = np.zeros((len(grid), len(grid[0])))

def animate(i):
    try:
        print(i)
        empty[travelled[i][0]][travelled[i][1]] = i + 100
        ax.clear()
        ax.matshow(empty, cmap = 'Blues')

    except IndexError:
        print("EZ")
        return empty

fig, ax = plt.subplots()

ani = animation.FuncAnimation(fig, animate, frames = len(travelled), interval = 0.001, repeat = False)
# ani.save('LeastResistance.gif', writer = 'pillow', fps = 5, dpi = 100)
plt.show()

