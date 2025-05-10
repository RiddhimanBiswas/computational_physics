import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Load the data from the file
n, error = np.loadtxt("/home/riddhiman/computational_physics/assignment_2/error_vs_n.txt", unpack=True)

# Perform a log-log plot
plt.figure(figsize=(8, 6))
plt.loglog(n, error, 'bo', label="Data")

# Fit a straight line to the log-log data
log_n = np.log(n)
log_error = np.log(error)
slope, intercept, r_value, p_value, std_err = linregress(log_n, log_error)

# Plot the fitted line
plt.loglog(n, np.exp(intercept) * n**slope, 'r-', label=f"Fit: slope = {slope:.2f}")

# Add labels and title
plt.xlabel('n (number of bins)')
plt.ylabel('Error')
plt.title('Log-Log Plot of Error vs n')

# Show the plot with a legend
plt.legend()
plt.grid(True)
plt.savefig('/home/riddhiman/computational_physics/assignment_2/images_assignment2/error_vs_n_loglog.png')

# Print the slope
print(f"Slope of the log-log plot: {slope:.2f}")