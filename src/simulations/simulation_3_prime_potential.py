import numpy as np
import matplotlib.pyplot as plt

def get_prime_partitions(limit=500):
 """Generates primes and partitions them."""
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

print("=== Simulation 3: Prime Potential Visualization ===")
primes_4n1, primes_4n3, primes_S = get_prime_partitions()

# Get the logarithmic positions
log_pos_4n1 = np.log(primes_4n1)
log_pos_4n3 = np.log(primes_4n3)
log_pos_S = np.log(primes_S)

# Get the weights (w_p = p^(-1/2))
weights_4n1 = np.array(primes_4n1)**(-0.5)
weights_4n3 = np.array(primes_4n3)**(-0.5)
weights_S = np.array(primes_S)**(-0.5)

# Visualize the potential V(y)
plt.figure(figsize=(15, 10))
# We plot the Hyperbolic primes with a negative sign to visually represent the opposition
plt.stem(log_pos_4n1, weights_4n1, linefmt='b-', markerfmt='bo', basefmt=' ', 
 label='V_E (4n+1 Primes - Proximity)')
plt.stem(log_pos_4n3, -weights_4n3, linefmt='r-', markerfmt='ro', basefmt=' ', 
 label='V_H (4n+3 Primes - Identity)')
plt.stem(log_pos_S, weights_S, linefmt='g-', markerfmt='go', basefmt=' ', 
 label='V_S (Anchor Primes)')
plt.title('The Prime Potential V(y) on a Logarithmic Axis', fontsize=16)
plt.xlabel('y = log(x)', fontsize=14)
plt.ylabel('Potential Strength (w_p = p^(-1/2))', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('prime_potential.png', dpi=300, bbox_inches='tight')
plt.show()

print(f"Number of 4n+1 primes: {len(primes_4n1)}")
print(f"Number of 4n+3 primes: {len(primes_4n3)}")
print(f"Number of anchor primes: {len(primes_S)}")
print(f"Total primes plotted: {len(primes_4n1) + len(primes_4n3) + len(primes_S)}")
print("="*50) 