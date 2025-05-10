import numpy as np
import matplotlib.pyplot as plt

# Load data from the file; assumes three columns: i, j, T(i,j)
data = np.loadtxt('/home/riddhiman/computational_physics/assignment_4/laplace_neumann.txt')

# Determine grid dimensions from the i and j columns
nx = int(np.max(data[:, 0]))
ny = int(np.max(data[:, 1]))

# Initialize a 2D array to store the temperature values.
# Adjust for Fortran's 1-indexing by subtracting 1.
T = np.zeros((nx, ny))
for row in data:
    i, j, t = row
    T[int(i)-1, int(j)-1] = t

# Create coordinate arrays for plotting.
# The i index will be on the x-axis and j on the y-axis.
x = np.arange(1, nx+1)
y = np.arange(1, ny+1)
X, Y = np.meshgrid(x, y, indexing='ij')

# Print the temperature at a specific point (10, 10) in the grid.
print(f"Temperature at (10, 10): {T[9, 9]}")

# Plot the temperature profile using a filled contour plot with finer resolution.
plt.figure(figsize=(8, 6))
contour = plt.contourf(X, Y, T, levels=100, cmap='viridis')  # Increase the number of levels for finer detail
plt.colorbar(contour, label='Temperature')
plt.xlabel('Grid Index i')
plt.ylabel('Grid Index j')
plt.title('Temperature Profile, Neumann Boundary Conditions')
plt.show()
