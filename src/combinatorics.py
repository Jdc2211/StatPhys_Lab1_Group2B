import matplotlib.pyplot as plt

def omega(N, k):
    if k == 0:
        return 1
    num, den = 1, 1
    for i in range(k):
        num *= (N - i)
        den *= (k - i)
    return num // den

for N in [20, 50, 80, 100]:
    k_vals = list(range(N + 1))
    probs = [omega(N, k) / (2**N) for k in k_vals]
    plt.plot(k_vals, probs, label=f"N = {N}")

plt.xlabel("k (Number of Heads)")
plt.ylabel("Probability P(k)")
plt.legend()
plt.grid(True)
plt.show()