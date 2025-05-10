import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
nx, ny = 100, 100
# Each record contains: time (1) + a (nx*ny) + b (nx*ny) = 1 + 10000 + 10000 = 20001 numbers
record_length = 1 + nx*ny + nx*ny

filename = "/home/riddhiman/computational_physics/assignment_5/Diffusion_1.000_100.000.txt"

# Read all numbers from file.
# Depending on the Fortran list-directed output, the file might have line breaks not corresponding to records.
# We load all numbers and then break them into records.
data = np.loadtxt(filename)
data = data.flatten()

# Determine number of records
nrec = len(data) // record_length
if len(data) % record_length != 0:
    raise ValueError("Data size is not a multiple of expected record length.")

# Preallocate lists for times and fields.
times = np.empty(nrec)
a_records = np.empty((nrec, nx, ny))
b_records = np.empty((nrec, nx, ny))

# Parse the flat data array into records.
for k in range(nrec):
    start = k * record_length
    rec = data[start:start+record_length]
    times[k] = rec[0]
    a_flat = rec[1:1+nx*ny]
    b_flat = rec[1+nx*ny:]
    a_records[k,:,:] = a_flat.reshape((nx, ny))
    b_records[k,:,:] = b_flat.reshape((nx, ny))

# Setup the figure and two subplots (one for each field)
fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(12, 5))

# Create initial plots using imshow. Adjust vmin and vmax if you have a known range.
im_a = ax_a.imshow(a_records[0], cmap='viridis', origin='lower')
ax_a.set_title("Field a")
fig.colorbar(im_a, ax=ax_a)

im_b = ax_b.imshow(b_records[0], cmap='inferno', origin='lower')
ax_b.set_title("Field b")
fig.colorbar(im_b, ax=ax_b)

time_text = fig.suptitle("Time = {:.3f}".format(times[0]))

def update(frame):
    im_a.set_data(a_records[frame])
    im_b.set_data(b_records[frame])
    time_text.set_text("Time = {:.3f}".format(times[frame]))
    return im_a, im_b, time_text

ani = animation.FuncAnimation(fig, update, frames=nrec, interval=100, blit=False)
ani.save('/home/riddhiman/computational_physics/assignment_5/test_images/diffusion_animation.gif', writer='pillow', fps=30)

plt.tight_layout()
plt.show()