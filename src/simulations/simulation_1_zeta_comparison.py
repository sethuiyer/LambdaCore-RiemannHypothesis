import numpy as np

def dirichlet_sum(s, limit=2000):
    """Calculates the zeta function using the Dirichlet series sum."""
    return np.sum([1 / (n**s) for n in range(1, limit + 1)])

def euler_product(s, limit=2000):
    """Calculates the zeta function using the Euler product over primes."""
    
    def get_primes(n):
        """Simple sieve to get primes up to n."""
        primes = []
        is_prime = [True] * (n + 1)
        is_prime[0] = is_prime[1] = False
        for p in range(2, int(np.sqrt(n)) + 1):
            if is_prime[p]:
                for i in range(p * p, n + 1, p):
                    is_prime[i] = False
        for p in range(2, n + 1):
            if is_prime[p]:
                primes.append(p)
        return primes

    primes_up_to_limit = get_primes(limit)
    product = 1.0
    for p in primes_up_to_limit:
        product *= (1 - 1 / (p**s))**-1
    return product

s_val = 2 + 0j  # A complex value for s with Re(s) > 1

zeta_from_sum = dirichlet_sum(s_val)
zeta_from_product = euler_product(s_val)
actual_zeta_2 = np.pi**2 / 6  # The known value for ζ(2)

print("=== Simulation 1: Zeta Function Comparison ===")
print(f"Calculating for s = {s_val}")
print(f"Dirichlet Sum approx:      {zeta_from_sum.real:.6f}")
print(f"Euler Product approx:      {zeta_from_product.real:.6f}")
print(f"Actual value of ζ(2):      {actual_zeta_2:.6f}")
print(f"Dirichlet Sum error:       {abs(zeta_from_sum.real - actual_zeta_2):.6f}")
print(f"Euler Product error:       {abs(zeta_from_product.real - actual_zeta_2):.6f}")
print("="*50) 