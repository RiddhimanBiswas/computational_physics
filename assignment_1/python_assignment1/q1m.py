import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def gaussian(x, A, mu, sigma):
    return A * np.exp(-0.5 * ((x - mu) / sigma) ** 2)

# Change the path to the location of the file accordingly
data = np.loadtxt('/home/riddhiman/computational_physics/assignment_1/random_walk_10^5_data.txt')

x_data = data[:, 0]  
y_data = data[:, 2]  

# Fit the Gaussian curve
popt, pcov = curve_fit(gaussian, x_data, y_data, p0=[1, 0, 1])

A, mu, sigma = popt

# Plot the data and the fitted Gaussian curve
plt.figure(figsize=(8, 6))
plt.scatter(x_data, y_data, color='black', label='Data', s=10)
plt.plot(x_data, gaussian(x_data, *popt), 'r-', label='Gaussian Fit')

# Add fitted parameters as annotations in the graph
annotation_text = (
    f"Amplitude (A): {A:.3f}\n"
    f"Mean (Mu): {mu:.3f}\n"
    f"Std Dev (Sigma): {sigma:.3f}"
)
plt.text(0.05, 0.95, annotation_text, transform=plt.gca().transAxes, 
         fontsize=10, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.8))

# Add labels, title, and legend
plt.title('Gaussian Fit to Random Walk Distribution')
plt.xlabel('Value')
plt.ylabel('Normalized Frequency')
plt.legend()
plt.grid(True)
plt.show()