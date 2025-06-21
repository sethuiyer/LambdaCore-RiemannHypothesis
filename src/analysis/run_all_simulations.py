#!/usr/bin/env python3
"""
Master script to run all Λ-Core Riemann Hypothesis simulations
"""

import subprocess
import sys
import time

def run_simulation(script_name, description):
 """Run a simulation script and capture output"""
 print(f"\n{'='*60}")
 print(f"RUNNING: {description}")
 print(f"Script: {script_name}")
 print(f"{'='*60}")
 
 start_time = time.time()
 try:
 result = subprocess.run([sys.executable, script_name], 
 capture_output=True, text=True, check=True)
 print(result.stdout)
 if result.stderr:
 print("STDERR:", result.stderr)
 
 elapsed = time.time() - start_time
 print(f"\n {description} completed successfully in {elapsed:.2f} seconds")
 
 except subprocess.CalledProcessError as e:
 elapsed = time.time() - start_time
 print(f" {description} failed after {elapsed:.2f} seconds")
 print("STDOUT:", e.stdout)
 print("STDERR:", e.stderr)
 return False
 
 return True

def main():
 """Run all simulations"""
 print(" Starting Λ-Core Riemann Hypothesis Simulation Suite")
 print(f"Python version: {sys.version}")
 
 simulations = [
 ("simulation_1_zeta_comparison.py", "Zeta Function Comparison (Dirichlet vs Euler)"),
 ("simulation_2_prime_partitions.py", "Prime Class Partitioning and Visualization"),
 ("simulation_3_prime_potential.py", "Prime Potential V(y) Visualization"),
 ("simulation_4_hamiltonian_eigenvalues.py", "Hamiltonian Eigenvalue Analysis")
 ]
 
 total_start = time.time()
 successful = 0
 
 for script, description in simulations:
 if run_simulation(script, description):
 successful += 1
 time.sleep(1) # Brief pause between simulations
 
 total_elapsed = time.time() - total_start
 
 print(f"\n{'='*60}")
 print(f"SIMULATION SUITE COMPLETE")
 print(f"{'='*60}")
 print(f"Total time: {total_elapsed:.2f} seconds")
 print(f"Successful: {successful}/{len(simulations)}")
 
 if successful == len(simulations):
 print(" All simulations completed successfully!")
 print("\nGenerated files:")
 print(" - prime_partitions.png")
 print(" - prime_potential.png") 
 print(" - riemann_zeros_comparison.png")
 else:
 print(f" {len(simulations) - successful} simulation(s) failed")
 return 1
 
 return 0

if __name__ == "__main__":
 sys.exit(main()) 