import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Simulation grid dimensions and record length
nx, ny = 100, 100
record_length = 1 + nx * ny + nx * ny  # time (1) + a (nx*ny) + b (nx*ny)

# Directory containing the files and output directory for images
input_path = "/home/riddhiman/computational_physics/assignment_5/"
output_path = "/home/riddhiman/computational_physics/assignment_5/images_assignment5/"
os.makedirs(output_path, exist_ok=True)

# Get all files matching the Turing pattern
file_list = glob.glob(os.path.join(input_path, "Turing_*.txt"))

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

    # Preallocate arrays for time and for fields a and b
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

    base_title = r"Turing: $D_a=" + da + r", \, D_b=" + db + r", \, \alpha=" + alpha + r", \, \beta=" + beta + r"$"

    # (2) Plot the time evolution of total concentration for fields a and b.
    # Compute total concentration at each time step by summing over the grid.
    total_a = np.array([np.sum(a_records[i]) for i in range(nrec)])
    total_b = np.array([np.sum(b_records[i]) for i in range(nrec)])

    # Create a new figure to plot total concentration evolution
    fig2, ax = plt.subplots(figsize=(8, 6))
    ax.plot(times, total_a, label="Total a", color='blue', marker='o')
    ax.plot(times, total_b, label="Total b", color='red', marker='x')
    ax.set_xlabel("Time")
    ax.set_ylabel("Total Concentration")
    ax.set_title(base_title + " - Total Concentration vs Time")
    ax.legend()
    plot_filename = base.replace(".txt", "_total.png")
    plot_filepath = os.path.join(output_path, plot_filename)
    fig2.savefig(plot_filepath)
    print(f"Saved total concentration plot to {plot_filepath}")
    plt.close(fig2)
