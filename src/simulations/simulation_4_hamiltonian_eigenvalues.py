import numpy as np
import scipy.linalg as linalg
import matplotlib.pyplot as plt

print("=== Simulation 4: Hamiltonian Eigenvalue Analysis ===")

# --- 1. Setup the Discretized Space ---
N_GRID = 5000 # Higher resolution grid
Y_MIN, Y_MAX = 0, 9.0 # Go out further to capture more primes (up to e^9 ~ 8100)
dy = (Y_MAX - Y_MIN) / N_GRID
y_grid = np.linspace(Y_MIN, Y_MAX, N_GRID)

print(f"Grid parameters:")
print(f" Grid points: {N_GRID}")
print(f" Y range: [{Y_MIN}, {Y_MAX}]")
print(f" Grid spacing: {dy:.6f}")
print(f" Max prime captured: ~{int(np.exp(Y_MAX))}")

# --- 2. Construct the Prime Potential (V) ---
def get_prime_partitions(limit):
 """Generates primes and partitions them into functional classes."""
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
 class_4n1 = [p for p in primes if p % 4 == 1]
 class_4n3 = [p for p in primes if p % 4 == 3]
 class_S = [2]
 return class_4n1, class_4n3, class_S

primes_4n1, primes_4n3, primes_S = get_prime_partitions(limit=int(np.exp(Y_MAX)))

print(f"Prime statistics:")
print(f" 4n+1 primes: {len(primes_4n1)}")
print(f" 4n+3 primes: {len(primes_4n3)}")
print(f" Anchor primes: {len(primes_S)}")
print(f" Total primes: {len(primes_4n1) + len(primes_4n3) + len(primes_S)}")

V_potential = np.zeros(N_GRID)
# The coupling constant needs to be tuned to match the kinetic energy scale.
# This is a key parameter of the model that sets the "strength" of the prime identities.
COUPLING_CONSTANT = 2 * 10**5 

def place_potential_on_grid(p_list, sign):
 """Places weighted prime potentials onto the discrete grid."""
 placed_count = 0
 for p in p_list:
 log_p = np.log(p)
 if Y_MIN < log_p < Y_MAX:
 idx = int((log_p - Y_MIN) / dy)
 V_potential[idx] += sign * (p**(-0.5)) * COUPLING_CONSTANT
 placed_count += 1
 return placed_count

placed_4n1 = place_potential_on_grid(primes_4n1, 1.0)
placed_4n3 = place_potential_on_grid(primes_4n3, -1.0)
placed_S = place_potential_on_grid(primes_S, 1.0)

print(f"Primes placed on grid:")
print(f" 4n+1 primes placed: {placed_4n1}")
print(f" 4n+3 primes placed: {placed_4n3}")
print(f" Anchor primes placed: {placed_S}")

V_matrix = np.diag(V_potential)

# --- 3. Construct the Kinetic Energy Operator (T) ---
# We use the Schrodinger form T = -1/2 * d^2/dy^2
T_matrix = np.zeros((N_GRID, N_GRID))
T_matrix += np.diag(-2 * np.ones(N_GRID))
T_matrix += np.diag(np.ones(N_GRID - 1), k=1)
T_matrix += np.diag(np.ones(N_GRID - 1), k=-1)
T_matrix *= -1.0 / (2.0 * dy**2)

# --- 4. Form the Hamiltonian and Solve for Eigenvalues ---
print("Constructing Hamiltonian matrix...")
H_matrix = T_matrix + V_matrix
# We only need the lowest eigenvalues as they correspond to the first zeros
num_eigenvalues = 15
print(f"Computing {num_eigenvalues} lowest eigenvalues...")
eigenvalues = linalg.eigvalsh(H_matrix, subset_by_index=[0, num_eigenvalues-1])

# The eigenvalues E_n of this operator should approximate t_n^2
computed_zeros_approx = np.sqrt(eigenvalues[eigenvalues > 0])

# --- 5. Compare with Known Riemann Zeros ---
known_zeros = [
 14.134725, 21.022040, 25.010858, 30.424876, 32.935062, 
 37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
 52.910381, 56.446248, 59.347044, 60.831779, 65.112544
]

# --- 6. Plotting the Comparison ---
plt.figure(figsize=(14, 10))
plt.eventplot(known_zeros, orientation='horizontal', colors='r', linelengths=0.8, 
 lineoffsets=1, label=f'First {len(known_zeros)} Known Riemann Zeros')
plt.eventplot(computed_zeros_approx, orientation='horizontal', colors='b', linelengths=0.8, 
 lineoffsets=2, label=f'First {len(computed_zeros_approx)} Computed Zeros from Model')

plt.title('Spectral Test of the Λ-Core Prime Hamiltonian', fontsize=16)
plt.yticks([1, 2], ['Known Zeros (from literature)', 'Eigenvalues of Model'])
plt.xlabel('Height on the Critical Line (t)', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, axis='x', linestyle=':', alpha=0.7)
plt.ylim(0.5, 2.5)
plt.xlim(0, 70)
plt.tight_layout()
plt.savefig('riemann_zeros_comparison.png', dpi=300, bbox_inches='tight')
plt.show()

# --- 7. Print Table of Results ---
print("\nTable 1: Comparison of Computed Spectrum vs. Known Riemann Zeros")
print("="*75)
print(f"{'n':<5}{'Known Zero (t_n)':<20}{'Computed Zero':<20}{'Relative Error (%)':<20}")
print("-"*75)
for i in range(min(len(computed_zeros_approx), len(known_zeros))):
 if i < len(computed_zeros_approx):
 error = 100 * abs(computed_zeros_approx[i] - known_zeros[i]) / known_zeros[i]
 print(f"{i+1:<5}{known_zeros[i]:<20.6f}{computed_zeros_approx[i]:<20.6f}{error:<20.2f}")
 else:
 print(f"{i+1:<5}{known_zeros[i]:<20.6f}{'N/A':<20}{'N/A':<20}")
print("="*75)

# Calculate statistics
if len(computed_zeros_approx) > 0:
 errors = [100 * abs(computed_zeros_approx[i] - known_zeros[i]) / known_zeros[i] 
 for i in range(min(len(computed_zeros_approx), len(known_zeros)))]
 print(f"\nStatistical Summary:")
 print(f" Mean relative error: {np.mean(errors):.2f}%")
 print(f" Std deviation of error: {np.std(errors):.2f}%")
 print(f" Max relative error: {np.max(errors):.2f}%")
 print(f" Min relative error: {np.min(errors):.2f}%")

print("="*50) 