import numpy as np
import matplotlib.pyplot as plt
import math

# Load the velocity data from the file.
data = np.loadtxt("/home/riddhiman/computational_physics/assignment_6/vel_data_debug.txt")

iterations = data[:, 0]
vel_data = data[:, 1:]
final_vel = vel_data[-1, :]
n_particles = final_vel.size // 3
final_vel = final_vel.reshape(n_particles, 3)

# Compute the speed (magnitude of the velocity) for each particle.
speeds = np.linalg.norm(final_vel, axis=1)

# Plot a histogram for the simulated speed distribution.
num_bins = 50
plt.hist(speeds, bins=num_bins, density=True, alpha=0.5, label='Simulated speeds')

# Maxwell-Boltzmann distribution (assuming m = 1 and k_B = 1)
# The MB speed distribution in 3D at temperature T is:
# f(v) = 4*pi * (1/(2*pi*T))^(3/2) * v^2 * exp(-v^2/(2*T))

T = 1.0   # adjust if your simulation uses a different temperature

def mb_distribution(v, T):
    return 4 * math.pi * (1.0 / (2 * math.pi * T))**1.5 * v**2 * np.exp(-v**2 / (2 * T))

# Create an array of speed values to evaluate the Maxwell–Boltzmann function.
v_vals = np.linspace(0, speeds.max()*1.1, 100)
mb_vals = [mb_distribution(v, T) for v in v_vals]

# Plot the theoretical Maxwell-Boltzmann distribution.
plt.plot(v_vals, mb_vals, 'r--', lw=2, label='Maxwell-Boltzmann')

plt.xlabel("Speed")
plt.ylabel("Probability Density")
plt.title("Speed Distribution vs. Maxwell-Boltzmann Distribution")
plt.legend()
plt.grid(True)
plt.show()
