import numpy as np
import matplotlib.pyplot as plt

# List of file paths and corresponding titles
file_paths = [
    '/home/riddhiman/computational_physics/assignment_2/test_correlation/correlation_extended2.txt',
    '/home/riddhiman/computational_physics/assignment_2/test_correlation/correlation_exponential_extended2.txt',
    '/home/riddhiman/computational_physics/assignment_2/test_correlation/correlation_gaussian_extended2.txt'
]

titles = [
    'Plot of Correlation vs. Step, 1000 Uniform random numbers, All steps',
    'Plot of Correlation vs. Step, 1000 Exponential random numbers, All steps',
    'Plot of Correlation vs. Step, 1000 Gaussian random numbers, All steps'
]

output_files = [
    '/home/riddhiman/computational_physics/assignment_2/images_assignment2/correlation_extended2.png',
    '/home/riddhiman/computational_physics/assignment_2/images_assignment2/correlation_exponential_extended2.png',
    '/home/riddhiman/computational_physics/assignment_2/images_assignment2/correlation_gaussian_extended2.png'
]

# Loop through each file, plot, and save the figure
for file_path, title, output_file in zip(file_paths, titles, output_files):
    # Load the data from the text file
    data = np.loadtxt(file_path)
    
    # Separate the columns into x and y
    x = data[:, 0]  # First column
    y = data[:, 1]  # Second column
    
    # Plot the data
    plt.figure()
    plt.plot(x, y, marker='o', linestyle='-', color='b')
    plt.xlabel('Step size')
    plt.ylabel('Correlation values')
    plt.title(title)
    plt.ylim(-1, 1)
    plt.grid(True)
    
    # Save the plot to a file
    plt.savefig(output_file)
    
    # Show the plot
    plt.show()