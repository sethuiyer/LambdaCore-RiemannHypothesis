import numpy as np

# --- Parameters for the Discretized Operator ---
# N: Number of internal grid points. Higher N -> finer resolution -> more eigenvalues -> higher accuracy
# but also slower computation. N=1000 is a good balance for initial check.
N = 1000 

# epsilon: Small value to approximate the singularity at r=0. log(epsilon) is the left boundary.
# Smaller epsilon means the domain extends further towards the singularity.
epsilon = 1e-3 # Corresponds to t_start = log(1e-3) approx -6.907

# T: Right boundary of the discretized domain in t-coordinates (t = log(r)).
# Larger T means the domain extends further away from the singularity.
T = 10 # Corresponds to r_end = e^10 approx 22026

# --- Derived Parameters ---
# h: Grid spacing
h = (T - np.log(epsilon)) / N

# --- Constructing the (N-1)x(N-1) Tridiagonal Matrix A ---
# A represents the discretized L_radial = -d²/dt² + 3/4 operator
# A_{i,i} = 2/h² + 3/4 (main diagonal)
# A_{i,i±1} = -1/h² (off-diagonals)

# Create a matrix of zeros
A = np.zeros((N-1, N-1))

# Fill the main diagonal
main_diag_val = 2 / (h**2) + 3/4
np.fill_diagonal(A, main_diag_val)

# Fill the off-diagonals
off_diag_val = -1 / (h**2)
np.fill_diagonal(A[1:], off_diag_val) # Upper diagonal
np.fill_diagonal(A[:,1:], off_diag_val) # Lower diagonal

# --- Compute Eigenvalues ---
# eigvalsh is used for symmetric matrices (our A is symmetric tridiagonal)
# It's generally faster and more stable for this type of matrix.
print(f"Computing eigenvalues for a {N-1}x{N-1} matrix. This might take a moment...")
eigenvalues = np.linalg.eigvalsh(A)

# Sort eigenvalues in ascending order
eigenvalues.sort()

# --- Target Riemann Zeta Zero Eigenvalues ---
# These are the imaginary parts (tau_k) of the first few non-trivial zeta zeros: s_k = 1/2 + i*tau_k
# The predicted eigenvalues for our operator are lambda_k = tau_k^2 + 1/2
tau_k_values = [
 14.134725141734693790457251983562, # tau_1
 21.022039638771554992628479944487, # tau_2
 25.010857580145688763213790992562, # tau_3
 30.424876125955026978648178873734, # tau_4
 32.935061587739189690422552994968, # tau_5
]

# Calculate the predicted lambda values
lambda_predicted = [tau**2 + 0.5 for tau in tau_k_values]

# --- Find Closest Computed Eigenvalues ---
print("\n--- Matching Computed Eigenvalues to Predicted Zeta Zeros ---")
print("Note: Discretization yields discrete eigenvalues approximating a continuous spectrum.")
print(" We expect *some* computed eigenvalues to be close to our targets.")
print("---------------------------------------------------------------")

tolerance = 0.5 # A reasonable tolerance for matching discrete approx to continuous spectrum
found_matches = 0

for i, target_lambda in enumerate(lambda_predicted):
 # Find the index of the closest eigenvalue in our computed list
 closest_eigenvalue_idx = np.argmin(np.abs(eigenvalues - target_lambda))
 closest_eigenvalue = eigenvalues[closest_eigenvalue_idx]
 
 difference = np.abs(target_lambda - closest_eigenvalue)
 
 if difference < tolerance: # Check if it's within a reasonable match tolerance
 print(f"Target lambda_{i+1} (τ={tau_k_values[i]:.4f}): {target_lambda:.6f}")
 print(f" -> Closest computed eigenvalue: {closest_eigenvalue:.6f}")
 print(f" -> Difference: {difference:.6f} (MATCH!)")
 found_matches += 1
 else:
 print(f"Target lambda_{i+1} (τ={tau_k_values[i]:.4f}): {target_lambda:.6f}")
 print(f" -> Closest computed eigenvalue: {closest_eigenvalue:.6f}")
 print(f" -> Difference: {difference:.6f} (No direct match within tolerance)")

print(f"\nFound {found_matches} potential matches within tolerance for the first {len(tau_k_values)} Riemann zeta zeros.")

# --- General Spectral Properties (for debugging/interpretation) ---
print("\n--- General Spectral Properties of Discretized Operator ---")
print(f"Number of computed eigenvalues: {len(eigenvalues)}")
print(f"Minimum computed eigenvalue: {eigenvalues.min():.6f}")
print(f"Maximum computed eigenvalue: {eigenvalues.max():.6f}")
print(f"Expected minimum of continuous spectrum (V0 + 1/4): {0.5 + 0.25:.6f}") # Should be 0.75 for L_radial
