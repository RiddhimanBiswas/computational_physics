import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

# Parameters
dr = 0.1      # bin width
n_bins = 100   # must match Fortran value
n_particles = 1200  # Number of particles
filename = '/home/riddhiman/computational_physics/assignment_6/gr_debug.txt'

# Load the file
data = np.loadtxt(filename)

# Separate iteration numbers and g(r) values
iters = data[:, 0].astype(int)  # First column is iteration
gr_all = data[:, 1:]            # Remaining columns are g(r) bins

# r values for plotting
n_bins = int(0.5 * 20.0 / dr)
r_vals = dr * (np.arange(n_bins) + 0.5)

# --- PLOT ---
plt.figure(figsize=(8, 5))

# Compute the average g(r) over all iterations
gr_avg = np.mean(gr_all, axis=0)

# Plot the averaged g(r) vs r
plt.plot(r_vals, gr_avg, label='Averaged g(r)', color='red')
peaks, _ = find_peaks(gr_avg)
for i, peak in enumerate(peaks):
    plt.axvline(x=r_vals[peak], color='blue', linestyle='--', alpha=0.7, label='Local maximum' if i == 0 else '')
    plt.legend(loc='upper right')
    plt.text(0.98, 0.88, "Peaks occur at r values:\n" + "\n".join([f"r{i+1}: {r_vals[peak]:.2f}" for i, peak in enumerate(peaks)]),
             transform=plt.gca().transAxes,
             ha='right', va='top',
             bbox=dict(facecolor='white', alpha=0.5))

plt.xlabel("r")
plt.ylabel("g(r)")
plt.title("Pair Correlation Function $g(r)$ vs $r$")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
