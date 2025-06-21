"""
LambdaCore-RiemannHypothesis: Core Package

Core mathematical implementations for the Λ-Core spectral framework.

Author: Sethu Iyer (https://sethuiyer.github.io/)
Date: December 2024
Version: 1.1
"""

from .zeta_functions import (
 dirichlet_series_zeta,
 euler_product_zeta,
 sieve_of_eratosthenes,
 validate_zeta_identity,
 known_riemann_zeros,
 mean_zero_spacing
)

from .prime_operators import (
 PrimePartitioner,
 PrimePotential
)

from .spectral_solver import (
 QuantumHamiltonian
)

__version__ = "1.1"
__author__ = "Sethu Iyer"

__all__ = [
 'dirichlet_series_zeta',
 'euler_product_zeta', 
 'sieve_of_eratosthenes',
 'validate_zeta_identity',
 'known_riemann_zeros',
 'mean_zero_spacing',
 'PrimePartitioner',
 'PrimePotential',
 'QuantumHamiltonian'
] 