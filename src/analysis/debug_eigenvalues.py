import numpy as np
import scipy.linalg as linalg
import matplotlib.pyplot as plt

print("=== DEBUG: Eigenvalue Analysis ===")

# Simplified version for debugging
N_GRID = 1000  # Smaller grid for faster computation
Y_MIN, Y_MAX = 0, 6.0  # Smaller range
dy = (Y_MAX - Y_MIN) / N_GRID

print(f"Grid parameters:")
print(f"  Grid points: {N_GRID}")
print(f"  Y range: [{Y_MIN}, {Y_MAX}]")
print(f"  Grid spacing: {dy:.6f}")

# Generate primes
def get_primes(limit):
    primes = []
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(np.sqrt(limit)) + 1):
        if is_prime[p]:
            for i in range(p * p, limit + 1, p):
                is_prime[i] = False
    for p in range(2, limit + 1):
        if is_prime[p]:
            primes.append(p)
    return primes

primes = get_primes(int(np.exp(Y_MAX)))
primes_4n1 = [p for p in primes if p % 4 == 1]
primes_4n3 = [p for p in primes if p % 4 == 3]

print(f"Primes found: {len(primes)}")
print(f"4n+1 primes: {len(primes_4n1)}")
print(f"4n+3 primes: {len(primes_4n3)}")

# Build potential
V_potential = np.zeros(N_GRID)
COUPLING_CONSTANT = 1e3  # Smaller coupling for testing

placed_count = 0
for p in primes:
    log_p = np.log(p)
    if Y_MIN < log_p < Y_MAX:
        idx = int((log_p - Y_MIN) / dy)
        if p % 4 == 1:
            V_potential[idx] += (p**(-0.5)) * COUPLING_CONSTANT
        elif p % 4 == 3:
            V_potential[idx] -= (p**(-0.5)) * COUPLING_CONSTANT
        else:  # p == 2
            V_potential[idx] += (p**(-0.5)) * COUPLING_CONSTANT
        placed_count += 1

print(f"Primes placed on grid: {placed_count}")
print(f"Non-zero potential elements: {np.count_nonzero(V_potential)}")
print(f"Max potential: {np.max(V_potential):.6f}")
print(f"Min potential: {np.min(V_potential):.6f}")

# Build kinetic operator
T_matrix = np.zeros((N_GRID, N_GRID))
T_matrix += np.diag(-2 * np.ones(N_GRID))
T_matrix += np.diag(np.ones(N_GRID - 1), k=1)
T_matrix += np.diag(np.ones(N_GRID - 1), k=-1)
T_matrix *= -1.0 / (2.0 * dy**2)

print(f"Kinetic energy scale: {1.0 / (2.0 * dy**2):.2f}")

# Build Hamiltonian
V_matrix = np.diag(V_potential)
H_matrix = T_matrix + V_matrix

# Compute eigenvalues
print("Computing eigenvalues...")
eigenvalues = linalg.eigvalsh(H_matrix, subset_by_index=[0, 19])  # First 20

print(f"\nFirst 20 eigenvalues:")
for i, ev in enumerate(eigenvalues):
    print(f"  {i+1:2d}: {ev:12.6f}")

# Filter positive eigenvalues and take square root
positive_eigenvalues = eigenvalues[eigenvalues > 0]
computed_zeros = np.sqrt(positive_eigenvalues)

print(f"\nPositive eigenvalues: {len(positive_eigenvalues)}")
print(f"Computed zeros (sqrt of positive eigenvalues):")
for i, zero in enumerate(computed_zeros):
    print(f"  {i+1:2d}: {zero:12.6f}")

# Compare with known zeros
known_zeros = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062]
print(f"\nComparison with first 5 known zeros:")
print(f"{'Known':<12} {'Computed':<12} {'Error %':<10}")
print("-" * 40)
for i in range(min(len(known_zeros), len(computed_zeros))):
    if i < len(computed_zeros):
        error = 100 * abs(computed_zeros[i] - known_zeros[i]) / known_zeros[i]
        print(f"{known_zeros[i]:<12.6f} {computed_zeros[i]:<12.6f} {error:<10.2f}")
    else:
        print(f"{known_zeros[i]:<12.6f} {'N/A':<12} {'N/A':<10}")

print("="*50) 