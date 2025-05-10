import numpy as np
import matplotlib.pyplot as plt

# Load the data from the text file
data = np.loadtxt('/home/riddhiman/computational_physics/assignment_2/correlation.txt')

# Separate the columns into x and y
x = data[:, 0]  # First column
y = data[:, 1]  # Second column

# Plot the data
plt.plot(x, y, marker='o', linestyle='-', color='b')
plt.xlabel('Step size')
plt.ylabel('Correlation values')
plt.title('Plot of Correlation vs. Step, Uniform random numbers')
plt.ylim(-1, 1)
plt.grid(True)
plt.savefig('/home/riddhiman/computational_physics/assignment_2/images_assignment2/correlation.png')
plt.show()
