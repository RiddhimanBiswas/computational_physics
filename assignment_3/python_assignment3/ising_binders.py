import numpy as np
import matplotlib.pyplot as plt
import glob
import re
import os
from scipy.optimize import curve_fit

# User-defined parameters
data_dir = "/home/riddhiman/computational_physics/assignment_3/q2"
save_dir = "/home/riddhiman/computational_physics/assignment_3/images_assignment3/part2_final"
os.makedirs(save_dir, exist_ok=True)

# Get all relevant files
file_list = sorted(glob.glob(f"{data_dir}/ising3d_L*_n1000000_J1.00.txt"))

# Extract unique L values
unique_L = sorted(set(int(re.search(r'ising3d_L(\d+)_n1000000_J1.00.txt', f).group(1)) for f in file_list))

# Data storage
binder_data = {}
observables = {L: {} for L in unique_L}

# Process each L
for L in unique_L:
    files = [f for f in file_list if re.search(rf'ising3d_L{L}_n1000000_J1.00.txt', f)]
    
    T_list, chi_list, Cv_list, ML_per_N_list, E_per_N_list = [], [], [], [], []
    M_sq_list, M_qd_list = [], []
    
    for file in files:
        try:
            data = np.loadtxt(file)
            if data.ndim == 1:
                data = data.reshape(1, -1)
            
            T, ML_per_N, E_per_N, Cv, chi, M_sq, M_qd = data.T
            
            T_list.append(T)
            chi_list.append(chi)
            Cv_list.append(Cv)
            ML_per_N_list.append(ML_per_N)
            E_per_N_list.append(E_per_N)
            M_sq_list.append(M_sq)
            M_qd_list.append(M_qd)
        except Exception as e:
            print(f"Error loading {file}: {e}")
    
    if not T_list:
        print(f"No valid data for L={L}. Skipping...")
        continue
    
    # Concatenate and sort by T
    T = np.concatenate(T_list)
    sorted_idx = np.argsort(T)
    T = T[sorted_idx]
    
    chi = np.concatenate(chi_list)[sorted_idx]
    Cv = np.concatenate(Cv_list)[sorted_idx]
    ML_per_N = np.concatenate(ML_per_N_list)[sorted_idx]
    E_per_N = np.concatenate(E_per_N_list)[sorted_idx]
    M_sq = np.concatenate(M_sq_list)[sorted_idx]
    M_qd = np.concatenate(M_qd_list)[sorted_idx]
    
    # Compute Binder cumulant
    U = 1 - (M_qd / (3 * M_sq ** 2))
    binder_data[L] = (T, U)
    
    # Store observables
    observables[L]['T'] = T
    observables[L]['chi'] = chi
    observables[L]['Cv'] = Cv
    observables[L]['ML_per_N'] = ML_per_N
    observables[L]['E_per_N'] = E_per_N

# Estimate critical temperature T_c
Tc_values = [T[np.argmin(np.abs(U - 0.5))] for L, (T, U) in binder_data.items()]
Tc = np.mean(Tc_values)

# Plot Binder Cumulant
plt.figure(figsize=(8, 6))
for L in unique_L:
    T, U = binder_data[L]
    plt.plot(T, U, 'o-', label=f'L={L}')
plt.axvline(Tc, color='black', linestyle='--', label=f'T_c ≈ {Tc:.2f}')
plt.xlabel("Temperature (T)")
plt.ylabel(r"Binder Cumulant $U$")
plt.title(r"Binder Cumulant $U$ vs Temperature $T$ (J=1.00)")
plt.legend()
plt.grid(True)
plt.savefig(f"{save_dir}/binder_cumulant.png", dpi=300)
plt.show()

# Define LaTeX labels for each observable
label_map = {
    'chi': (r'$\chi$', r'$\chi$'),
    'Cv': (r'$C_v$', r'$C_v$'),
    'ML_per_N': (r'$\frac{M_L}{N}$', r'$\frac{M_L}{N}$'),
    'E_per_N': (r'$\frac{E}{N}$', r'$\frac{E}{N}$'),
}

# Plot all observables
for observable in ['chi', 'Cv', 'ML_per_N', 'E_per_N']:
    plt.figure(figsize=(8, 6))
    max_points = []
    
    for L in unique_L:
        T, y_data = observables[L]['T'], observables[L][observable]
        plt.plot(T, y_data, 'o-', label=f'L={L}')
        
        if observable in ['chi', 'Cv']:
            max_T = T[np.argmax(y_data)]
            max_points.append(max_T)
    
    plt.axvline(Tc, color='black', linestyle='--', label=f'T_c ≈ {Tc:.2f}')
    
    if observable in ['chi', 'Cv'] and max_points:
        best_fit_T = np.mean(max_points)
        plt.axvline(best_fit_T, color='gray', linestyle=':', label=f'Max Fit ≈ {best_fit_T:.2f}')
    
    # Get LaTeX labels from the mapping
    ylabel, title_part = label_map[observable]
    plt.xlabel("Temperature (T)")
    plt.ylabel(ylabel)
    plt.title(f"{title_part} vs Temperature $T$ (J=1.00)")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{save_dir}/{observable}.png", dpi=300)
    plt.show()