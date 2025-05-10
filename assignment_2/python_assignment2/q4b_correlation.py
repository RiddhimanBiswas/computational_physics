import numpy as np
import matplotlib.pyplot as plt

# Load the data from the text file
data = np.loadtxt('/home/riddhiman/computational_physics/assignment_2/correlation_gaussian.txt')

# Separate the columns into x and y
x = data[:, 0]  # First column
y = data[:, 1]  # Second column

# Plot the data
plt.plot(x, y, marker='o', linestyle='-', color='b')
plt.xlabel('Step size')
plt.ylabel('Correlation values')
plt.title('Plot of Correlation vs. Step, Gaussian random numbers')
plt.ylim(-1, 1)
plt.grid(True)
plt.savefig('/home/riddhiman/computational_physics/assignment_2/images_assignment2/gaussian_correlation.png')
plt.show()
# The mean of the random numbers is   0.50110660308561639     
# The standard deviation of the random numbers is   0.28932260088298922 