import numpy as np
import matplotlib.pyplot as plt
import glob
import re
import os

# User-defined parameters
data_dir = "/home/riddhiman/computational_physics/assignment_3/equil_study/"
save_dir = "/home/riddhiman/computational_physics/assignment_3/images_assignment3/part1_analysis/"
os.makedirs(save_dir, exist_ok=True)

# Set niter value directly
niter = "50000"

# Find all relevant files (for ising.f90, which have T in filename)
file_list = sorted(glob.glob(f"{data_dir}ising3d_L*_n{niter}_T*_J*.txt"))

# Organize files by (T, J) pair
file_dict = {}
for file in file_list:
    match = re.search(r'ising3d_L(\d+)_n(\d+)_T([\d.]+)_J(-?[\d.]+).txt', file)
    if match:
        L, _, T, J = match.groups()
        key = (float(T), float(J))
        if key not in file_dict:
            file_dict[key] = []
        file_dict[key].append((int(L), file))

# Process each temperature
temperatures = sorted(set(T for T, _ in file_dict.keys()))[:4]  # Select first 4 temperatures

# Plot average energy
fig_energy, axes_energy = plt.subplots(2, 2, figsize=(12, 8))
fig_energy.suptitle(f"Average Energy vs J, niter={niter}", fontsize=16)
fig_energy.subplots_adjust(hspace=0.5, wspace=0.5)

# Plot average magnetization
fig_magnetization, axes_magnetization = plt.subplots(2, 2, figsize=(12, 8))
fig_magnetization.suptitle(f"Average Magnetization vs J, niter={niter}", fontsize=16)
fig_magnetization.subplots_adjust(hspace=0.5, wspace=0.5)

line_styles = ['-', '--', '-.', ':']
markers = ['o', 's', 'D', '^']

for idx, T in enumerate(temperatures):
    ax_energy = axes_energy[idx // 2, idx % 2]
    ax_magnetization = axes_magnetization[idx // 2, idx % 2]
    ax_energy.set_title(f"Temperature T={T}")
    ax_magnetization.set_title(f"Temperature T={T}")
    
    # Prepare data for magnetization and energy plots
    magnetization_data = {}
    energy_data = {}
    
    for (temp, J), files in file_dict.items():
        if temp != T:
            continue
        for L, file in files:
            data = np.loadtxt(file, skiprows=1)
            _, magnetization, energy = data.T
            avg_magnetization = np.mean(magnetization)
            avg_energy = np.mean(energy)
            if L not in magnetization_data:
                magnetization_data[L] = []
            if L not in energy_data:
                energy_data[L] = []
            magnetization_data[L].append((J, avg_magnetization))
            energy_data[L].append((J, avg_energy))
    
    # Plot energy
    for i, (L, values) in enumerate(sorted(energy_data.items())):
        values.sort()
        J_values, avg_energies = zip(*values)
        ax_energy.plot(J_values, avg_energies, label=f"L={L}", linestyle=line_styles[i % len(line_styles)], marker=markers[i % len(markers)])
    ax_energy.set_xlabel("J")
    ax_energy.set_ylabel("Avg Energy")
    ax_energy.legend()
    ax_energy.grid(True)
    
    # Plot magnetization
    for i, (L, values) in enumerate(sorted(magnetization_data.items())):
        values.sort()
        J_values, avg_magnetizations = zip(*values)
        ax_magnetization.plot(J_values, avg_magnetizations, label=f"L={L}", linestyle=line_styles[i % len(line_styles)], marker=markers[i % len(markers)])
    ax_magnetization.set_xlabel("J")
    ax_magnetization.set_ylabel("Avg Magnetization")
    ax_magnetization.legend()
    ax_magnetization.grid(True)

plt.tight_layout(rect=[0, 0, 1, 0.96])
save_path_energy = f"{save_dir}avg_energy_vs_J_n{niter}.png"
save_path_magnetization = f"{save_dir}avg_magnetization_vs_J_n{niter}.png"
fig_energy.savefig(save_path_energy, dpi=300)
fig_magnetization.savefig(save_path_magnetization, dpi=300)
plt.show()
plt.close(fig_energy)
plt.close(fig_magnetization)
