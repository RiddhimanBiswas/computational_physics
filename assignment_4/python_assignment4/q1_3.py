import numpy as np
import matplotlib.pyplot as plt

# Load the data from the file.
# Assumes the file columns are: x, y_actual, y_euler, y_mod, y_imp.
data = np.loadtxt("/home/riddhiman/computational_physics/assignment_4/q1_3_values.txt")

# Extract columns into separate arrays.
x = data[:, 0]
y_actual = data[:, 1]
y_euler = data[:, 2]
y_mod = data[:, 3]
y_imp = data[:, 4]

# Find the index for x closest to 1.550
target_x = 1.550
index = np.argmin(np.abs(x - target_x))

# Get the values at that index.
x_val = x[index]
yA = y_actual[index]
yE = y_euler[index]
yM = y_mod[index]
yI = y_imp[index]

# Compute the differences.
diff_euler = yA - yE
diff_mod   = yA - yM
diff_imp   = yA - yI

# Print the differences in the terminal.
print(f"At x = {x_val:.3f}:")
print(f"  Difference (y_actual - y_euler)     = {diff_euler:.6f}")
print(f"  Difference (y_actual - y_mod)       = {diff_mod:.6f}")
print(f"  Difference (y_actual - y_imp)       = {diff_imp:.6f}")

# Plot the solutions.
plt.figure(figsize=(10, 6))
plt.plot(x, y_actual, label="Actual (tan x)", linewidth=2)
plt.plot(x, y_euler, label="Euler", linestyle="--")
plt.plot(x, y_mod, label="Modified Euler", linestyle="-.")
plt.plot(x, y_imp, label="Implicit Euler", linestyle=":")
plt.xlabel("x")
plt.ylabel("y")
plt.title(r"Solutions of the Differential Equation: $y' = y^2 + 1$")
plt.legend()
plt.grid(True)
plt.show()