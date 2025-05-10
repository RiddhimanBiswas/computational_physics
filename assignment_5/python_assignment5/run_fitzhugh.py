import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import glob
import os

# Dimensions and record size
nx, ny = 100, 100
record_length = 1 + nx*ny + nx*ny  # time + a (nx*ny) + b (nx*ny)

# Get all files matching the pattern
file_list = glob.glob("/home/riddhiman/computational_physics/assignment_5/Turing_*.txt")

for filename in file_list:
    # Extract parameters from the filename.
    # Expected filename format: "Turing_<d_a>_<d_b>_<alpha>_<beta>.txt"
    base = os.path.basename(filename)
    base_no_ext = base.replace("Turing_", "").replace(".txt", "")
    parts = base_no_ext.split("_")
    if len(parts) != 4:
        print(f"Skipping file {filename} - unexpected filename format.")
        continue
    da, db, alpha, beta = parts

    # Load the data from the file and flatten it
    data = np.loadtxt(filename).flatten()
    nrec = len(data) // record_length
    if len(data) % record_length != 0:
        print(f"Data size mismatch in {filename}. Skipping.")
        continue

    # Preallocate arrays for time and fields
    times = np.empty(nrec)
    a_records = np.empty((nrec, nx, ny))
    b_records = np.empty((nrec, nx, ny))

    # Parse the flat data into records
    for k in range(nrec):
        start = k * record_length
        rec = data[start:start + record_length]
        times[k] = rec[0]
        a_flat = rec[1:1 + nx * ny]
        b_flat = rec[1 + nx * ny:]
        a_records[k, :, :] = a_flat.reshape((nx, ny))
        b_records[k, :, :] = b_flat.reshape((nx, ny))

    # Create a figure and two subplots
    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(12, 5))

    im_a = ax_a.imshow(a_records[0], cmap='viridis', origin='lower')
    ax_a.set_title("Field a")
    fig.colorbar(im_a, ax=ax_a)

    im_b = ax_b.imshow(b_records[0], cmap='inferno', origin='lower')
    ax_b.set_title("Field b")
    fig.colorbar(im_b, ax=ax_b)

    # Title including parameters; time will update in the animation as well.
    base_title = r"Turing: $D_a=" + da + r", D_b=" + db + r", \alpha=" + alpha + r", \beta=" + beta + r"$"
    fig.suptitle(base_title + f" | Time = {times[0]:.3f}")

    def update(frame):
        im_a.set_data(a_records[frame])
        im_b.set_data(b_records[frame])
        fig.suptitle(base_title + f" | Time = {times[frame]:.3f}")
        return im_a, im_b

    # Create the animation using the Pillow writer (GIF)
    ani = animation.FuncAnimation(fig, update, frames=nrec, interval=100, blit=False)
    gif_filename = base.replace(".txt", ".gif")
    output_path = "/home/riddhiman/computational_physics/assignment_5/images_assignment5/"
    gif_filename = os.path.join(output_path, base.replace(".txt", ".gif"))
    ani.save(gif_filename, writer='pillow', fps=15)
    print(f"Saved animation to {gif_filename}")

    # Close the figure to free up memory before processing the next file.
    plt.close(fig)
