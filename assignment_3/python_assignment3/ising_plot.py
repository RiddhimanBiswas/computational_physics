import numpy as np
import matplotlib.pyplot as plt
import glob
import re
import os

# User-defined parameters
data_dir = "/home/riddhiman/computational_physics/assignment_3/"
save_dir = "/home/riddhiman/computational_physics/assignment_3/images_assignment3/"
os.makedirs(save_dir, exist_ok=True)

# Set niter value directly
niter = "50000"

# Find all relevant files (for ising.f90, which have T in filename)
file_list = sorted(glob.glob(f"{data_dir}ising3d_L*_n{niter}_T*_J*.txt"))

# Organize files by (L, J) pair
file_dict = {}
for file in file_list:
    match = re.search(r'ising3d_L(\d+)_n(\d+)_T([\d.]+)_J(-?[\d.]+).txt', file)
    if match:
        L, _, T, J = match.groups()
        key = (L, J)
        if key not in file_dict:
            file_dict[key] = []
        file_dict[key].append((float(T), file))

# Process each (L, J) pair
for (L, J), files in file_dict.items():
    # Sort files by temperature value
    files.sort(key=lambda x: x[0])
    if len(files) < 4:
        print(f"Skipping L={L}, J={J} (less than 4 T values found)")
        continue

    # --- Magnetization Plot ---
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    fig.suptitle(f"L={L}, J={J}, niter={niter}", fontsize=14)
    for i, (T, file) in enumerate(files[:4]):  # Take first 4 T values
        data = np.loadtxt(file, skiprows=1)
        iterations, magnetization, energy = data.T
        avg_magnetization = np.mean(magnetization)
        ax = axes[i // 2, i % 2]
        ax.plot(iterations, magnetization, label=f"T={T}, Avg M={avg_magnetization:.2f}", color='blue')
        ax.set_xlabel("Iterations")
        ax.set_ylabel("Magnetization")
        ax.legend()
        ax.grid(True)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    # Save before showing to avoid empty figures
    save_path = f"{save_dir}magnetization_L{L}_n{niter}_T_J{J}.png"
    plt.savefig(save_path, dpi=300)
    plt.show()
    plt.close()

    # --- Energy Plot ---
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    fig.suptitle(f"Energy Evolution: L={L}, J={J}, niter={niter}", fontsize=14)
    for i, (T, file) in enumerate(files[:4]):
        data = np.loadtxt(file, skiprows=1)
        iterations, magnetization, energy = data.T
        avg_energy = np.mean(energy)
        ax = axes[i // 2, i % 2]
        ax.plot(iterations, energy, label=f"T={T}, Avg E={avg_energy:.2f}", color='red')
        ax.set_xlabel("Iterations")
        ax.set_ylabel("Energy")
        ax.legend()
        ax.grid(True)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    save_path = f"{save_dir}energy_L{L}_n{niter}_T_J{J}.png"
    plt.savefig(save_path, dpi=300)
    plt.show()
    plt.close()
