import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation

# Create an n x n grid of zeros
n = 21
grid = np.zeros((n, n))

# Create a list of growth points
growth = []

# Set boundary conditions
grid[0, :] = 0
grid[-1, :] = 1

# Initializing Laplace's equation on the grid
iterations = 100
for _ in range(iterations):
    for i in range(1, n-1): # Keeps the first and last row values fixed
        for j in range(0, n):
            up = grid[i-1, j]
            down = grid[i+1, j]
            left = grid[i, (j-1) % n]
            right = grid[i, (j+1) % n]
            grid[i, j] = (left + right + up + down) / 4

# Define the Laplace operator
def laplaceOperator(grid):
    n = len(grid[0])
    newGrid = grid.copy()
    for i in range(1, n - 1): # Keeps the first and last row values fixed
        for j in range(0, n):
            if (i, j) not in growth:
                up = grid[i-1, j]
                down = grid[i+1, j]
                left = grid[i, (j-1) % n]
                right = grid[i, (j+1) % n]
                newGrid[i, j] = (left + right + up + down) / 4
    return newGrid

# Define Laplace's equation
def laplaceEquation(grid, iterations = 100):
    for _ in range(iterations):
        grid = laplaceOperator(grid)
    return grid

def simulation(grid):
    global growth
    n = len(grid[0])
    
    # Find all possible growth sites
    possibleSites = []
    for i, j in growth:
        for delta_i, delta_j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Displacements: up, down, left, right
            new_i, new_j = i + delta_i, (j + delta_j) % n
            
            if 0 < new_i < n and (new_i, new_j) not in growth:
                possibleSites.append((new_i, new_j))

    # Terminate if the algorithm is stuck
    if len(possibleSites) == 0: 
        return grid

    # Calculate growth probability for each possible growth site
    probabilities = []
    for i, j in possibleSites:
        prob = grid[i, j]**2
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
    if newPoint[0] == n - 1:
        return grid

    # Update the grid and recursively call the simulation function
    grid = laplaceEquation(grid)
    grid = simulation(grid)

    return grid

# Set the growth site
growRow, growCol = 0, n // 2
growPt = (growRow, growCol)
#grid[growPt] = 0
growth.append(growPt)

# Begin the simulation
grid = simulation(grid)


# Results
print(grid)

# Cleaner results
newGrid = np.zeros((n, n))
    
# Animation
def animate(i): 
    try:
        print(i)
        x = growth[i][0]
        y = growth[i][1]
        newGrid[x][y] = i + 100
        ax.clear()
        ax.matshow(newGrid, cmap='Blues')

    except IndexError:
        print("Done")
        return newGrid

fig, ax = plt.subplots()

ani = FuncAnimation(fig, animate, frames = len(growth), interval = 0.0001, repeat = False)
# ani.save('DBM.gif', writer='pillow', fps=120, dpi=100)
plt.show()


'''
# Simple plotting
newGrid = np.zeros((n, n))
for i, j in growth:
    newGrid[i, j] = 1
    
fig, ax = plt.subplots()
ax.matshow(grid, cmap='Blues')
ax.matshow(newGrid, cmap='Blues')
# Ticks
ax.set_xticks(np.arange(-0.5, n, 1), minor=True)
ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
ax.grid(which='minor', linestyle='-', linewidth=1)

plt.show()
'''
