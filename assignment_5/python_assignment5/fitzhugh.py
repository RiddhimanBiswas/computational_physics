import numpy as np
import matplotlib.pyplot as plt

# Parameters
alpha_vals = [0.5, 1.0, 1.5]  # Different values of alpha
beta_vals = [0.8, 1.0, 1.2]   # Different values of beta

# Range for a and b
a_vals = np.linspace(-2, 2, 400)
a_grid, b_grid = np.meshgrid(np.linspace(-2, 2, 20), np.linspace(-2, 2, 20))

# Vector field equations
def da_dt(a, b, alpha):
    return b - a + a**3 - alpha

def db_dt(a, b, beta):
    return -b + beta * a

# Plotting
plt.figure(figsize=(10, 8))

# Loop over alpha and beta values
for alpha in alpha_vals:
    for beta in beta_vals:
        # Nullclines
        b_nullcline1 = a_vals - a_vals**3 + alpha  # da/dt = 0
        b_nullcline2 = a_vals                      # db/dt = 0

        # Plot nullclines
        plt.plot(a_vals, b_nullcline1, label=f"da/dt=0 (α={alpha})", linestyle='-', alpha=0.7)
        plt.plot(a_vals, b_nullcline2, label=f"db/dt=0 (β={beta})", linestyle='--', alpha=0.7)

# Compute vector field
u = da_dt(a_grid, b_grid, alpha=1.0)  # Example alpha
v = db_dt(a_grid, b_grid, beta=1.0)  # Example beta
norm = np.sqrt(u**2 + v**2)  # Normalize vectors
u, v = u / norm, v / norm

# Plot vector field
plt.quiver(a_grid, b_grid, u, v, color='gray', alpha=0.6)

# Final plot adjustments
plt.xlabel('a')
plt.ylabel('b')
plt.title('FitzHugh-Nagumo Nullclines and Vector Field')
plt.legend(loc='best', fontsize='small')
plt.grid(True)
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.xlim(-2, 2)
plt.ylim(-2, 2)
plt.show()
