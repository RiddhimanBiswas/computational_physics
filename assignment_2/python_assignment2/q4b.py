import numpy as np
import matplotlib.pyplot as plt

# Read the random numbers from the file
random_numbers = np.loadtxt('/home/riddhiman/computational_physics/assignment_2/gaussian_random.txt')

# Plot the histogram of the random numbers
plt.figure(figsize=(10, 6))
plt.hist(random_numbers, bins=100, density=True, alpha=0.6, color='b', edgecolor='black')

# Add a title and labels
plt.title('Probability Distribution of 10,000 Random Numbers, Gaussian distribution')
plt.xlabel('Random Number Value')
plt.ylabel('Probability Density')

# Show grid and plot
plt.grid(True)
plt.savefig('/home/riddhiman/computational_physics/assignment_2/images_assignment2/gaussian_random_histogram.png')
plt.show()