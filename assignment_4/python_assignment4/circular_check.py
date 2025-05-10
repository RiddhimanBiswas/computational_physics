import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# Load and inspect the data
# ----------------------------
file_path = "/home/riddhiman/computational_physics/assignment_4/circular_ring.txt"

# Load data from the file
data = np.loadtxt(file_path)

# Extracting columns
t = data[:, 0]              # Time
y_data = data[:, 1:51]      # Displacements of 50 particles
v_data = data[:, 51:101]    # Velocities of 50 particles
K_E = data[:, 101]          # Kinetic Energy
P_E = data[:, 102]          # Potential Energy
E = data[:, 103]            # Total Energy

# ----------------------------
# Quick sanity check
# ----------------------------
print(f"Time steps: {len(t)}")
print(f"Max displacement: {np.max(y_data)}")
print(f"Min displacement: {np.min(y_data)}")
print(f"Max total energy: {np.max(E):.4f}")
print(f"Min total energy: {np.min(E):.4f}")
print(f"Average total energy: {np.mean(E):.4f}")
print(f"Energy deviation: {np.max(E) - np.min(E):.4e}")

# ----------------------------
# Plotting to visualize data
# ----------------------------

# Plot Energy vs Time
plt.figure(figsize=(12, 6))
plt.plot(t, K_E, label="Kinetic Energy", color="blue")
plt.plot(t, P_E, label="Potential Energy", color="green")
plt.plot(t, E, label="Total Energy", color="red", linestyle="--")
plt.xlabel("Time (t)")
plt.ylabel("Energy")
plt.title("Energy Conservation Check")
plt.legend()
plt.grid(True)
plt.show()

# Plot displacement of a few particles over time
plt.figure(figsize=(12, 6))
for i, j in [(0, 25), (1, 49), (10, 35)]:  # Plot particle pairs
    plt.plot(t, y_data[:, i], label=f"Particle {i+1}", linestyle="-")
    plt.plot(t, y_data[:, j], label=f"Particle {j+1} (superposing)", linestyle="--")
plt.xlabel("Time (t)")
plt.ylabel("Displacement (y)")
plt.title("Displacement of Selected Particles Over Time (Superposing Pairs)")
plt.legend()
plt.grid(True)
plt.show()

# ----------------------------
# Energy Conservation Check
# ----------------------------
energy_deviation = np.max(E) - np.min(E)
if energy_deviation < 1e-5:
    print("✅ Energy is conserved! System looks good.")
else:
    print("⚠️ Warning: Energy drift detected! Check the timestep and RK4 implementation.")

    # ----------------------------
    # Position of the 1st particle after 2000 iterations
    # ----------------------------
index = 2000  # Corresponding to t=40
if index < len(t):
    position_1st_particle = y_data[index, 0]
    print(f"The position of the 1st particle after 2000 iterations (t=40) is: {position_1st_particle:.4f}")
else:
    print("Index out of range. Check the number of iterations or time steps.")
