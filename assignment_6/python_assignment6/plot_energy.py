import matplotlib.pyplot as plt
import numpy as np

# Load the data from the file
data = np.loadtxt("/home/riddhiman/computational_physics/assignment_6/energy_debug.txt")

# Unpack the columns
iter = data[:, 0]
V_tot = data[:, 1]
K_tot = data[:, 2]
E_tot = data[:, 3]

# Calculate mean and standard deviation
V_mean = np.mean(V_tot)
V_std = np.std(V_tot)

K_mean = np.mean(K_tot)
K_std = np.std(K_tot)

E_mean = np.mean(E_tot)
E_std = np.std(E_tot)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(iter, V_tot, label=f"V_tot (Potential)\nμ = {V_mean:.3f}, σ = {V_std:.3f}", linewidth=2)
plt.plot(iter, K_tot, label=f"K_tot (Kinetic)\nμ = {K_mean:.3f}, σ = {K_std:.3f}", linewidth=2)
plt.plot(iter, E_tot, label=f"E_tot (Total)\nμ = {E_mean:.3f}, σ = {E_std:.3f}", linewidth=2)

# Formatting
plt.xlabel("Iteration")
plt.ylabel("Energy")
plt.title("Energy vs. Iteration")
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()
