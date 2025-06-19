import numpy as np
import scipy.linalg as linalg
import matplotlib.pyplot as plt

print("=== Simulation 4 FIXED: Hamiltonian Eigenvalue Analysis ===")

# --- 1. Setup the Discretized Space ---
N_GRID = 2000  # Reasonable grid size for testing
Y_MIN, Y_MAX = 0, 7.0  # Capture primes up to e^7 ~ 1100
dy = (Y_MAX - Y_MIN) / N_GRID
y_grid = np.linspace(Y_MIN, Y_MAX, N_GRID)

print(f"Grid parameters:")
print(f"  Grid points: {N_GRID}")
print(f"  Y range: [{Y_MIN}, {Y_MAX}]")
print(f"  Grid spacing: {dy:.6f}")
print(f"  Max prime captured: ~{int(np.exp(Y_MAX))}")

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
print(f"  4n+1 primes: {len(primes_4n1)}")
print(f"  4n+3 primes: {len(primes_4n3)}")
print(f"  Anchor primes: {len(primes_S)}")
print(f"  Total primes: {len(primes_4n1) + len(primes_4n3) + len(primes_S)}")

# Build kinetic operator first to understand energy scale
T_matrix = np.zeros((N_GRID, N_GRID))
T_matrix += np.diag(-2 * np.ones(N_GRID))
T_matrix += np.diag(np.ones(N_GRID - 1), k=1)
T_matrix += np.diag(np.ones(N_GRID - 1), k=-1)
T_matrix *= -1.0 / (2.0 * dy**2)

kinetic_scale = 1.0 / (2.0 * dy**2)
print(f"Kinetic energy scale: {kinetic_scale:.2f}")

# The coupling constant should be chosen to match the target eigenvalue scale
# Since we want eigenvalues ~ (14-65)^2 ~ 200-4000, and kinetic scale is ~40000,
# we need the potential to be on the same order of magnitude
target_eigenvalue_scale = 500  # Target for first few eigenvalues
COUPLING_CONSTANT = target_eigenvalue_scale * 50  # Scale potential appropriately

print(f"Using coupling constant: {COUPLING_CONSTANT}")

V_potential = np.zeros(N_GRID)

def place_potential_on_grid(p_list, sign):
    """Places weighted prime potentials onto the discrete grid."""
    placed_count = 0
    for p in p_list:
        log_p = np.log(p)
        if Y_MIN < log_p < Y_MAX:
            idx = int((log_p - Y_MIN) / dy)
            if idx < N_GRID:  # Safety check
                V_potential[idx] += sign * (p**(-0.5)) * COUPLING_CONSTANT
                placed_count += 1
    return placed_count

placed_4n1 = place_potential_on_grid(primes_4n1, 1.0)
placed_4n3 = place_potential_on_grid(primes_4n3, -1.0)
placed_S = place_potential_on_grid(primes_S, 1.0)

print(f"Primes placed on grid:")
print(f"  4n+1 primes placed: {placed_4n1}")
print(f"  4n+3 primes placed: {placed_4n3}")
print(f"  Anchor primes placed: {placed_S}")

print(f"Potential statistics:")
print(f"  Non-zero elements: {np.count_nonzero(V_potential)}")
print(f"  Max potential: {np.max(V_potential):.2f}")
print(f"  Min potential: {np.min(V_potential):.2f}")

V_matrix = np.diag(V_potential)

# --- 3. Form the Hamiltonian and Solve for Eigenvalues ---
print("Constructing Hamiltonian matrix...")
H_matrix = T_matrix + V_matrix

# Compute eigenvalues
num_eigenvalues = 25
print(f"Computing {num_eigenvalues} lowest eigenvalues...")
eigenvalues = linalg.eigvalsh(H_matrix, subset_by_index=[0, num_eigenvalues-1])

print(f"\nFirst {num_eigenvalues} eigenvalues:")
for i, ev in enumerate(eigenvalues):
    print(f"  {i+1:2d}: {ev:10.2f}")

# The eigenvalues E_n of this operator should approximate t_n^2
positive_eigenvalues = eigenvalues[eigenvalues > 0]
computed_zeros_approx = np.sqrt(positive_eigenvalues)

print(f"\nPositive eigenvalues: {len(positive_eigenvalues)}")
print(f"Computed zeros (square roots):")
for i, zero in enumerate(computed_zeros_approx):
    print(f"  {i+1:2d}: {zero:10.6f}")

# --- 4. Compare with Known Riemann Zeros ---
known_zeros = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062, 
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
    52.910381, 56.446248, 59.347044, 60.831779, 65.112544
]

# --- 5. Plotting the Comparison ---
plt.figure(figsize=(14, 10))
plt.eventplot(known_zeros[:10], orientation='horizontal', colors='r', linelengths=0.8, 
              lineoffsets=1, label=f'First 10 Known Riemann Zeros')
if len(computed_zeros_approx) > 0:
    plt.eventplot(computed_zeros_approx[:10], orientation='horizontal', colors='b', linelengths=0.8, 
                  lineoffsets=2, label=f'First 10 Computed Zeros from Model')

plt.title('Spectral Test of the Λ-Core Prime Hamiltonian (Fixed)', fontsize=16)
plt.yticks([1, 2], ['Known Zeros (from literature)', 'Eigenvalues of Model'])
plt.xlabel('Height on the Critical Line (t)', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, axis='x', linestyle=':', alpha=0.7)
plt.ylim(0.5, 2.5)
plt.xlim(0, 70)
plt.tight_layout()
plt.savefig('riemann_zeros_comparison_fixed.png', dpi=300, bbox_inches='tight')
plt.show()

# --- 6. Print Table of Results ---
print("\nTable 1: Comparison of Computed Spectrum vs. Known Riemann Zeros")
print("="*75)
print(f"{'n':<5}{'Known Zero (t_n)':<20}{'Computed Zero':<20}{'Relative Error (%)':<20}")
print("-"*75)

comparison_count = min(len(computed_zeros_approx), len(known_zeros), 10)
if comparison_count > 0:
    for i in range(comparison_count):
        error = 100 * abs(computed_zeros_approx[i] - known_zeros[i]) / known_zeros[i]
        print(f"{i+1:<5}{known_zeros[i]:<20.6f}{computed_zeros_approx[i]:<20.6f}{error:<20.2f}")
    
    # Calculate statistics
    errors = [100 * abs(computed_zeros_approx[i] - known_zeros[i]) / known_zeros[i] 
              for i in range(comparison_count)]
    print("="*75)
    print(f"\nStatistical Summary ({comparison_count} zeros):")
    print(f"  Mean relative error: {np.mean(errors):.2f}%")
    print(f"  Std deviation of error: {np.std(errors):.2f}%")
    print(f"  Max relative error: {np.max(errors):.2f}%")
    print(f"  Min relative error: {np.min(errors):.2f}%")
else:
    print("No positive eigenvalues found for comparison")
    print("="*75)

print("="*50) 