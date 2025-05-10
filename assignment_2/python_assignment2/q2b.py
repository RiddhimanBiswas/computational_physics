import numpy as np
import matplotlib.pyplot as plt

# Read the random numbers from the file
random_numbers = np.loadtxt('/home/riddhiman/computational_physics/assignment_2/random_number.txt')

# Create a scatter plot to show that the numbers are uncorrelated
plt.figure(figsize=(10, 6))
plt.scatter(range(len(random_numbers)), random_numbers[:], label="Random Numbers", s=2, alpha=0.6)

# Add a title and labels
plt.title('Scatter Plot of Random Numbers, Uniform distribution')
plt.xlabel('Index')
plt.ylabel('Random Number')

# Show grid and plot
plt.grid(True)
plt.legend()
plt.savefig('/home/riddhiman/computational_physics/assignment_2/images_assignment2/uniform_random_scatter.png')
plt.show()