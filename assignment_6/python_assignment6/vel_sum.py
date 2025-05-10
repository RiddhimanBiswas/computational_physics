import numpy as np
import matplotlib.pyplot as plt

# --- Load velocity data ---
vel_data = np.loadtxt("/home/riddhiman/computational_physics/assignment_6/vel_data_debug.txt")
n_frames, total_columns = vel_data.shape

# --- Extract iteration numbers ---
iters = vel_data[:, 0].astype(int)

# --- Extract and reshape velocity data ---
vel_only = vel_data[:, 1:]
n_particles = vel_only.shape[1] // 3
velocities = vel_only.reshape(n_frames, n_particles, 3)

# --- Compute total momentum per frame ---
total_momentum = np.sum(velocities, axis=1)  # shape: (n_frames, 3)
momentum_x = total_momentum[:, 0]
momentum_y = total_momentum[:, 1]
momentum_z = total_momentum[:, 2]
momentum_magnitude = np.linalg.norm(total_momentum, axis=1)

# --- Plotting ---
plt.figure(figsize=(10, 6))
plt.plot(iters, momentum_x, label='Px', linestyle='--')
plt.plot(iters, momentum_y, label='Py', linestyle='-.')
plt.plot(iters, momentum_z, label='Pz', linestyle=':')
plt.plot(iters, momentum_magnitude, label='|P|', color='black', linewidth=2)

plt.xlabel('Iteration')
plt.ylabel('Total Momentum')
plt.title('Total Momentum Components and Magnitude vs Iteration')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
