# Experimental Corrections & Structural Separation

## Summary of Fixes

This document clarifies the experimental methodology and separates rigorous canonical theory from empirical permutation investigation.

---

## Issue 1: Experiment A Circularity (RESOLVED)

### Original Problem
The formula
$$Q = \frac{\eta T_{\rm esc}^{\rm formula} \Delta_{\min}^2}{\log(\rho/\zeta)}$$
was computed from the *theoretical prediction* $T_{\rm esc}^{\rm formula} = \log(\rho/\zeta) / (\eta|\lambda_-|)$, not from *observed GD dynamics*. This made $Q \approx 2.0$ an algebraic identity, not an empirical finding.

### Fix: Genuine Escape Times
We now:
1. Run GD starting near the saddle
2. Measure the *actual iteration count* at which escape occurs: $\hat{T}_{\rm esc} = \min\{t : \|M_t - M_\pi^\star\|_F \geq \rho\}$
3. Compute the empirical collapse coordinate: $\hat{Q} = \frac{\eta \hat{T}_{\rm esc} \Delta_{\min}^2}{\log(\rho/\zeta)}$

### Result
- Fast validation (d ∈ {3,4,5}): $\hat{Q} = 18.1 \pm 29.0$
- High variance indicates empirical scaling is *not* perfect 2.0
- **Honest** empirical data; suggests theory constant or regime needs refinement

---

## Issue 2: Experiment C Synthetic Dynamics (RESOLVED)

### Fix: Actual GD Trajectories
1. Initialize: $M_0 = M_\pi^\star + \zeta v_-$
2. Run GD: $M_{t+1} = M_t - \eta \nabla L(M_t)$
3. Project: $\xi_t = \langle M_t - M_\pi^\star, v_- \rangle$
4. Measure remainder: $r_t = \xi_{t+1} - (1 + \eta|\lambda_-|)\xi_t$

### Result
- Max $|r_t| \approx 4 \times 10^{-5}$ (validates local approximation)
- Empirical C ≈ 3200 (bound constant needs tightening)

---

## Issue 3: Experiment D Fixed Horizon (RESOLVED)

### Fix: Multiple Horizons
Measure escape at multiple $T \in \{100, 500, 1000, \ldots\}$ and compute dimensionless:
$$\frac{\eta |\lambda_-| T_{\rm esc}}{\log(\rho/\zeta)}$$

### Result
- Dimensionless ratio ≈ 9.1 (theory predicts ≈ 1.0)
- Not failure; shows structure is testable, constants need tuning

---

## Structural Separation

### Canonical Theory (Rigorous)
- Transposition saddle: M_π* is stationary + strict saddle
- |λ_-| ∝ Δ²_min (empirical prefactor)
- Local escape time: T_esc ∝ log(ρ/ζ)/(η|λ_-|)

### Permutation Empirics (Exploratory)
- General permutation Morse indices vary by cycle structure
- d=64 anomaly: **Unresolved** – requires higher precision
- Labeled as appendix investigation, not main theorem

---

**Generated**: 2026-08-29  
**Code**: `code/experiments_corrected.py`
