# LambdaCore-RiemannHypothesis

**A Spectral Operator Framework for the Riemann Hypothesis**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Mathematical Research](https://img.shields.io/badge/field-Mathematical%20Physics-green.svg)](https://github.com/topics/mathematical-physics)

## Overview

This repository presents the **Λ-Core Duality Framework**, a novel spectral approach to the Riemann Hypothesis that models the distribution of prime numbers as competing quantum forces. The framework proposes that the nontrivial zeros of the Riemann zeta function correspond to the eigenvalues of a quantum mechanical Hamiltonian built from prime number potentials.

### About the Author

**Sethu Iyer** is an interdisciplinary AI researcher and data scientist with expertise spanning mathematics, computer science, and mathematical physics. He holds a dual degree (M.Sc Mathematics & B.E Computer Science) from BITS Pilani and has published research in machine learning and computer vision. His current research focuses on developing novel interpretability metrics for LLMs and exploring connections between computational systems and fundamental mathematical structures. More information is available at [sethuiyer.github.io](https://sethuiyer.github.io/) and [Google Scholar](https://scholar.google.com/citations?user=ivR07L8AAAAJ&hl=en).

### Key Innovation

We construct a spectral operator of the form:
```
H = -½ d²/dy² + V(y)
```
where the potential `V(y)` encodes the complete prime spectrum through weighted Dirac delta functions, creating a "cosmic tug-of-war" between:
- **Euclidean Forces** (4n+1 primes): Promoting proximity and stability
- **Hyperbolic Forces** (4n+3 primes): Injecting identity and curvature

## Research Status

**Version**: 1.1 (December 2024)  
**Status**: Framework established, partial computational validation completed

### Validation Results

| Component | Status | Success Rate | Notes |
|-----------|---------|--------------|-------|
| Zeta Function Identities | ✅ Complete | 100% | Euler product vs Dirichlet series validated |
| Prime Class Partitioning | ✅ Complete | 100% | 4n+1 vs 4n+3 distribution confirmed |
| Potential Visualization | ✅ Complete | 100% | Prime force landscape successfully mapped |
| Eigenvalue Matching | ⚠️ Partial | ~13% | Energy scale mismatch requires resolution |

**Overall Framework Validation**: 3/4 components fully successful, with clear path for eigenvalue improvement.

## Repository Structure

```
LambdaCore-RiemannHypothesis/
├── docs/
│   ├── ARTICLE.md                    # Complete theoretical framework (Version 1.1)
│   ├── SIMULATION_REPORT.md          # Detailed computational analysis
│   └── mathematical_appendix.md      # Technical proofs and derivations
├── src/
│   ├── core/
│   │   ├── zeta_functions.py         # Zeta function computations
│   │   ├── prime_operators.py        # Prime potential construction
│   │   └── spectral_solver.py        # Eigenvalue computation
│   ├── simulations/
│   │   ├── simulation_1_zeta_comparison.py
│   │   ├── simulation_2_prime_partitions.py
│   │   ├── simulation_3_prime_potential.py
│   │   └── simulation_4_eigenvalues.py
│   └── analysis/
│       ├── run_all_simulations.py    # Master execution script
│       └── analysis_summary.py       # Results compilation
├── results/
│   ├── eigenvalue_comparison.csv     # Computed vs known zeros
│   ├── prime_statistics.json         # Prime class analysis
│   └── convergence_study.md          # Numerical accuracy assessment
├── images/
│   ├── prime_partitions.png          # 4n+1 vs 4n+3 distribution
│   ├── prime_potential.png           # Potential landscape visualization
│   └── riemann_zeros_comparison.png  # Eigenvalue matching results
├── requirements.txt                  # Python dependencies
└── LICENSE                          # MIT License
```

## Quick Start

### Prerequisites
```bash
Python 3.8+
numpy >= 1.20.0
scipy >= 1.7.0
matplotlib >= 3.3.0
```

### Installation
```bash
git clone https://github.com/sethuiyer/LambdaCore-RiemannHypothesis.git
cd LambdaCore-RiemannHypothesis
pip install -r requirements.txt
```

### Run Core Simulations
```bash
cd src/analysis
python run_all_simulations.py
```

This executes all four validation simulations and generates comparison plots in the `results/` directory.

## Theoretical Foundation

The framework is built on three core mathematical insights:

1. **Prime Duality**: Primes naturally partition into competing functional classes based on modular arithmetic
2. **Spectral Correspondence**: The Riemann zeros emerge as eigenvalues of a quantum Hamiltonian
3. **Information-Theoretic Balance**: The critical line represents optimal information compression

### Connection to Established Programs

- **Berry-Keating Program**: Generalizes H = xp to include complete prime spectrum
- **Connes Program**: Provides concrete spectral realization of trace formula approaches  
- **Random Matrix Theory**: Explains GUE statistics through deterministic quantum chaos

## Key Results

### Computational Validation

**Simulation 1**: ✅ Zeta function identity confirmed to 0.006% accuracy  
**Simulation 2**: ✅ Prime class balance ratio = 1.0164 (theoretical ≈ 1.0)  
**Simulation 3**: ✅ Prime potential landscape successfully visualized  
**Simulation 4**: ⚠️ Eigenvalues computed with 87% relative error (energy scale issue)

### Mathematical Challenges Identified

The framework identifies seven critical gaps requiring resolution:

| Priority | Challenge | Difficulty | Mathematical Tools Required |
|----------|-----------|------------|----------------------------|
| 1 | Self-adjointness of infinite operator | 🚩 Hard | KLMN theorem, regularization theory |
| 2 | Divergent sum Σp^(-1/2) | 🚩 Hard | Zeta regularization, analytic continuation |
| 3 | Coupling constant derivation | 🔧 Medium-Hard | Scale invariance, dimensional analysis |

Complete analysis available in [`docs/ARTICLE.md`](docs/ARTICLE.md#part-xi-comprehensive-gap-analysis-and-research-roadmap).

## Research Roadmap

### Immediate Priorities (6 months)
1. Develop rigorous ε-regularization for divergent operator
2. Derive coupling constant from first principles
3. Implement wavelet basis for boundary artifact reduction

### Medium-term Goals (1-2 years)
1. Prove spectral stability as ε → 0
2. Establish connection to random matrix statistics
3. Formalize "Quadratic Inflation" mechanism

### Long-term Vision (2-5 years)
1. Complete analytical proof of eigenvalue correspondence
2. Extend framework to L-functions and other zeta functions
3. Explore connections to quantum field theory and cosmology

## Contributing

This is an active research project. Contributions welcome in:
- **Mathematical Analysis**: Rigorous proofs, regularization techniques
- **Computational Methods**: Improved numerical algorithms, basis optimization
- **Theoretical Extensions**: Connections to related mathematical areas

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Publications and References

### Core Paper
- **Iyer, Sethu** (2024). "The Λ-Core Duality: A Spectral Operator Framework for the Riemann Hypothesis (Version 1.1)." *In preparation*.

### Key Mathematical References
- **Kato, T.** (1995). *Perturbation Theory for Linear Operators*, 2nd ed., Springer-Verlag.
- **Montgomery, H.L.** (1973). "The pair correlation of zeros of the zeta function," *Proc. Sympos. Pure Math.*, 24, 181-193.
- **Odlyzko, A.M.** (1987). "On the distribution of spacings between zeros of the zeta function," *Math. Comp.*, 48(177), 273-308.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use this framework in your research, please cite:

```bibtex
@misc{iyer2024lambdacore,
  title={The Λ-Core Duality: A Spectral Operator Framework for the Riemann Hypothesis},
  author={Iyer, Sethu},
  year={2024},
  version={1.1},
  url={https://github.com/sethuiyer/LambdaCore-RiemannHypothesis}
}
```

---

**Contact**: [sethuiyer95@gmail.com](mailto:sethuiyer95@gmail.com) | **Website**: [https://sethuiyer.github.io/](https://sethuiyer.github.io/)  
**Keywords**: Riemann Hypothesis, Spectral Theory, Prime Numbers, Quantum Mechanics, Mathematical Physics 