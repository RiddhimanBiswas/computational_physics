import numpy as np
import matplotlib.pyplot as plt

# Load data from the file
# The file is assumed to have three columns: t, x, v.
data = np.loadtxt("/home/riddhiman/computational_physics/assignment_4/nonlinear_rk4_q6_mod.txt")

# Extract columns into separate arrays
t = data[:, 0]
x = data[:, 1]
v = data[:, 2]

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(t, x, label="x (position)", linewidth=2)
plt.plot(t, v, label="v (velocity)", linestyle="--", linewidth=2)
plt.xlabel("Time (t)")
plt.ylabel("Value")
plt.title("Second-Order ODE: $\\frac{d^2x}{dt^2} = -\\sin(x)$\nInitial Conditions: $x(0) = 0$, $v(0) = 2$", fontsize=14)
plt.legend(loc="best", fontsize=12)
plt.grid(True)
plt.show()