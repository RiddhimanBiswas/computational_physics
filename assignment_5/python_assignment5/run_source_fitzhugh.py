import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Simulation grid dimensions
nx, ny = 100, 100
record_length = 1 + nx * ny + nx * ny  # Each record: time (1) + a field (nx*ny) + b field (nx*ny)

# Directories for input data and output GIFs
input_dir = "/home/riddhiman/computational_physics/assignment_5/"
output_dir = "/home/riddhiman/computational_physics/assignment_5/images_assignment5/"
os.makedirs(output_dir, exist_ok=True)

def extract_sourceturing_params(filename):
    """
    Extract parameters from a filename with the expected format:
    SourceTuring_<d_a>_<d_b>_<alpha>_<beta>.txt

    This extraction method follows the same procedure as in the very first code.
    
    Parameters:
        filename (str): The filename (or basename) to extract parameters from.
    
    Returns:
        tuple: A tuple (d_a, d_b, alpha, beta) as strings.
        
    Raises:
        ValueError: If the filename does not match the expected format.
    """
    base = os.path.basename(filename)
    # Check that the filename starts with "SourceTuring_" and ends with ".txt"
    if not (base.startswith("SourceTuring_") and base.endswith(".txt")):
        raise ValueError(f"Filename {filename} does not match the expected format.")
    
    # Remove the prefix and extension.
    base_no_ext = base.replace("SourceTuring_", "").replace(".txt", "")
    parts = base_no_ext.split("_")
    if len(parts) != 4:
        raise ValueError(f"Skipping file {filename} - unexpected filename format (found {len(parts)} parts).")
    return parts  # returns (d_a, d_b, alpha, beta) as strings

# Process each file in the input directory that matches the expected filename format.
for filename in os.listdir(input_dir):
    try:
        d_a, d_b, alpha, beta = extract_sourceturing_params(filename)
    except ValueError:
        continue  # Skip files that do not match the expected pattern.

    input_filepath = os.path.join(input_dir, filename)
    output_filepath = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.gif")

    # Read and flatten data from the text file.
    data = np.loadtxt(input_filepath).flatten()

    # Determine the number of records available.
    nrec = len(data) // record_length
    if len(data) % record_length != 0:
        raise ValueError(f"Data size in {filename} is not a multiple of the expected record length.")

    # Preallocate arrays for time and fields a and b.
    times = np.empty(nrec)
    a_records = np.empty((nrec, nx, ny))
    b_records = np.empty((nrec, nx, ny))

    # Parse the flat data array into separate records.
    for k in range(nrec):
        start = k * record_length
        rec = data[start:start + record_length]
        times[k] = rec[0]
        a_flat = rec[1:1 + nx * ny]
        b_flat = rec[1 + nx * ny:]
        a_records[k, :, :] = a_flat.reshape((nx, ny))
        b_records[k, :, :] = b_flat.reshape((nx, ny))

    # Set up the figure with two side-by-side subplots for the fields.
    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Create the initial plots using imshow.
    im_a = ax_a.imshow(a_records[0], cmap='viridis', origin='lower')
    ax_a.set_title("Field a")
    fig.colorbar(im_a, ax=ax_a)
    
    im_b = ax_b.imshow(b_records[0], cmap='inferno', origin='lower')
    ax_b.set_title("Field b")
    fig.colorbar(im_b, ax=ax_b)

    # Updated time_text with doubled curly braces for literal LaTeX commands.
    time_text = fig.suptitle(r"$\mathrm{{Time}} = {:.3f}, \, d_a = {}, \, d_b = {}, \, \alpha = {}, \, \beta = {}$"
                              .format(times[0], d_a, d_b, alpha, beta))

    # Define the update function for the animation.
    def update(frame):
        im_a.set_data(a_records[frame])
        im_b.set_data(b_records[frame])
        time_text.set_text(r"$\mathrm{{Time}} = {:.3f}, \, d_a = {}, \, d_b = {}, \, \alpha = {}, \, \beta = {}$"
                           .format(times[frame], d_a, d_b, alpha, beta))
        return im_a, im_b, time_text

    # Create and save the animation as a GIF.
    ani = animation.FuncAnimation(fig, update, frames=nrec, interval=1000 / 15, blit=False)
    ani.save(output_filepath, writer='pillow', fps=15)

    plt.tight_layout()
    plt.close(fig)  # Close the figure to free memory.
    print(f"Generated GIF: {output_filepath}")
