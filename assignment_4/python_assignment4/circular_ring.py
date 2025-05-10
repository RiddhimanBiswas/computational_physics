import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ----------------------------
# Load the simulation data
# ----------------------------
file_path = "/home/riddhiman/computational_physics/assignment_4/circular_ring.txt"
data = np.loadtxt(file_path)

# Extract time and y displacement data
t = data[:, 0]              # Time values
y_data = data[:, 1:51]      # y displacements for 50 particles
v_data = data[:, 51:101]    # velocities for 50 particles

# ----------------------------
# Define the circular ring coordinates (x-z plane)
# ----------------------------
N = 50
radius = 5.0
theta = np.linspace(0, 2 * np.pi, N, endpoint=False)  # Angles for 50 particles
x_coords = radius * np.cos(theta)
z_coords = radius * np.sin(theta)

# ----------------------------
# Setup the figure and 3D plot
# ----------------------------
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# Initial plot setup
scat = ax.scatter(x_coords, z_coords, y_data[0, :], c='b', s=50, label='Particles')
ax.set_xlim(-radius - 1, radius + 1)
ax.set_ylim(-radius - 1, radius + 1)
ax.set_zlim(-2.0, 2.0)
ax.set_xlabel('X-axis')
ax.set_ylabel('Z-axis')
ax.set_zlabel('Y Displacement')
ax.set_title('Circular Ring Motion Over Time')
ax.legend()

# Add a text annotation for time
time_text = ax.text2D(0.05, 0.95, '', transform=ax.transAxes)

# ----------------------------
# Define update function for animation
# ----------------------------
def update(frame):
    # Get y-coordinates (displacement) for current frame
    y_coords = y_data[frame, :]

    # Update particle positions in 3D space
    scat._offsets3d = (x_coords, z_coords, y_coords)

    # Change marker size dynamically with velocity (optional)
    v_mag = np.abs(v_data[frame, :])
    marker_size = 50 + 100 * v_mag / np.max(v_mag)
    scat.set_sizes(marker_size)

    # Update time text
    time_text.set_text(f'Time: {t[frame]:.2f} s')

    return scat, time_text

# ----------------------------
# Create the animation
# ----------------------------
ani = FuncAnimation(fig, update, frames=len(t), interval=10, blit=False)

# Save as mp4 or just display
# ani.save('/home/riddhiman/computational_physics/assignment_4/images_assignment4/ring_animation.mp4', fps=30)
plt.show()
