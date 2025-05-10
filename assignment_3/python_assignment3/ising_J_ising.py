import numpy as np
import matplotlib.pyplot as plt
import glob
import re
import os
from mpl_toolkits.mplot3d import Axes3D  # For 3D plotting

# User-defined parameters
threshold_m = 0.01      # Magnetization fluctuation threshold
threshold_e = 0.01      # Energy fluctuation threshold
window = 1000           # Number of iterations to check stabilization
time_per_iteration = 1e-4  # Conversion factor (seconds per iteration)
niter = "50000"         # Fixed number of iterations

# Define data directory and ensure the images directory exists
data_dir = "/home/riddhiman/computational_physics/assignment_3/"
images_dir = "/home/riddhiman/computational_physics/assignment_3/images_assignment3/"
os.makedirs(images_dir, exist_ok=True)

# Find all relevant files for ising.f90 (files contain _T and _J)
file_list = sorted(glob.glob(f"{data_dir}ising3d_L*_n{niter}_T*_J*.txt"))

# Extract unique L and T values from the filenames
L_values = sorted(set(re.search(r'ising3d_L(\d+)_', f).group(1) for f in file_list))
T_values = sorted(set(re.search(r'_T([\d.]+)_', f).group(1) for f in file_list), key=float)

# Process each lattice size L
for L in L_values:
    # Lists for 3D plotting data: magnetization-based stabilization times
    J_all_m, T_all_m, stab_all_m = [], [], []
    # And lists for energy-based stabilization times
    J_all_e, T_all_e, stab_all_e = [], [], []
    
    # Loop over each temperature T for current L
    for T in T_values:
        # Filter files for current L and T (e.g., filenames containing "L{L}" and "_T{T}_")
        files = [f for f in file_list if f"L{L}" in f and f"_T{T}_" in f]
        if not files:
            continue
        
        # Process each file corresponding to the given L and T
        for file in files:
            J_match = re.search(r'_J(-?[\d.]+).txt', file)
            if not J_match:
                continue
            J_val = float(J_match.group(1))
            data = np.loadtxt(file, skiprows=1)
            iterations, magnetization, energy = data.T
            
            # Determine stabilization time for magnetization
            n_stable_m = iterations[-1]  # Default to the last iteration
            for i in range(len(iterations) - window):
                if np.max(magnetization[i:i+window]) - np.min(magnetization[i:i+window]) < threshold_m:
                    n_stable_m = iterations[i]
                    break
            stab_time_m = n_stable_m * time_per_iteration
            J_all_m.append(J_val)
            T_all_m.append(float(T))
            stab_all_m.append(stab_time_m)
            
            # Determine stabilization time for energy
            n_stable_e = iterations[-1]
            for i in range(len(iterations) - window):
                if np.max(energy[i:i+window]) - np.min(energy[i:i+window]) < threshold_e:
                    n_stable_e = iterations[i]
                    break
            stab_time_e = n_stable_e * time_per_iteration
            J_all_e.append(J_val)
            T_all_e.append(float(T))
            stab_all_e.append(stab_time_e)
    
    # --- Create a 3D scatter plot for Magnetization-based Stabilization Times ---
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    sc1 = ax.scatter(J_all_m, T_all_m, stab_all_m, c=stab_all_m, cmap='viridis', marker='o')
    ax.set_xlabel(r"$J_{ising}$")
    ax.set_ylabel("Temperature (T)")
    ax.set_zlabel("Stabilization Time (s)")
    ax.set_title(f"Magnetization-based Stabilization Times for L={L}, niter=50000")
    fig.colorbar(sc1, ax=ax, label="Stabilization Time (s)")
    save_path = f"{images_dir}stabilization_m_L{L}_n50000_3D.png"
    plt.savefig(save_path, dpi=300)
    plt.show()
    plt.close()
    
    # --- Create a 3D scatter plot for Energy-based Stabilization Times ---
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    sc2 = ax.scatter(J_all_e, T_all_e, stab_all_e, c=stab_all_e, cmap='plasma', marker='^')
    ax.set_xlabel(r"$J_{ising}$")
    ax.set_ylabel("Temperature (T)")
    ax.set_zlabel("Stabilization Time (s)")
    ax.set_title(f"Energy-based Stabilization Times for L={L}, niter=50000")
    fig.colorbar(sc2, ax=ax, label="Stabilization Time (s)")
    save_path = f"{images_dir}stabilization_e_L{L}_n50000_3D.png"
    plt.savefig(save_path, dpi=300)
    plt.show()
    plt.close()
