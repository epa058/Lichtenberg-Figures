import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation

# Create a circular grid
print('Enter a radius, e.g.: 50:')
N = 2*int(input())+1

# Anisotropy generator
print('Include anisotropies? (Yes / No):')
anis = str(input()).upper()

if anis == "YES":
    grid = np.random.randint(0, 2, size=(N, N))

else:
    grid = np.zeros((N, N))

# Midpoint circle algorithm
perimeter = [] # List of points on circle
r = (N - 1) // 2 # Ensures radius is within grid
x0, y0 = N // 2, N // 2 # Coordinates of center of grid

f = 1 - r # Decision parameter
dx, dy = 1, - 2 * r # Increment values for x and y
x, y = 0, r # Algorithm start point

# Records cardinal points on boundary
perimeter.append((x0, y0 + r))
perimeter.append((x0, y0 - r))
perimeter.append((x0 + r, y0))
perimeter.append((x0 - r, y0))

# While loop to record remainder of circle
while x < y:
    # Move upwards
    if f >= 0:
        y -= 1
        dy += 2
        f += dy
    # Move rightwards
    x += 1
    dx += 2
    f += dx
    
    # Record boundary points by symmetry
    perimeter.append((x0 + x, y0 + y))
    perimeter.append((x0 - x, y0 + y))
    perimeter.append((x0 + x, y0 - y))
    perimeter.append((x0 - x, y0 - y))
    perimeter.append((x0 + y, y0 + x))
    perimeter.append((x0 - y, y0 + x))
    perimeter.append((x0 + y, y0 - x))
    perimeter.append((x0 - y, y0 - x))

# Set boundary conditions
grid[x0, y0] = 0
for i, j in perimeter:
    grid[i, j] = 1
    
# Set grid values outside disk to zero
for i in range(N):
    for j in range(N):
        if ((i - x0)**2 + (j - y0)**2) > r**2 and grid[i, j] != 1:
            grid[i, j] = 0

# Create a list of growth points
growth = []
    
# Set growth site
growRow = x0
growCol = y0
growPt = (growRow, growCol)
grid[growPt] = 0
growth.append(growPt)

# Define the Laplace operator
def laplaceOperator(grid):
    global growth
    N = len(grid)
    pts = []
    
    for i in range(N):
        for j in range(N):
            if ((i - x0)**2 + (j - y0)**2) < r**2:
                pt = (i, j)
                pts.append(pt)
                
    # Update each point in the randomized order
    np.random.shuffle(pts)
    for i, j in pts:
        if (i, j) not in growth and (i, j) not in perimeter:
            up = grid[i-1, j]
            down = grid[i+1, j]
            left = grid[i, j-1]
            right = grid[i, j+1]
            grid[i, j] = (left + right + up + down) / 4
    return grid

# Define Laplace's equation
def laplaceEquation(grid, iterations = 100):
    for _ in range(iterations):
        grid = laplaceOperator(grid)
    #print(grid)
    return grid

# Initializing Laplace's equation on the grid
grid = laplaceEquation(grid)

def simulation(grid):
    global growth
    N = len(grid)
    
    # Find all possible growth sites
    possibleSites = []
    for i, j in growth:
        for delta_i, delta_j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Displacements: up, down, left, right
            new_i, new_j = i + delta_i, j + delta_j
            
            if ((new_i - x0)**2 + (new_j - y0)**2) < r**2 and (new_i, new_j) not in perimeter and (new_i, new_j) not in growth:
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
        return grid

    # Select next growth site
    newPoint = random.choices(possibleSites, weights = probabilities, k = 1)[0]
    print(newPoint)

    # Add new growth site to growth list
    grid[newPoint] = 0
    growth.append(newPoint)

    # Terminate if reached boundary
    if ((newPoint[0] - x0)**2 + (newPoint[1] - y0)**2) >= (r - 1)**2:
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
Grid = np.zeros((N, N))
    
# Animation
def animate(i): 
    try:
        print(i)
        x = growth[i][0]
        y = growth[i][1]
        grid[x][y] = i + 100
        ax.clear()
        ax.matshow(grid, cmap='Blues')

    except IndexError:
        print("Done")
        return grid

fig, ax = plt.subplots()

ani = FuncAnimation(fig, animate, frames = len(growth), interval = 0.0001, repeat = False)
# ani.save('DBM.gif', writer='pillow', fps=120, dpi=100)
plt.show()


'''
# Simple plotting
newGrid = np.zeros((N, N))
for i, j in growth:
    newGrid[i, j] = 1
    
fig, ax = plt.subplots()
ax.matshow(grid, cmap='Blues')
ax.matshow(newGrid, cmap='Blues')
# Ticks
ax.set_xticks(np.arange(-0.5, N, 1), minor=True)
ax.set_yticks(np.arange(-0.5, N, 1), minor=True)
ax.grid(which='minor', linestyle='-', linewidth=1)

plt.show()
'''
