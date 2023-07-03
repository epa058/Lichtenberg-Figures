import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation

# Create an n x n grid of zeros
n = 51
grid = np.zeros((n, n))

# Create two lists of growth points
growthUp = []
growthDown = []

# Set boundary conditions
grid[0, :] = -10
grid[-1, :] = 10

# Initializing Laplace's equation on the grid
iterations = 500
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
    for i in range(1, n - 1): # keeps the first and last row values fixed
        for j in range(0, n):
            if (i, j) not in growthUp and (i, j) not in growthDown:
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

def simulation(grid, direction="up"):
    global growthUp
    global growthDown
    n = len(grid[0])
    
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
            new_i, new_j = i + delta_i, (j + delta_j) % n
            
            if 0 <= new_i < n and (new_i, new_j) not in growth:
                possibleSites.append((new_i, new_j))

    # Terminate if the algorithm is stuck
    if len(possibleSites) == 0 or bool(set(growthUp) & set(growthDown)) == True: 
        return grid

    # Calculate growth probability for each possible growth site
    if direction == "up":
        probabilities = []

        for i, j in possibleSites:
            prob = grid[i, j]
            probabilities.append(prob)

        minProb = min(probabilities)
        shiftedProbabilities = [(p + abs(minProb))**2 for p in probabilities]
        
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
        grid[newPoint] = -10
        growth.append(newPoint)
        
    elif direction == "down":
        probabilities = []
        for i, j in possibleSites:
            prob = -grid[i, j]
            probabilities.append(prob)

        minProb = min(probabilities)
        shiftedProbabilities = [(p + abs(minProb))**2 for p in probabilities]

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
        grid[newPoint] = 10
        growth.append(newPoint)

    # Update the grid and recursively call the simulation function
    grid = laplaceEquation(grid)
    if direction == "up":
        grid = simulation(grid, "down")
    elif direction == "down":
        grid = simulation(grid, "up")
        
    return grid

# Set the growth site
growRowUp, growColUp = 0, n // 2
growPtUp = (growRowUp, growColUp)
growthUp.append(growPtUp)

growRowDown, growColDown = n-1, n // 2
growPtDown = (growRowDown, growColDown)
growthDown.append(growPtDown)

# Begin the simulation
grid = simulation(grid)

# Results
print(grid)

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

# Cleaner results
newGrid = np.zeros((n, n))
    
# Animation
def animate(i): 
    try:
        print(i)
        x = growthUp[i][0]
        y = growthUp[i][1]
        newGrid[x][y] = i + 100
        
        x = growthDown[i][0]
        y = growthDown[i][1]
        newGrid[x][y] = i + 200
        ax.clear()
        ax.matshow(newGrid, cmap='Blues')

    except IndexError:
        print("Done")
        return newGrid

fig, ax = plt.subplots()

growth = min(growthUp, growthDown)
    
ani = FuncAnimation(fig, animate, frames = len(growth), interval = 0.0001, repeat = False)
ani.save('DBM.gif', writer='pillow', fps=120, dpi=100)
plt.show()
