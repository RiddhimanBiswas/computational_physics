import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

# --- Parameters ---
n_particles = 1200
box_length = 20.0
data_file = "/home/riddhiman/computational_physics/assignment_6/pos_data_debug.txt"  # your Fortran output file
tracked_indices = [0, 100, 200, 300, 400]  # indices of particles to track

# --- Load data ---
data = np.loadtxt(data_file)

# Frame count
n_frames = data.shape[0]

# Extract iterations and positions
iters = data[:, 0].astype(int)
positions = data[:, 1:]  # shape: (n_frames, 3 * n_particles)

# Reshape into (n_frames, n_particles, 3)
positions = positions.reshape(n_frames, n_particles, 3)

# --- Plotting Setup ---
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(0, box_length)
ax.set_ylim(0, box_length)
ax.set_zlim(0, box_length)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Particle Movement Over Time')

# Create two scatter plots:
# 1. All particles (lighter gray)
sc_all = ax.scatter([], [], [], s=3, color='#BBBBBB', label='Other particles')

# 2. Tracked particles (color coded)
tracked_colors = ['r', 'g', 'b', 'c', 'm']
sc_tracked = []
for i, color in enumerate(tracked_colors):
    label = f"Tracked {tracked_indices[i]}"
    s = ax.scatter([], [], [], s=30, color=color, label=label)
    sc_tracked.append(s)

# Static legend (prevent flickering)
ax.legend(loc='upper right')

# --- Update function for animation ---
def update(frame):
    pos = positions[frame]

    # Update all particle positions
    sc_all._offsets3d = (pos[:, 0], pos[:, 1], pos[:, 2])

    # Update tracked particles
    for i, idx in enumerate(tracked_indices):
        particle_pos = pos[idx]
        sc_tracked[i]._offsets3d = ([particle_pos[0]], [particle_pos[1]], [particle_pos[2]])

    ax.set_title(f"Iteration: {iters[frame]}")
    return [sc_all] + sc_tracked

# --- Create animation ---
ani = animation.FuncAnimation(fig, update, frames=n_frames, interval=150, blit=False)  # ~6.6 fps

# --- Show animation ---
plt.tight_layout()
plt.show()

# --- Save as GIF ---
ani.save('/home/riddhiman/computational_physics/assignment_6/images_assignment6/lowT_particle_motion_tracked.gif',
         writer='pillow', fps=10, dpi=200)

# --- Optional: Save as MP4 ---
# ani.save('particle_motion_tracked.mp4', fps=7, dpi=200)
