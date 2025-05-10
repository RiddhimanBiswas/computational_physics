import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Simulation parameters
nx, ny = 100, 100
record_length = 1 + nx * ny + nx * ny  # Each record: time (1) + a (nx*ny) + b (nx*ny)

# Directories for input files and output GIFs
input_dir = "/home/riddhiman/computational_physics/assignment_5/"
output_dir = os.path.join(input_dir, "images_assignment5")
os.makedirs(output_dir, exist_ok=True)

def extract_diffusion_params(filename):
    """
    Extract parameters from a filename with the expected format:
    Diffusion_<d_a>_<d_b>.txt

    This function mimics the manual extraction method used in your first code sample.
    
    Parameters:
        filename (str): The filename or basename to extract parameters from.
        
    Returns:
        tuple: A tuple (d_a, d_b) as strings.
        
    Raises:
        ValueError: If the filename does not match the expected format.
    """
    base = os.path.basename(filename)
    # Check that the filename starts with "Diffusion_" and ends with ".txt"
    if not (base.startswith("Diffusion_") and base.endswith(".txt")):
        raise ValueError(f"Filename {filename} does not match the expected format.")
    
    # Remove the prefix and extension.
    base_no_ext = base.replace("Diffusion_", "").replace(".txt", "")
    parts = base_no_ext.split("_")
    if len(parts) != 2:
        raise ValueError(f"Skipping file {filename} - unexpected filename format (found {len(parts)} parts).")
    return parts  # returns (d_a, d_b) as strings

# Process each file in the input directory that matches the expected filename format.
for filename in os.listdir(input_dir):
    try:
        d_a, d_b = extract_diffusion_params(filename)
    except ValueError:
        continue  # Skip files that do not match the expected pattern.

    input_filepath = os.path.join(input_dir, filename)
    output_filepath = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.gif")

    # Load and flatten numerical data from the file.
    data = np.loadtxt(input_filepath).flatten()
    
    # Determine the number of records in the data.
    nrec = len(data) // record_length
    if len(data) % record_length != 0:
        raise ValueError(f"Data size in {filename} is not a multiple of the expected record length.")

    # Preallocate arrays for time and fields 'a' and 'b'.
    times = np.empty(nrec)
    a_records = np.empty((nrec, nx, ny))
    b_records = np.empty((nrec, nx, ny))

    # Parse the flattened data into respective records.
    for k in range(nrec):
        start = k * record_length
        rec = data[start:start + record_length]
        times[k] = rec[0]
        a_flat = rec[1:1 + nx * ny]
        b_flat = rec[1 + nx * ny:]
        a_records[k, :, :] = a_flat.reshape((nx, ny))
        b_records[k, :, :] = b_flat.reshape((nx, ny))

    # Set up the figure with two subplots—one for each field.
    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(12, 5))
    im_a = ax_a.imshow(a_records[0], cmap='viridis', origin='lower')
    ax_a.set_title("Field a")
    fig.colorbar(im_a, ax=ax_a)

    im_b = ax_b.imshow(b_records[0], cmap='inferno', origin='lower')
    ax_b.set_title("Field b")
    fig.colorbar(im_b, ax=ax_b)

    # Create a title containing the simulation parameters.
    title_text = f"Diffusion: d_a = {d_a}, d_b = {d_b}"
    time_text = fig.suptitle(f"{title_text}\nTime = {times[0]:.3f}")

    def update(frame):
        im_a.set_data(a_records[frame])
        im_b.set_data(b_records[frame])
        time_text.set_text(f"{title_text}\nTime = {times[frame]:.3f}")
        return im_a, im_b, time_text

    ani = animation.FuncAnimation(fig, update, frames=nrec, interval=100, blit=False)
    ani.save(output_filepath, writer='pillow', fps=15)

    print(f"Generated GIF: {output_filepath}")
    plt.close(fig)
