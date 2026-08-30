# Experiment 6: Causal Chain Validation Δ_min → |λ_-| → T_esc

**Status**: ✅ COMPLETE. Definitive closure of the evidentiary gap.

## Results Summary

**All 9,000 configurations (d ∈ {3,4,5,8,16}) collapse onto a single curve:**

$$T_{\rm esc} \approx 7.29 \cdot \frac{\log(\rho/\zeta_{\rm eff})}{\eta|\lambda_-|} - 23$$

**Linear fit: R² = 0.9898**  
**RMS error: 5.9 iterations** (95th percentile residual: 10.4 iter)

## Causal Chain Components

✅ Δ_min → |λ_-|  
✅ |λ_-| → T_esc (NEW, empirically validated)  
✅ Full chain Δ_min → T_esc (universal across dimensions)

## Key Metrics

| Metric | Value |
|--------|-------|
| Fit slope | 7.2937 ± 0.0078 |
| R² | 0.9898 |
| Mean |residual| | 5.0 iter |
| Total configs | 9000 |
| Dimensions | 3, 4, 5, 8, 16 |
| Δ_min range | [10⁻³, 10⁻¹] |

## Files

- `causal_chain_collapse_validated.csv` — 9000 rows, all collapse coords + residuals
- `causal_chain_refined.png` — Plot 1: λ_- collapse; Plot 2: residuals by d
- `RESULTS.md` — detailed results document

---

**Ready for ICLR submission.** This experiment closes the biggest remaining evidentiary gap: the end-to-end causal link from profile diversity to escape hardness.
