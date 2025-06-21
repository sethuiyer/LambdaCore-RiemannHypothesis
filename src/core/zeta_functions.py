"""
LambdaCore-RiemannHypothesis: Zeta Functions Module

Core implementations of zeta function computations, Euler products,
and Dirichlet series for the spectral framework.

Author: Sethu Iyer (https://sethuiyer.github.io/)
Date: December 2024
Version: 1.1
"""

import numpy as np
from scipy.special import zeta as scipy_zeta
import warnings

def dirichlet_series_zeta(s, max_terms=10000):
 """
 Compute ζ(s) using the Dirichlet series representation.
 
 ζ(s) = Σ(n=1 to ∞) 1/n^s
 
 Args:
 s (float): The complex argument
 max_terms (int): Maximum number of terms to include
 
 Returns:
 complex: The computed value of ζ(s)
 """
 if np.real(s) <= 1:
 warnings.warn("Dirichlet series convergence requires Re(s) > 1")
 
 n_values = np.arange(1, max_terms + 1)
 terms = 1.0 / (n_values ** s)
 return np.sum(terms)

def euler_product_zeta(s, max_prime=1000):
 """
 Compute ζ(s) using the Euler product representation.
 
 ζ(s) = Π(p prime) 1/(1 - p^(-s))
 
 Args:
 s (float): The complex argument
 max_prime (int): Maximum prime to include in product
 
 Returns:
 complex: The computed value of ζ(s)
 """
 if np.real(s) <= 1:
 warnings.warn("Euler product convergence requires Re(s) > 1")
 
 primes = sieve_of_eratosthenes(max_prime)
 product = 1.0
 
 for p in primes:
 factor = 1.0 / (1.0 - p**(-s))
 product *= factor
 
 return product

def sieve_of_eratosthenes(limit):
 """
 Generate primes up to limit using the Sieve of Eratosthenes.
 
 Args:
 limit (int): Upper bound for prime generation
 
 Returns:
 list: List of prime numbers up to limit
 """
 if limit < 2:
 return []
 
 is_prime = [True] * (limit + 1)
 is_prime[0] = is_prime[1] = False
 
 for p in range(2, int(np.sqrt(limit)) + 1):
 if is_prime[p]:
 for i in range(p * p, limit + 1, p):
 is_prime[i] = False
 
 return [p for p in range(2, limit + 1) if is_prime[p]]

def validate_zeta_identity(s=2.0, max_terms=10000, max_prime=1000, tolerance=1e-6):
 """
 Validate the fundamental identity: Dirichlet series = Euler product.
 
 Args:
 s (float): Test value for ζ(s)
 max_terms (int): Terms for Dirichlet series
 max_prime (int): Primes for Euler product
 tolerance (float): Acceptable error threshold
 
 Returns:
 dict: Validation results including both values and error
 """
 dirichlet_val = dirichlet_series_zeta(s, max_terms)
 euler_val = euler_product_zeta(s, max_prime)
 exact_val = scipy_zeta(s)
 
 dirichlet_error = abs(dirichlet_val - exact_val) / abs(exact_val)
 euler_error = abs(euler_val - exact_val) / abs(exact_val)
 identity_error = abs(dirichlet_val - euler_val) / abs(exact_val)
 
 return {
 'dirichlet_value': dirichlet_val,
 'euler_value': euler_val,
 'exact_value': exact_val,
 'dirichlet_error': dirichlet_error,
 'euler_error': euler_error,
 'identity_error': identity_error,
 'validation_passed': identity_error < tolerance
 }

def known_riemann_zeros():
 """
 Return the first 15 known nontrivial zeros of the Riemann zeta function.
 
 Returns:
 list: Heights of the first 15 zeros on the critical line
 """
 return [
 14.134725141734693790, 21.022039638771554993, 25.010857580145688763,
 30.424876125859513210, 32.935061587739189690, 37.586178158825671257,
 40.918719012147495187, 43.327073280914999519, 48.005150881167159727,
 49.773832477672302181, 52.910381279279131003, 56.446247697063446123,
 59.347044003392468915, 60.831778524671805049, 65.112544048081651204
 ]

def mean_zero_spacing(max_height=100):
 """
 Compute the mean spacing between consecutive Riemann zeros.
 Uses the asymptotic formula: spacing ≈ 2π/log(t/(2π))
 
 Args:
 max_height (float): Height on critical line
 
 Returns:
 float: Mean spacing at given height
 """
 return 2 * np.pi / np.log(max_height / (2 * np.pi)) 