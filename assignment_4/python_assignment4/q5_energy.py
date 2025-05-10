import numpy as np
import matplotlib.pyplot as plt

# Load data from the file
# The file is assumed to have three columns: t, x, v.
data = np.loadtxt("/home/riddhiman/computational_physics/assignment_4/nonlinear_rk4_q7b.txt")

# Extract columns into separate arrays
t = data[:, 0]
x = data[:, 1]
v = data[:, 2]
K_E = 0.5 * v**2  # Kinetic Energy
P_E = 1 - np.cos(x)  # Potential Energy (assuming U(x) = 1 - cos(x))
E = K_E + P_E  # Total Energy

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(t, K_E, label="Kinetic Energy (K_E)", linewidth=2)
plt.plot(t, P_E, label="Potential Energy (P_E)", linestyle="--", linewidth=2)
plt.plot(t, E, label="Total Energy (E)", linestyle="-.", linewidth=2)
plt.xlabel("Time (t)")
plt.ylabel("Energy")
plt.title("Energy Curves for $\\frac{d^2x}{dt^2} = -\\sin(x)$\nInitial Conditions: $x(0) = 0$, $v(0) = 2.1$", fontsize=14)
plt.legend(loc="best", fontsize=12)
plt.grid(True)
plt.show()