import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

integral_vals = np.loadtxt("/home/riddhiman/computational_physics/assignment_2/importance_sampling_integral.txt", usecols=0)

integral_vals = np.array(integral_vals)
bin_size = 0.01
bins = np.arange(min(integral_vals), max(integral_vals) + bin_size, bin_size)

hist, bin_edges = np.histogram(integral_vals, bins=bins, density=True)

bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

plt.figure(figsize=(10, 6))
plt.scatter(bin_centers, hist, color='g', label='Integral Values', s=10, alpha=0.6)
mu, std = norm.fit(integral_vals)

xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'k', linewidth=2, label=f"Fit: $\\mu={mu:.2f}$, $\\sigma={std:.2f}$")

plt.title("Distribution of Integral Values by Importance Sampling")
plt.xlabel("Integral Value")
plt.ylabel("Density")
#plt.xlim(0,15)
plt.legend()
plt.tight_layout()

plt.savefig('/home/riddhiman/computational_physics/assignment_2/images_assignment2/importance_sampling_value.png')
plt.show()