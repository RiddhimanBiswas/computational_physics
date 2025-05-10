import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Define Gaussian function for fitting
def gaussian(x, A, mu, sigma):
    return A * np.exp(-0.5 * ((x - mu) / sigma) ** 2)

# Load data from the file
data = np.loadtxt('/home/riddhiman/computational_physics/assignment_1/random_walk_10^5_10^5_data.txt')

# Extract columns
x = data[:, 0]  # First column: Sum
count = data[:, 1]  # Second column: Count
norm_dist = data[:, 2]  # Third column: Normalized Distribution

# ===== Plot 1: Count vs Sum =====
# Fit Gaussian curve with constraints: sigma >= 0
popt_count, _ = curve_fit(
    gaussian, x, count, 
    p0=[max(count), np.mean(x), np.std(x)], 
    bounds=([0, -np.inf, 0], [np.inf, np.inf, np.inf])
)
A_count, mu_count, sigma_count = popt_count

# Create the plot
plt.figure(figsize=(8, 6))
plt.scatter(x, count, color='blue', label='Data', s=10)
plt.plot(x, gaussian(x, *popt_count), 'r-', label='Gaussian Fit')

# Add fitted parameters as annotations in the graph
annotation_text_count = (
    f"Amplitude (A): {A_count:.2f}\n"
    f"Mean (Mu): {mu_count:.2f}\n"
    f"Std Dev (Sigma): {sigma_count:.2f}"
)
plt.text(0.05, 0.95, annotation_text_count, transform=plt.gca().transAxes, 
         fontsize=10, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.8))

# Add labels, title, and legend
plt.title('10^5 random walk, 10^5 steps, bin size = 1')  # Customize title
plt.xlabel('Sum')
plt.ylabel('Count')
plt.legend()
plt.grid(True)
plt.xlim(-1000, 1000)  # Set x-axis limits
plt.savefig("q1l_a.png")
plt.show()

# ===== Plot 2: Normalized Distribution vs Sum =====
# Fit Gaussian curve with constraints: sigma >= 0
popt_norm, _ = curve_fit(
    gaussian, x, norm_dist, 
    p0=[max(norm_dist), np.mean(x), np.std(x)], 
    bounds=([0, -np.inf, 0], [np.inf, np.inf, np.inf])
)
A_norm, mu_norm, sigma_norm = popt_norm

# Create the plot
plt.figure(figsize=(8, 6))
plt.scatter(x, norm_dist, color='green', label='Data', s=10)
plt.plot(x, gaussian(x, *popt_norm), 'orange', label='Gaussian Fit')

# Add fitted parameters as annotations in the graph
annotation_text_norm = (
    f"Amplitude (A): {A_norm:.2e}\n"
    f"Mean (Mu): {mu_norm:.2f}\n"
    f"Std Dev (Sigma): {sigma_norm:.2f}"
)
plt.text(0.05, 0.95, annotation_text_norm, transform=plt.gca().transAxes, 
         fontsize=10, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.8))

# Add labels, title, and legend
plt.title('10^5 random walk, 10^5 steps, bin size = 1')  # Customize title
plt.xlabel('Sum')
plt.ylabel('Normalized Distribution')
plt.legend()
plt.grid(True)
plt.xlim(-1000, 1000)  # Set x-axis limits
plt.savefig("q1l_b.png")
plt.show()