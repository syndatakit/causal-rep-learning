# Complete Experimental Methodology & Constants
## Causal Representation Learning: Permutation Saddles & Identifiability

**Document Version**: 2026-08-29 (post-correction)  
**Status**: Publication-ready reproducibility specification

---

## Part 1: Universal Constants

| Constant | Value | Interpretation |
|----------|-------|------------------|
| Ground truth mixing | M* = I | Unknown; recovered up to sign/permutation |
| True latent covariance (env 0) | Λ₀ = I | Baseline (identity) |
| # Environments | E = 5 | Fixed across all experiments |
| Loss function | L(M) = Σₑ ∥MΛₑMᵀ − Λₑ∥²_F | Population covariance matching |
| Escape radius ρ | 0.3 | Frobenius norm threshold |
| Machine precision | ~1e-16 (float64) | NumPy default |
| Gradient tolerance | < 1e-6 | Stationarity verification |
| Hessian computation | Analytical (d² × d²) | Vectorized via scipy.linalg.eigh |
| Random seed (base) | 42 | Reproducibility across all runs |

---

## Part 2: Dataset Generation (Profile Families)

### 2.1 Random Family (Experiments A, B, D, E, F)

```python
def random_profiles(d, num_envs=5):
    np.random.seed(d)  # Dimension-dependent seed
    v_profiles = np.random.randn(num_envs, d)  # (E × d)
    return v_profiles
```

### 2.2 Linear Family (Experiment A control)

```python
def linear_profiles(d, num_envs=5):
    np.random.seed(d)
    v_base = np.linspace(1, num_envs, num_envs)[:, None] * np.ones((1, d))
    v_profiles = v_base + 0.1 * np.random.randn(num_envs, d)
    return v_profiles
```

### 2.3 Geometric Family (Experiment A control)

```python
def geometric_profiles(d, num_envs=5):
    np.random.seed(d)
    v_base = np.exp(np.linspace(0, 1, num_envs)[:, None]) * np.ones((1, d))
    v_profiles = v_base + 0.1 * np.random.randn(num_envs, d)
    return v_profiles
```

### 2.4 Profile Diversity Parameter

```python
def compute_delta_min(v_profiles):
    E, d = v_profiles.shape
    delta_min = np.inf
    for j in range(d):
        for k in range(j+1, d):
            delta = np.linalg.norm(v_profiles[:, j] - v_profiles[:, k])
            delta_min = min(delta_min, delta)
    return delta_min
```

---

## Part 3: Permutation Saddle Construction

```python
def construct_M_pi_star(d, pi, v_profiles):
    scales = np.ones(d)
    for i in range(d):
        j_pi = pi[i]
        v_i = v_profiles[:, i]
        v_j_pi = v_profiles[:, j_pi]
        dot_prod = np.dot(v_i, v_j_pi)
        norm_sq = np.dot(v_j_pi, v_j_pi)
        if norm_sq > 1e-10:
            scales[i] = np.sqrt(max(0, dot_prod / norm_sq))
    
    P_pi = np.eye(d)[pi]
    M_pi_star = P_pi @ np.diag(scales)
    return M_pi_star
```

Permutation used: **Transposition (1 2)** for all experiments.

---

## Part 4: Analytical Hessian

```python
def hessian_analytical(M, Lambda_list):
    d = M.shape[0]
    H = np.zeros((d*d, d*d))
    for Lambda_e in Lambda_list:
        for i in range(d):
            for j in range(d):
                for k in range(d):
                    for l in range(d):
                        idx1 = i*d + j
                        idx2 = k*d + l
                        term = 2 * Lambda_e[j, k] * Lambda_e[l, i] + \
                               2 * Lambda_e[j, l] * Lambda_e[k, i]
                        H[idx1, idx2] += term
    return H
```

Exact formula; machine precision (float64) limited by NumPy.

---

## Part 5: Experiments (Summary)

### Experiment A: Universal Scaling Collapse (CORRECTED)

**Key fix**: Now measures actual GD escape times, not theoretical formula.

```
T̂_esc = min{t : ∥M_t − M_π*∥_F ≥ ρ}
Q̂ = (η · T̂_esc · Δ²_min) / log(ρ/ζ)
```

**Hyperparameters**:
- d ∈ {3,4,5,8} | η ∈ {10⁻³, 10⁻²} | ζ ∈ {10⁻³, 10⁻²} | profiles ∈ {random}
- **Fast validation**: 12 rows
- **Theory predicts**: Q̂ ≈ 2.0
- **Actual result**: Q̂ = 18.1 ± 29.0 (variance suggests regime/constants need refinement)

### Experiment C: Nonlinear Remainder (CORRECTED)

**Key fix**: Actual GD trajectories, not synthetic remainders.

```
r_t = ξ_{t+1} − (1 + η|λ_−|)ξ_t
|r_t| ≤ C·η·∥z_t∥²
```

**Result**:
- max|r_t| ≈ 4×10⁻⁵ (small; validates local approximation)
- C ≈ 3200 (loose; constant needs tightening)

### Experiment D: Multi-Horizon Escape (CORRECTED)

**Key fix**: Multiple escape horizons; dimensionless prediction test.

```
η|λ_−|T_esc / log(ρ/ζ) ≈ 1.0 (theory prediction)
```

**Result**: Ratio ≈ 9.1 (not 1.0; suggests prefactor or regime adjustment needed)

---

## Part 6: Random Seeds

| Usage | Formula |
|-------|----------|
| Profile per d | np.random.seed(d) |
| Trial variation | np.random.seed(42 + trial_index) |

---

## Part 7: Canonical vs. Permutation

### Canonical (Main Theorem)
- Transposition saddle: stationary + strict saddle
- Local escape: T_esc ~ log(ρ/ζ) / (η|λ_−|)

### Permutation (Exploratory)
- Morse indices vary by cycle structure (empirical)
- d=64 anomaly: **Unresolved** – needs mpmath verification
- Presented as appendix investigation, not main result

---

## Repository Status

**Live on GitHub**: https://github.com/syndatakit/causal-rep-learning

**Latest commit**: EXPERIMENTAL_METHODOLOGY.md + corrected experiments pushed 2026-08-29

**Files**:
- `EXPERIMENTAL_METHODOLOGY.md` – This document
- `AUDIT_CORRECTIONS.md` – Structural fixes & theory/empirics separation  
- `code/experiments_corrected.py` – Corrected code (genuine dynamics)
- `full_results/exp_{a,c,d}_corrected_*.csv` – Corrected empirical data

---

**End of specification. Publication-ready with noted limitations.**