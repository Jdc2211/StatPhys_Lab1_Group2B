import math

# Microscopic system calculations (N=123) for table 1 and the first three questions of part 4.2
N_micro = 123
M = 23
k_eq = 61  # k = floor(N/2) = 61 (most probable macrostate)

def log_probability(n, k):
    if k < 0 or k > n:
        return -float('inf')
    log_comb = math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
    return log_comb - n * math.log(2)

def probability(n, k):
    log_p = log_probability(n, k)
    return math.exp(log_p) if log_p > -700 else 0.0

# Microscopic calculations for Table 1
P_30_micro = probability(N_micro, 30)
P_max_micro = probability(N_micro, k_eq)
sum_c_micro = sum(probability(N_micro, k) for k in range(k_eq - 10, k_eq + 11))
sum_d_micro = sum(probability(N_micro, k) for k in range(k_eq - 20, k_eq + 21))

# Entropy changes (Delta S / k_B = ln(P_final / P_initial))
deltaS_e_micro = math.log(probability(N_micro, k_eq + 25) / P_max_micro)
deltaS_f_micro = math.log(probability(N_micro, k_eq + 10) / P_max_micro)
deltaS_g_micro = math.log(probability(N_micro, 20) / P_max_micro) # from N/2 to k=20 -> log(P(20)/P(61)) or vice versa

# Waiting time for k = 8
P_8 = probability(N_micro, 8)
t_wait_micro = 1.0 / (P_8 * N_micro)

# Likelihood ratios
ratio_33_micro = P_max_micro / probability(N_micro, 33)
ratio_window_micro = P_max_micro / probability(N_micro, k_eq - 10)

print("\n--- MICROSCOPIC RESULTS (N = 123) ---")
print(f"(a) P_30: {P_30_micro:.5e}")
print(f"(b) P_N/2 (P_61): {P_max_micro:.5e}")
print(f"(c) Sum P(N/2 ± 10): {sum_c_micro:.5f}")
print(f"(d) Sum P(N/2 ± 20): {sum_d_micro:.5f}")
print(f"(e) ΔS/k_B (N/2 + 25 -> N/2): {deltaS_e_micro:.2f}")
print(f"(f) ΔS/k_B (N/2 + 10 -> N/2): {deltaS_f_micro:.2f}")
print(f"(g) ΔS/k_B (N/2 to 20): {-deltaS_g_micro:.2f}") # Magnitude from N/2 to 20
print(f"(h) Waiting time for k=8: {t_wait_micro:.5e} s")
print(f"(i) Ratio P(N/2) / P(33): {ratio_33_micro:.5e}")
print(f"(i*) Ratio P(N/2) / P(N/2 ± 10): {ratio_window_micro:.2f}")



# PART 2: MACROSCOPIC SYSTEM (N = 1e23)
N_macro = 1e23
sigma_macro = math.sqrt(N_macro) / 2.0

# (a) P_30 for macroscopic N (approximate via log10)
# log10(P_30) ≈ 30*log10(N) - log10(30!) - N*log10(2)
log10_P_30_macro = 30 * math.log10(N_macro) - math.lgamma(31)/math.log(10) - N_macro * math.log10(2)

# (b) P_N/2 Gaussian peak height
P_max_macro = math.sqrt(2 / (math.pi * N_macro))

# (c) & (d) Cumulative windows (discrete states * peak height in macroscopic limit)
prob_c_macro = 21 * P_max_macro
prob_d_macro = 41 * P_max_macro

# (e) & (f) Entropy changes Delta S / k_B ≈ -2 * x^2 / N
deltaS_e_macro = -2 * (25**2) / N_macro
deltaS_f_macro = -2 * (10**2) / N_macro

# (g) Delta S between maximum disorder and k=20 (extensive deviation)
deltaS_g_macro = N_macro * math.log(2)

# (h) Waiting time for k=8 (log10 seconds)
log10_T_wait_macro = N_macro * math.log10(2)

# (i) Likelihood ratios
log10_Ratio_M_macro = N_macro * math.log10(2)
ratio_eq_macro = math.exp(2 * (10**2) / N_macro)

print("\n--- MACROSCOPIC RESULTS (N = 1e23) ---")
print(f"(a) log10(P_30): {log10_P_30_macro:.2e}")
print(f"(b) P_N/2: {P_max_macro:.2e}")
print(f"(c) Sum P(N/2 ± 10): {prob_c_macro:.2e}")
print(f"(d) Sum P(N/2 ± 20): {prob_d_macro:.2e}")
print(f"(e) ΔS/k_B (N/2 + 25 -> N/2): {deltaS_e_macro:.2e}")
print(f"(f) ΔS/k_B (N/2 + 10 -> N/2): {deltaS_f_macro:.2e}")
print(f"(g) ΔS/k_B (N/2 to 20): {deltaS_g_macro:.2e}")
print(f"(h) log10(T_wait for k=8): {log10_T_wait_macro:.2e} s")
print(f"(i) log10(Ratio P(N/2)/P(33)): {log10_Ratio_M_macro:.2e}")
print(f"(i*) Ratio P(N/2)/P(N/2 ± 10): 1 + {ratio_eq_macro - 1:.2e}")
print("=" * 60)