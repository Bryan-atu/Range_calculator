import matplotlib.pyplot as plt
import numpy as np

# Runtime data
typical = np.array([19, 18, 28, 20, 20, 19, 19, 20, 23, 17, 20, 23, 18], dtype=float)
enhanced = np.array([127, 141, 99, 104, 128, 108, 108, 102, 91, 129, 122], dtype=float)

typical_mean = typical.mean()
typical_median = np.median(typical)
typical_p95 = np.quantile(typical, 0.95)

enhanced_mean = enhanced.mean()
enhanced_median = np.median(enhanced)
enhanced_p95 = np.quantile(enhanced, 0.95)

metrics = ["Mean", "Median", "95th percentile"]
typ_vals = [typical_mean, typical_median, typical_p95]
enh_vals = [enhanced_mean, enhanced_median, enhanced_p95]

y = np.arange(len(metrics))

plt.figure(figsize=(8, 4.5))

for i in range(len(metrics)):
    plt.plot([typ_vals[i], enh_vals[i]], [y[i], y[i]], linewidth=2)

plt.scatter(typ_vals, y, s=60, label="Typical pipeline")
plt.scatter(enh_vals, y, s=60, label="Enhanced pipeline")

for i, v in enumerate(typ_vals):
    plt.text(v - 1.5, y[i] + 0.08, f"{v:.1f}s", ha="right", fontsize=9)

for i, v in enumerate(enh_vals):
    plt.text(v + 1.5, y[i] + 0.08, f"{v:.1f}s", ha="left", fontsize=9)

plt.yticks(y, metrics)
plt.xlabel("Execution time (s)")
plt.title("Pipeline Runtime Summary Comparison")
plt.grid(True, axis="x", linestyle="--", linewidth=0.5, alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("Figure_5_10A_Runtime_Dumbbell.png", dpi=300, bbox_inches="tight")
plt.show()

typical_z = (typical - typical.mean()) / typical.std(ddof=1)
enhanced_z = (enhanced - enhanced.mean()) / enhanced.std(ddof=1)

plt.figure(figsize=(8, 4.5))

x1 = np.ones(len(typical_z)) * 1
x2 = np.ones(len(enhanced_z)) * 2

plt.scatter(x1, typical_z, s=35, alpha=0.8, label="Typical pipeline")
plt.scatter(x2, enhanced_z, s=35, alpha=0.8, label="Enhanced pipeline")

plt.axhline(0, linestyle="--", linewidth=1)
plt.axhline(1, linestyle=":", linewidth=0.8)
plt.axhline(-1, linestyle=":", linewidth=0.8)
plt.axhline(2, linestyle=":", linewidth=0.8)
plt.axhline(-2, linestyle=":", linewidth=0.8)

plt.xticks([1, 2], ["Typical pipeline", "Enhanced pipeline"])
plt.ylabel("Runtime Z-score")
plt.title("Standardised Runtime Variability by Pipeline Type")
plt.grid(True, axis="y", linestyle="--", linewidth=0.5, alpha=0.5)
plt.tight_layout()
plt.savefig("Figure_5_10B_Runtime_ZScore.png", dpi=300, bbox_inches="tight")
plt.show()

def summarise(name, arr):
    print(name)
    print(f"  mean   = {arr.mean():.2f} s")
    print(f"  std    = {arr.std(ddof=1):.2f} s")
    print(f"  median = {np.median(arr):.2f} s")
    print(f"  IQR    = {(np.quantile(arr, 0.75) - np.quantile(arr, 0.25)):.2f} s")
    print(f"  p95    = {np.quantile(arr, 0.95):.2f} s")
    print()

summarise("Typical pipeline", typical)
summarise("Enhanced pipeline", enhanced)

overhead = (enhanced.mean() - typical.mean()) / typical.mean()
print(f"Execution overhead ratio = {overhead:.2f}x")
