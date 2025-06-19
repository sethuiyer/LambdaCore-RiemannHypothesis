"""
LambdaCore-RiemannHypothesis: Spectral Solver Module

Implementation of the quantum Hamiltonian construction and eigenvalue
computation for the Λ-Core spectral framework.

Author: Sethu Iyer (https://sethuiyer.github.io/)
Date: December 2024
Version: 1.1
"""

import numpy as np
import scipy.linalg as linalg
import matplotlib.pyplot as plt
from .prime_operators import PrimePotential
from .zeta_functions import known_riemann_zeros

class QuantumHamiltonian:
    """
    Constructs and solves the quantum Hamiltonian H = T + V where:
    T = -1/2 * d²/dy² (kinetic energy operator)
    V = prime potential from the Λ-Core framework
    """
    
    def __init__(self, prime_potential, y_min=0, y_max=10, n_grid=1000):
        """
        Initialize the Hamiltonian constructor.
        
        Args:
            prime_potential (PrimePotential): The prime potential object
            y_min (float): Minimum coordinate value
            y_max (float): Maximum coordinate value
            n_grid (int): Number of grid points
        """
        self.prime_potential = prime_potential
        self.y_min = y_min
        self.y_max = y_max
        self.n_grid = n_grid
        self.dy = (y_max - y_min) / n_grid
        
        # Construct the Hamiltonian components
        self._construct_kinetic_operator()
        self._construct_potential_operator()
        self._construct_hamiltonian()
    
    def _construct_kinetic_operator(self):
        """
        Construct the kinetic energy operator T = -1/2 * d²/dy².
        Uses standard finite difference discretization.
        """
        self.T_matrix = np.zeros((self.n_grid, self.n_grid))
        
        # Second derivative finite difference: [-1, 2, -1] / dy²
        self.T_matrix += np.diag(-2 * np.ones(self.n_grid))
        self.T_matrix += np.diag(np.ones(self.n_grid - 1), k=1)
        self.T_matrix += np.diag(np.ones(self.n_grid - 1), k=-1)
        
        # Apply the -1/2 factor and grid scaling
        self.T_matrix *= -1.0 / (2.0 * self.dy**2)
    
    def _construct_potential_operator(self):
        """
        Construct the potential energy operator V from prime spectrum.
        """
        y_grid, V_potential = self.prime_potential.construct_discrete_potential(
            self.y_min, self.y_max, self.n_grid
        )
        self.V_matrix = np.diag(V_potential)
        self.y_grid = y_grid
        self.V_potential = V_potential
    
    def _construct_hamiltonian(self):
        """
        Construct the full Hamiltonian H = T + V.
        """
        self.H_matrix = self.T_matrix + self.V_matrix
    
    def solve_eigenvalues(self, num_eigenvalues=15, which='smallest'):
        """
        Solve for the eigenvalues of the Hamiltonian.
        
        Args:
            num_eigenvalues (int): Number of eigenvalues to compute
            which (str): Which eigenvalues to compute ('smallest', 'largest')
            
        Returns:
            tuple: (eigenvalues, eigenvectors)
        """
        if which == 'smallest':
            # Get the smallest eigenvalues
            eigenvalues = linalg.eigvalsh(
                self.H_matrix, 
                subset_by_index=[0, num_eigenvalues-1]
            )
        else:
            # For largest, need to compute more and select
            eigenvalues = linalg.eigvalsh(self.H_matrix)
            eigenvalues = eigenvalues[-num_eigenvalues:]
        
        # Filter for positive eigenvalues (physical spectrum)
        positive_eigenvalues = eigenvalues[eigenvalues > 0]
        
        return positive_eigenvalues
    
    def compute_riemann_approximation(self, num_zeros=15):
        """
        Compute approximation to Riemann zeros using eigenvalues.
        The correspondence is: t_n ≈ sqrt(E_n)
        
        Args:
            num_zeros (int): Number of zeros to approximate
            
        Returns:
            numpy.ndarray: Approximated zero heights
        """
        eigenvalues = self.solve_eigenvalues(num_zeros)
        return np.sqrt(eigenvalues)
    
    def validate_against_known_zeros(self, num_zeros=15):
        """
        Compare computed eigenvalues against known Riemann zeros.
        
        Args:
            num_zeros (int): Number of zeros to compare
            
        Returns:
            dict: Validation results and statistics
        """
        computed_zeros = self.compute_riemann_approximation(num_zeros)
        known_zeros = np.array(known_riemann_zeros()[:num_zeros])
        
        # Ensure we have the same number for comparison
        min_length = min(len(computed_zeros), len(known_zeros))
        computed_zeros = computed_zeros[:min_length]
        known_zeros = known_zeros[:min_length]
        
        # Compute relative errors
        relative_errors = np.abs(computed_zeros - known_zeros) / known_zeros * 100
        
        results = {
            'computed_zeros': computed_zeros,
            'known_zeros': known_zeros,
            'relative_errors': relative_errors,
            'mean_relative_error': np.mean(relative_errors),
            'max_relative_error': np.max(relative_errors),
            'min_relative_error': np.min(relative_errors),
            'num_compared': min_length
        }
        
        return results 