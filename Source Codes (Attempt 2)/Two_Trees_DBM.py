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
grid[:, 0] = -10
grid[:, -1] = 10

# Create two lists of growth points
growthLeft = []
growthRight = []

# Set the growth site
growRowLeft, growColLeft = x_row // 2, 0
growPtLeft = (growRowLeft, growColLeft)
growthLeft.append(growPtLeft)

growRowRight, growColRight = x_row // 2, y_col - 1
growPtRight = (growRowRight, growColRight)
growthRight.append(growPtRight)

# Initializing Laplace's equation on the grid
iterations = 500
for _ in range(iterations):
    for i in range(0, x_row):
        for j in range(1, y_col-1): # Keeps the first and last column values fixed
            up = grid[(i-1) % x_row, j]
            down = grid[(i+1) % x_row, j]
            left = grid[i, (j-1)]
            right = grid[i, (j+1)]
            grid[i, j] = (left + right + up + down) / 4

# Define the Laplace operator
def laplaceOperator(grid):
    x_row = len(grid)
    y_col = len(grid[0])
    newGrid = grid.copy()
    
    for i in range(0, x_row): # keeps the first and last row values fixed
        for j in range(1, y_col-1):
            if (i, j) not in growthLeft and (i, j) not in growthRight:
                up = grid[(i-1) % x_row, j]
                down = grid[(i+1) % x_row, j]
                left = grid[i, j-1]
                right = grid[i, j+1]
                newGrid[i, j] = (left + right + up + down) / 4
    return newGrid

# Define Laplace's equation
def laplaceEquation(grid, iterations = 500):
    for _ in range(iterations):
        grid = laplaceOperator(grid)
    return grid

def simulation(grid, direction="left"):
    global growthLeft
    global growthRight
    x_row = len(grid)
    y_col = len(grid[0])
    
    if direction == "left":
        growth = growthLeft
        otherGrowth = growthRight
    elif direction == "right":
        growth = growthRight
        otherGrowth = growthLeft
    
    # Find all possible growth sites
    possibleSites = []
    for i, j in growth:
        for delta_i, delta_j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Displacements: up, down, left, right
            new_i, new_j = (i + delta_i) % x_row, j + delta_j
            
            if 0 <= new_j < y_col and (new_i, new_j) not in growth:
                possibleSites.append((new_i, new_j))

    # Terminate if the algorithm is stuck or if the trees touch
    if len(possibleSites) == 0 or bool(set(growthLeft) & set(growthRight)) == True: 
        return grid

    # Calculate growth probability for each possible growth site
    if direction == "left":
        probabilities = []

        for i, j in possibleSites:
            prob = grid[i, j]
            probabilities.append(prob)

        # Shift probability values upwards so that the trees won't clump themselves together
        minProb = min(probabilities)
        k = 1 # you can set k equal to 2 or 1/2 as well
        shiftedProbabilities = [(p + abs(minProb))**k for p in probabilities]
        
        # Normalize probabilities
        totalProb = sum(shiftedProbabilities)
        if totalProb != 0:
            shiftedProbabilities = [p / totalProb for p in shiftedProbabilities]
        else:
            shiftedProbabilities = [1 / len(possibleSites)] * len(possibleSites)

        # Select next growth site
        newPoint = random.choices(possibleSites, weights = shiftedProbabilities, k = 1)[0]
        print(newPoint)

        # Add new growth site to growth list
        grid[newPoint] = -10 # negative value to ensure it attracts rightGrowth
        growth.append(newPoint)
        
    elif direction == "right":
        probabilities = []
        for i, j in possibleSites:
            prob = -grid[i, j] # negative sign to ensure non-negative probability
            probabilities.append(prob)
            
        # Shift probability values upwards so that the trees won't clump themselves together
        minProb = min(probabilities)
        k = 1 # you can set k equal to 2 or 1/2 as well
        shiftedProbabilities = [(p + abs(minProb))**k for p in probabilities]

        # Normalize probabilities
        totalProb = sum(shiftedProbabilities)
        if totalProb != 0:
            shiftedProbabilities = [p / totalProb for p in shiftedProbabilities]
        else:
            shiftedProbabilities = [1 / len(possibleSites)] * len(possibleSites)

        # Select next growth site
        newPoint = random.choices(possibleSites, weights = shiftedProbabilities, k = 1)[0]
        print(newPoint)

        # Add new growth site to growth list
        grid[newPoint] = 10 # positive value to ensure it attracts leftGrowth
        growth.append(newPoint)

    # Update the grid and recursively call the simulation function
    grid = laplaceEquation(grid)
    if direction == "left":
        grid = simulation(grid, "right")
    elif direction == "right":
        grid = simulation(grid, "left")
        
    return grid

# Begin the simulation
grid = simulation(grid)

# Results
print(grid)
print(growthLeft)
print(growthRight)

# Cleaner results
Grid = np.zeros((x_row, y_col))
    
# Animation
def animate(i): 
    try:
        print(i)
        x = growthLeft[i][0]
        y = growthLeft[i][1]
        Grid[x][y] = i + 100
        
        x = growthRight[i][0]
        y = growthRight[i][1]
        Grid[x][y] = i + 200
        ax.clear()
        ax.matshow(Grid, cmap='Blues')

    except IndexError:
        print("Done!")
        return Grid

fig, ax = plt.subplots()

growth = min(growthLeft, growthRight)
    
ani = FuncAnimation(fig, animate, frames = len(growth), interval = 0.0001, repeat = False)
ani.save('DBM.gif', writer='pillow', fps=120, dpi=100)
plt.show()

'''
# Simple plotting
newGrid = np.zeros((n, n))
for i, j in growthLeft:
    newGrid[i, j] = -10
for i, j in growthRight:
    newGrid[i, j] = 10
    
fig, ax = plt.subplots()
ax.matshow(grid, cmap='Blues')
ax.matshow(newGrid, cmap='Blues')
# Ticks
ax.set_xticks(np.arange(-0.5, n, 1), minor=True)
ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
ax.grid(which='minor', linestyle='-', linewidth=1)

cbar = plt.colorbar(ax.matshow(newGrid, cmap='Blues'))
cbar.set_label('Colorbar Label')

plt.show()
'''

