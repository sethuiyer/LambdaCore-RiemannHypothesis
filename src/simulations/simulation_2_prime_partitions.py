import numpy as np
import matplotlib.pyplot as plt

def partition_primes(limit=10000):
    """Partitions primes up to a limit into 4n+1 and 4n+3 classes."""
    primes = []
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(np.sqrt(limit)) + 1):
        if is_prime[p]:
            for i in range(p * p, limit + 1, p):
                is_prime[i] = False
    for p in range(3, limit + 1):  # We exclude 2 for this classification
        if is_prime[p]:
            primes.append(p)
            
    class_4n1 = [p for p in primes if p % 4 == 1]
    class_4n3 = [p for p in primes if p % 4 == 3]
    
    return class_4n1, class_4n3

print("=== Simulation 2: Prime Class Partitioning ===")
primes_4n1, primes_4n3 = partition_primes()

# Plot the cumulative counts
plt.figure(figsize=(12, 8))
plt.plot(np.cumsum([1]*len(primes_4n1)), label='Count of 4n+1 Primes (Euclidean)', linewidth=2)
plt.plot(np.cumsum([1]*len(primes_4n3)), label='Count of 4n+3 Primes (Hyperbolic)', linewidth=2)
plt.title('Cumulative Counts of Prime Classes', fontsize=14)
plt.xlabel('N-th Prime in Class', fontsize=12)
plt.ylabel('Cumulative Count', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('prime_partitions.png', dpi=300, bbox_inches='tight')
plt.show()

print(f"Number of 4n+1 primes found: {len(primes_4n1)}")
print(f"Number of 4n+3 primes found: {len(primes_4n3)}")
print(f"Ratio (4n+3)/(4n+1): {len(primes_4n3)/len(primes_4n1):.4f}")
print("="*50) 