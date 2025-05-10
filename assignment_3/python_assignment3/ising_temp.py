import numpy as np
import matplotlib.pyplot as plt
import glob
import re
import os

# User-defined parameters
data_dir = "/home/riddhiman/computational_physics/assignment_3/q2"
save_dir = "/home/riddhiman/computational_physics/assignment_3/images_assignment3/part2_final_individual"
os.makedirs(save_dir, exist_ok=True)

# Get all relevant files (corrected glob pattern)
file_list = sorted(glob.glob(f"{data_dir}/ising3d_L*_n1000000_J*.txt"))

# Extract unique (L, J) pairs
unique_pairs = set()
for file in file_list:
    match = re.search(r'ising3d_L(\d+)_n1000000_J([\d.]+)\.txt', file)
    if match:
        L, J = match.groups()
        unique_pairs.add((L, J))

# Process each unique (L, J) pair
for L, J in unique_pairs:
    # Filter files for the current (L, J) pair
    filtered_files = [file for file in file_list if re.search(rf'ising3d_L{L}_n1000000_J{J}\.txt', file)]
    
    # Initialize lists to store combined data
    T_list, ML_per_N_list, E_per_N_list, Cv_list, chi_list = [], [], [], [], []
    magnetic_sq_avg_list, magnetic_qd_avg_list = [], []
    
    for file in filtered_files:
        try:
            # Load data (columns: T, M_L/N, E/N, Cv, chi, M_sq_avg, M_qd_avg)
            data = np.loadtxt(file)
            if data.ndim == 1:  # If only one line exists, reshape to match expected format
                data = data.reshape(1, -1)
                
            T, ML_per_N, E_per_N, Cv, chi, magnetic_sq_avg, magnetic_qd_avg = data.T
            
            # Append data to lists
            T_list.append(T)
            ML_per_N_list.append(ML_per_N)
            E_per_N_list.append(E_per_N)
            Cv_list.append(Cv)
            chi_list.append(chi)
            magnetic_sq_avg_list.append(magnetic_sq_avg)
            magnetic_qd_avg_list.append(magnetic_qd_avg)
        except Exception as e:
            print(f"Error loading {file}: {e}")

    # Check if any data was loaded
    if not T_list:
        print(f"No valid data found for L={L}, J={J}. Skipping...")
        continue

    # Convert lists to numpy arrays
    T = np.concatenate(T_list)
    ML_per_N = np.concatenate(ML_per_N_list)
    E_per_N = np.concatenate(E_per_N_list)
    Cv = np.concatenate(Cv_list)
    chi = np.concatenate(chi_list)
    magnetic_sq_avg = np.concatenate(magnetic_sq_avg_list)
    magnetic_qd_avg = np.concatenate(magnetic_qd_avg_list)

    # Sort data by Temperature (T) in case files are not ordered
    sorted_indices = np.argsort(T)
    T = T[sorted_indices]
    ML_per_N = ML_per_N[sorted_indices]
    E_per_N = E_per_N[sorted_indices]
    Cv = Cv[sorted_indices]
    chi = chi[sorted_indices]
    magnetic_sq_avg = magnetic_sq_avg[sorted_indices]
    magnetic_qd_avg = magnetic_qd_avg[sorted_indices]

    # List of (data, ylabel, color, filename prefix) tuples
    plots = [
        (chi, r"Magnetic Susceptibility $\chi$", 'blue', "chi"),
        (Cv, "Specific Heat $C_v$", 'red', "cv"),
        (ML_per_N, "Magnetization per spin $M_L/N$", 'green', "magnetization"),
        (E_per_N, "Energy per spin $E/N$", 'purple', "energy")
    ]
    
    for y_data, ylabel, color, fname in plots:
        plt.figure(figsize=(8, 6))
        plt.plot(T, y_data, 'o-', color=color)
        plt.xlabel("Temperature (T)")
        plt.ylabel(ylabel)
        plt.title(f"{ylabel} vs Temperature (L={L}, J={J})")
        plt.grid(True)

        # Save before showing
        save_path = f"{save_dir}/{fname}_L{L}_n1000000_J{J}.png"
        plt.savefig(save_path, dpi=300)
        plt.show()
        plt.close()
