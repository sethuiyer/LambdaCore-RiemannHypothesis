"""
LambdaCore-RiemannHypothesis: Prime Operators Module

Implementation of prime partitioning, potential construction, and the
Λ-Core duality framework components.

Author: Sethu Iyer (https://sethuiyer.github.io/)
Date: December 2024
Version: 1.1
"""

import numpy as np
import matplotlib.pyplot as plt
from .zeta_functions import sieve_of_eratosthenes

class PrimePartitioner:
    """
    Handles the partitioning of primes into functional classes:
    - Euclidean (4n+1): Proximity-promoting forces
    - Hyperbolic (4n+3): Identity-injecting forces  
    - Anchor (2): Special boundary case
    """
    
    def __init__(self, max_prime=10000):
        """
        Initialize the partitioner with prime generation.
        
        Args:
            max_prime (int): Maximum prime to consider
        """
        self.max_prime = max_prime
        self.primes = sieve_of_eratosthenes(max_prime)
        self._partition_primes()
    
    def _partition_primes(self):
        """Partition primes into the three functional classes."""
        self.euclidean_primes = [p for p in self.primes if p % 4 == 1]
        self.hyperbolic_primes = [p for p in self.primes if p % 4 == 3]
        self.anchor_primes = [p for p in self.primes if p == 2]
    
    def get_partition_statistics(self):
        """
        Compute statistics on the prime partitioning.
        
        Returns:
            dict: Statistics including counts and ratios
        """
        n_euclidean = len(self.euclidean_primes)
        n_hyperbolic = len(self.hyperbolic_primes)
        n_anchor = len(self.anchor_primes)
        n_total = len(self.primes)
        
        # The ratio should approach 1.0 by Dirichlet's theorem
        balance_ratio = n_hyperbolic / n_euclidean if n_euclidean > 0 else float('inf')
        
        return {
            'euclidean_count': n_euclidean,
            'hyperbolic_count': n_hyperbolic,
            'anchor_count': n_anchor,
            'total_count': n_total,
            'balance_ratio': balance_ratio,
            'euclidean_fraction': n_euclidean / n_total,
            'hyperbolic_fraction': n_hyperbolic / n_total
        }
    
    def visualize_partition(self, save_path=None):
        """
        Create visualization of the prime partitioning.
        
        Args:
            save_path (str): Optional path to save the plot
        """
        stats = self.get_partition_statistics()
        
        # Create cumulative count plots
        euclidean_positions = np.searchsorted(self.primes, self.euclidean_primes)
        hyperbolic_positions = np.searchsorted(self.primes, self.hyperbolic_primes)
        
        euclidean_cumulative = np.arange(1, len(self.euclidean_primes) + 1)
        hyperbolic_cumulative = np.arange(1, len(self.hyperbolic_primes) + 1)
        
        plt.figure(figsize=(12, 8))
        plt.plot(self.euclidean_primes, euclidean_cumulative, 'b-', 
                linewidth=2, label=f'4n+1 Primes (Euclidean): {stats["euclidean_count"]}')
        plt.plot(self.hyperbolic_primes, hyperbolic_cumulative, 'r-', 
                linewidth=2, label=f'4n+3 Primes (Hyperbolic): {stats["hyperbolic_count"]}')
        
        plt.xlabel('Prime Value')
        plt.ylabel('Cumulative Count')
        plt.title(f'Prime Class Partitioning: Λ-Core Duality Framework\n'
                 f'Balance Ratio (4n+3)/(4n+1) = {stats["balance_ratio"]:.4f}')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()

class PrimePotential:
    """
    Constructs the quantum potential V(y) from the prime spectrum.
    
    V(y) = Σ_p w_p * δ(y - log(p)) * sign(p)
    
    where w_p = p^(-1/2) and sign(p) depends on the prime class.
    """
    
    def __init__(self, partitioner, coupling_constant=1.0):
        """
        Initialize the potential constructor.
        
        Args:
            partitioner (PrimePartitioner): Prime partition object
            coupling_constant (float): Overall energy scale
        """
        self.partitioner = partitioner
        self.coupling_constant = coupling_constant
    
    def construct_discrete_potential(self, y_min=0, y_max=10, n_grid=1000):
        """
        Construct the potential on a discrete grid.
        
        Args:
            y_min (float): Minimum y value (log scale)
            y_max (float): Maximum y value (log scale)
            n_grid (int): Number of grid points
            
        Returns:
            tuple: (y_grid, V_potential)
        """
        y_grid = np.linspace(y_min, y_max, n_grid)
        V_potential = np.zeros(n_grid)
        dy = (y_max - y_min) / n_grid
        
        # Place Euclidean primes (positive potential)
        for p in self.partitioner.euclidean_primes:
            log_p = np.log(p)
            if y_min < log_p < y_max:
                idx = int((log_p - y_min) / dy)
                if 0 <= idx < n_grid:
                    weight = p**(-0.5) * self.coupling_constant
                    V_potential[idx] += weight
        
        # Place Hyperbolic primes (negative potential)
        for p in self.partitioner.hyperbolic_primes:
            log_p = np.log(p)
            if y_min < log_p < y_max:
                idx = int((log_p - y_min) / dy)
                if 0 <= idx < n_grid:
                    weight = p**(-0.5) * self.coupling_constant
                    V_potential[idx] -= weight
        
        # Place Anchor primes (positive potential)
        for p in self.partitioner.anchor_primes:
            log_p = np.log(p)
            if y_min < log_p < y_max:
                idx = int((log_p - y_min) / dy)
                if 0 <= idx < n_grid:
                    weight = p**(-0.5) * self.coupling_constant
                    V_potential[idx] += weight
        
        return y_grid, V_potential
    
    def visualize_potential(self, y_min=0, y_max=6, n_grid=1000, save_path=None):
        """
        Visualize the prime potential landscape.
        
        Args:
            y_min (float): Minimum y value
            y_max (float): Maximum y value  
            n_grid (int): Grid resolution
            save_path (str): Optional save path
        """
        y_grid, V_potential = self.construct_discrete_potential(y_min, y_max, n_grid)
        
        # Separate visualization by prime class for clarity
        plt.figure(figsize=(15, 7))
        
        # Plot individual prime contributions
        for p in self.partitioner.euclidean_primes:
            log_p = np.log(p)
            if y_min < log_p < y_max:
                weight = p**(-0.5) * self.coupling_constant
                plt.stem([log_p], [weight], linefmt='b-', markerfmt='bo', 
                        basefmt=' ', alpha=0.7)
        
        for p in self.partitioner.hyperbolic_primes:
            log_p = np.log(p)
            if y_min < log_p < y_max:
                weight = p**(-0.5) * self.coupling_constant
                plt.stem([log_p], [-weight], linefmt='r-', markerfmt='ro', 
                        basefmt=' ', alpha=0.7)
        
        for p in self.partitioner.anchor_primes:
            log_p = np.log(p)
            if y_min < log_p < y_max:
                weight = p**(-0.5) * self.coupling_constant
                plt.stem([log_p], [weight], linefmt='g-', markerfmt='go', 
                        basefmt=' ', alpha=0.9)
        
        # Add legend and formatting
        plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        plt.xlabel('y = log(x)')
        plt.ylabel('Potential Strength V(y)')
        plt.title('The Prime Potential Landscape: Λ-Core Duality Framework')
        
        # Custom legend
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], marker='o', color='blue', linestyle='-', 
                   label='Euclidean Forces (4n+1 primes)'),
            Line2D([0], [0], marker='o', color='red', linestyle='-', 
                   label='Hyperbolic Forces (4n+3 primes)'),
            Line2D([0], [0], marker='o', color='green', linestyle='-', 
                   label='Anchor Forces (p=2)')
        ]
        plt.legend(handles=legend_elements, loc='upper right')
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def get_potential_statistics(self, y_min=0, y_max=10, n_grid=1000):
        """
        Compute statistics of the constructed potential.
        
        Returns:
            dict: Potential statistics and properties
        """
        y_grid, V_potential = self.construct_discrete_potential(y_min, y_max, n_grid)
        
        return {
            'max_potential': np.max(V_potential),
            'min_potential': np.min(V_potential),
            'mean_potential': np.mean(V_potential),
            'std_potential': np.std(V_potential),
            'positive_sites': np.sum(V_potential > 0),
            'negative_sites': np.sum(V_potential < 0),
            'zero_sites': np.sum(V_potential == 0)
        } 