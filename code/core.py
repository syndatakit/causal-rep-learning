#!/usr/bin/env python3
"""
Core loss function, profile construction, and saddle point setup.
"""
import numpy as np
from scipy.linalg import eigh

def loss_covariance_matching(M, Lambda_list):
    """
    Population covariance-matching loss for causal representation learning.
    
    L(M) = sum_e || M @ Lambda_e @ M^T - Lambda_e ||_F^2
    
    Args:
        M: (d, d) mixing matrix
        Lambda_list: list of (d, d) diagonal covariance matrices
    
    Returns:
        float: loss value
    """
    loss = 0
    for Lambda_e in Lambda_list:
        M_Lambda_MT = M @ Lambda_e @ M.T
        diff = M_Lambda_MT - Lambda_e
        loss += np.sum(diff**2)
    return loss

def gradient_loss(M, Lambda_list):
    """Gradient of loss w.r.t. M."""
    grad = np.zeros_like(M)
    for Lambda_e in Lambda_list:
        M_Lambda_MT = M @ Lambda_e @ M.T
        diff = M_Lambda_MT - Lambda_e
        grad += 4 * diff @ Lambda_e @ M.T
    return grad

def hessian_loss_analytical(M, Lambda_list):
    """
    Analytic Hessian of loss w.r.t. M (vectorized form).
    Shape: (d^2, d^2)
    """
    d = M.shape[0]
    H = np.zeros((d*d, d*d))
    
    for Lambda_e in Lambda_list:
        # Second derivative
        for i in range(d):
            for j in range(d):
                for k in range(d):
                    for l in range(d):
                        idx1 = i*d + j
                        idx2 = k*d + l
                        # H[i,j,k,l] contribution
                        term = (2 * Lambda_e[j, k] * Lambda_e[l, i] +
                               2 * Lambda_e[j, l] * Lambda_e[k, i])
                        H[idx1, idx2] += term
    return H

def construct_profile_family(d, family_type='random', num_envs=5, separation=0.1):
    """
    Construct environment profile list v_j = (λ_0j, λ_1j, ..., λ_{E-1,j}).
    
    Args:
        d: latent dimension
        family_type: 'random', 'linear', or 'geometric'
        num_envs: number of environments
        separation: controls profile separation Δ_min
    
    Returns:
        v_profiles: (num_envs, d) array of profiles
        Delta_min: minimum pairwise profile separation
    """
    np.random.seed(d)
    
    if family_type == 'random':
        v_profiles = np.random.randn(num_envs, d)
    elif family_type == 'linear':
        v_profiles = np.linspace(1, num_envs, num_envs)[:, None] * np.ones((1, d))
        v_profiles += separation * np.random.randn(num_envs, d)
    elif family_type == 'geometric':
        v_profiles = np.exp(np.linspace(0, 1, num_envs)[:, None]) * np.ones((1, d))
        v_profiles += separation * np.random.randn(num_envs, d)
    else:
        raise ValueError(f"Unknown family_type: {family_type}")
    
    # Compute Δ_min
    Delta_min = np.inf
    for j in range(d):
        for k in range(j+1, d):
            delta_jk = np.linalg.norm(v_profiles[:, j] - v_profiles[:, k])
            Delta_min = min(Delta_min, delta_jk)
    
    return v_profiles, Delta_min

def construct_permutation_saddle(d, pi, v_profiles):
    """
    Construct scaled permutation matrix M_π^* = P_π @ diag(s_1^*, ..., s_d^*).
    
    s_i^* = sqrt(<v_i, v_{π(i)}> / ||v_{π(i)}||^2)
    
    Args:
        d: dimension
        pi: permutation array (0-indexed)
        v_profiles: (num_envs, d) array
    
    Returns:
        M_pi_star: (d, d) saddle point matrix
        scales: scaling factors s_i^*
    """
    scales = np.ones(d)
    for i in range(d):
        j_pi = pi[i]
        v_i = v_profiles[:, i]
        v_j_pi = v_profiles[:, j_pi]
        dot_prod = np.dot(v_i, v_j_pi)
        norm_sq = np.dot(v_j_pi, v_j_pi)
        if norm_sq > 1e-10:
            scales[i] = np.sqrt(dot_prod / norm_sq)
    
    P_pi = np.eye(d)[pi]
    M_pi_star = P_pi @ np.diag(scales)
    
    return M_pi_star, scales
