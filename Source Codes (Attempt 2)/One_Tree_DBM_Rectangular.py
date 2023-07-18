import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import sys
print(sys.getrecursionlimit())
sys.setrecursionlimit(2000)
print(sys.getrecursionlimit())

# Create a rectangular grid of zeros
print('Enter a number of rows, e.g.: 100:')
x_row = int(input())

print('Enter a number of columns, e.g.: 100:')
y_col = int(input())

# Anisotropy generator
print('Include anisotropies? (Yes / No):')
anis = str(input()).upper()

if anis == "YES":
    grid = np.random.randint(0, 2, size=(x_row, y_col))

else:
    grid = np.zeros((x_row, y_col))

# Set boundary conditions
grid[0, :] = 0
grid[-1, :] = 10

# Create a list of growth points
growth = []

# Set the growth site
'''
print('Enter a starting position, e.g.: 0, 0:')
growRow, growCol = input().split(",")
growRow = int(growRow)
growCol = int(growCol)
growPt = (growRow, growCol)
grid[growPt] = 0
growth.append(growPt)
'''
growRow = 0
growCol = y_col // 2
growPt = (growRow, growCol)
growth.append(growPt)

# Initializing Laplace's equation on the grid
iterations = 100
for _ in range(iterations):
    for i in range(1, x_row-1): # Keeps the first and last row values fixed
        for j in range(0, y_col):
            up = grid[i-1, j]
            down = grid[i+1, j]
            left = grid[i, (j-1) % y_col]
            right = grid[i, (j+1) % y_col]
            grid[i, j] = (left + right + up + down) / 4
# print(grid)

# Define the Laplace operator
def laplaceOperator(grid):
    x_row = len(grid)
    y_col = len(grid[0])
    newGrid = grid.copy()
    
    for i in range(1, x_row - 1): # Keeps the first and last row values fixed
        for j in range(0, y_col):
            if (i, j) not in growth:
                up = grid[i-1, j]
                down = grid[i+1, j]
                left = grid[i, (j-1) % y_col]
                right = grid[i, (j+1) % y_col]
                newGrid[i, j] = (left + right + up + down) / 4
    return newGrid

# Define Laplace's equation
def laplaceEquation(grid, iterations = 100):
    for _ in range(iterations):
        grid = laplaceOperator(grid)
    # print(grid)
    return grid

def simulation(grid):
    global growth
    x_row = len(grid)
    y_col = len(grid[0])
    
    # Find all possible growth sites
    possibleSites = []
    for i, j in growth:
        for delta_i, delta_j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Displacements: up, down, left, right
            new_i, new_j = i + delta_i, (j + delta_j) % y_col
            
            if 0 < new_i < x_row and (new_i, new_j) not in growth:
                possibleSites.append((new_i, new_j))

    # Terminate if the algorithm is stuck
    if len(possibleSites) == 0: 
        return grid

    # Calculate growth probability for each possible growth site
    probabilities = []
    for i, j in possibleSites:
        prob = grid[i, j]**2 # you can square or square root this
        probabilities.append(prob)

    # Normalize probabilities
    totalProb = sum(probabilities)
    if totalProb != 0:
        probabilities = [p / totalProb for p in probabilities]
    else:
        probabilities = [1 / len(possibleSites)] * len(possibleSites)

    # Select next growth site
    newPoint = random.choices(possibleSites, weights = probabilities, k = 1)[0]
    print(newPoint)

    # Add new growth site to growth list
    grid[newPoint] = 0
    growth.append(newPoint)
    if newPoint[0] == x_row - 1:
        return grid

    # Update the grid and recursively call the simulation function
    grid = laplaceEquation(grid)
    grid = simulation(grid)

    return grid

# Begin the simulation
grid = simulation(grid)

# Results
print(grid)
print(growth)

# Cleaner results
Grid = np.zeros((x_row, y_col))
    
# Animation
def animate(i): 
    try:
        #print(i)
        x = growth[i][0]
        y = growth[i][1]
        Grid[x][y] = i + 100
        ax.clear()
        ax.matshow(Grid, cmap='Blues')

    except IndexError:
        print("Done!")
        return Grid

fig, ax = plt.subplots()

ani = FuncAnimation(fig, animate, frames = len(growth), interval = 0.0001, repeat = False)
ani.save('DBM.gif', writer='pillow', fps=120, dpi=100)
plt.show()

'''
# Simple plotting
newGrid = np.zeros((x_row, y_col))
for i, j in growth:
    newGrid[i, j] = 1
    
fig, ax = plt.subplots()
ax.matshow(grid, cmap='Blues')
ax.matshow(newGrid, cmap='Blues')
# Ticks
ax.set_xticks(np.arange(-0.5, x_row, 1), minor=True)
ax.set_yticks(np.arange(-0.5, y_col, 1), minor=True)
ax.grid(which='minor', linestyle='-', linewidth=1)

plt.show()
'''
