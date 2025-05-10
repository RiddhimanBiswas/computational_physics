import numpy as np
import matplotlib.pyplot as plt

# File name of the output from the Fortran code
filename = '/home/riddhiman/computational_physics/assignment_4/jacobi.txt'

# Read the file
with open(filename, 'r') as file:
    lines = file.readlines()

# The first line contains the x values
x = np.array([float(val) for val in lines[0].split()])

# The rest of the lines are y values from each iteration (starting with the first iteration on line 2)
y_solutions = []
for line in lines[1:]:
    y_solutions.append(np.array([float(val) for val in line.split()]))

# Determine which iterations to plot:
# Include the first iteration (index 0), every 500th iteration, and also the final iteration.
num_iterations = len(y_solutions)
plot_indices = [0]  # Always include the first iteration (line 2)
# Add every 500th iteration (adjusting for 0-based index: the 500th iteration is index 499)
plot_indices.extend(range(499, num_iterations, 500))
# Ensure the final iteration is included
if (num_iterations - 1) not in plot_indices:
    plot_indices.append(num_iterations - 1)
# Sort indices to ensure correct order
plot_indices = sorted(set(plot_indices))

# Create the plot
plt.figure(figsize=(8, 6))
for idx in plot_indices:
    label = f"Iteration {idx + 1}"  # +1 because our list is 0-indexed
    plt.plot(x, y_solutions[idx], label=label)

    # Define the actual solution as a function
    def actual_solution(x):
        term1 = (np.exp(-5 / 2) + np.cos(np.sqrt(15) / 2)) / (2 * np.sin(np.sqrt(15) / 2))
        term2 = np.exp(5 * x / 2) * np.sin(np.sqrt(15) / 2 * x)
        term3 = -0.5 * np.exp(5 * x / 2) * np.cos(np.sqrt(15) / 2 * x)
        return term1 * term2 + term3 + x + 0.5

    # Compute the actual solution for the x values
    y_actual = actual_solution(x)

    # Plot the actual solution in a completely different color, ensuring it's only added once
    if "Actual Solution" not in plt.gca().get_legend_handles_labels()[1]:
        plt.plot(x, y_actual, label="Actual Solution", color="black", linestyle="--", linewidth=2)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Convergence of Jacobi Iterations')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Find the value of y at x = 0.80 for the final iteration
x_target = 0.80
final_iteration = y_solutions[-1]

# Find the index of the closest x value to x_target
closest_index = np.argmin(np.abs(x - x_target))
y_at_target = final_iteration[closest_index]

print(f"The value of y at x={x_target} is {y_at_target}")