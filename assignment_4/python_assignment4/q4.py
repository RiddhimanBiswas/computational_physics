import numpy as np
import matplotlib.pyplot as plt

# Load the data from the file.
# Assumes the file has three columns: x, y_actual, y_rk4.
data = np.loadtxt("/home/riddhiman/computational_physics/assignment_4/q4_values.txt")

# Extract the columns.
x = data[:, 0]
y_actual = data[:, 1]
y_rk4 = data[:, 2]

# Find the index for x closest to 1.55.
target_x = 1.55
index = np.argmin(np.abs(x - target_x))

# Get the values at that index.
x_val = x[index]
yA = y_actual[index]
yRK4 = y_rk4[index]

# Compute the difference.
difference = yA - yRK4

# Print the difference in the terminal.
print(f"At x = {x_val:.3f}, difference (y_actual - y_rk4) = {difference:.6f}")

# Plot the actual solution and the RK4 solution.
plt.figure(figsize=(10, 6))
plt.plot(x, y_actual, label="Actual (tan x)", linewidth=2)
plt.plot(x, y_rk4, label="RK4", linestyle="--")
plt.xlabel("x")
plt.ylabel("y")
plt.title("RK4 Solution vs. Actual (tan x)")
plt.legend()
plt.grid(True)
plt.show()