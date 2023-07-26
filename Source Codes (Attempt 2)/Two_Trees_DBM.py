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
grid[0, :] = -10
grid[-1, :] = 10

# Create two lists of growth points
growthUp = []
growthDown = []

# Set the growth site
growRowUp, growColUp = 0, y_col // 2
growPtUp = (growRowUp, growColUp)
growthUp.append(growPtUp)

growRowDown, growColDown = x_row-1, y_col // 2
growPtDown = (growRowDown, growColDown)
growthDown.append(growPtDown)

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

# Define the Laplace operator
def laplaceOperator(grid):
    x_row = len(grid)
    y_col = len(grid[0])
    newGrid = grid.copy()
    
    for i in range(1, x_row - 1): # keeps the first and last row values fixed
        for j in range(0, y_col):
            if (i, j) not in growthUp and (i, j) not in growthDown:
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
    return grid

def simulation(grid, direction="up"):
    global growthUp
    global growthDown
    x_row = len(grid)
    y_col = len(grid[0])
    
    if direction == "up":
        growth = growthUp
        otherGrowth = growthDown
    elif direction == "down":
        growth = growthDown
        otherGrowth = growthUp
    
    # Find all possible growth sites
    possibleSites = []
    for i, j in growth:
        for delta_i, delta_j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Displacements: up, down, left, right
            new_i, new_j = i + delta_i, (j + delta_j) % y_col
            
            if 0 <= new_i < x_row and (new_i, new_j) not in growth:
                possibleSites.append((new_i, new_j))

    # Terminate if the algorithm is stuck or if the trees touch
    if len(possibleSites) == 0 or bool(set(growthUp) & set(growthDown)) == True: 
        return grid

    # Calculate growth probability for each possible growth site
    if direction == "up":
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
        grid[newPoint] = -10 # negative value to ensure it attracts downGrowth
        growth.append(newPoint)
        
    elif direction == "down":
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
        grid[newPoint] = 10 # positive value to ensure it attracts upGrowth
        growth.append(newPoint)

    # Update the grid and recursively call the simulation function
    grid = laplaceEquation(grid)
    if direction == "up":
        grid = simulation(grid, "down")
    elif direction == "down":
        grid = simulation(grid, "up")
        
    return grid

# Begin the simulation
grid = simulation(grid)

# Results
print(grid)
print(growthUp)
print(growthDown)

# Cleaner results
Grid = np.zeros((x_row, y_col))
    
# Animation
def animate(i): 
    try:
        print(i)
        x = growthUp[i][0]
        y = growthUp[i][1]
        Grid[x][y] = i + 100
        
        x = growthDown[i][0]
        y = growthDown[i][1]
        Grid[x][y] = i + 200
        ax.clear()
        ax.matshow(Grid, cmap='Blues')

    except IndexError:
        print("Done!")
        return Grid

fig, ax = plt.subplots()

growth = min(growthUp, growthDown)
    
ani = FuncAnimation(fig, animate, frames = len(growth), interval = 0.0001, repeat = False)
ani.save('DBM.gif', writer='pillow', fps=120, dpi=100)
plt.show()

'''
# Simple plotting
newGrid = np.zeros((n, n))
for i, j in growthUp:
    newGrid[i, j] = -10
for i, j in growthDown:
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

