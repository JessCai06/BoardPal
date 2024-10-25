import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Create figure and 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Define the grid size for the 10x10 plane
grid_size = 10

# Create the x and y coordinates
x = np.linspace(-grid_size // 2, grid_size // 2, grid_size)
y = np.linspace(-grid_size // 2, grid_size // 2, grid_size)
x, y = np.meshgrid(x, y)

# z coordinates for a flat plane (z = 0)
z = np.zeros_like(x)

# Plot the plane
ax.plot_surface(x, y, z, rstride=1, cstride=1, color='b', edgecolor='k')

# Set labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Set limits
ax.set_zlim(-1, 1)
ax.set_xlim(-grid_size // 2, grid_size // 2)
ax.set_ylim(-grid_size // 2, grid_size // 2)

# Display the plot
plt.show()
