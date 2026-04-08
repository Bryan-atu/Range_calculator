import matplotlib.pyplot as plt
import numpy as np

# Runtime data 
typical = [19, 18, 28, 20, 20, 19, 19, 20, 23, 17, 20, 23, 18]
enhanced = [127, 141, 99, 104, 128, 108, 108, 102, 91, 129, 122]

# Figure 5.10 - Runtime distribution comparison

fig, ax = plt.subplots(figsize=(8, 4.5))

ax.boxplot(typical, positions=[1], widths=0.5, showfliers=True)
ax.boxplot(enhanced, positions=[2], widths=0.5, showfliers=True)

x1 = np.ones(len(typical)) * 1
x2 = np.ones(len(enhanced)) * 2
ax.scatter(x1, typical, s=20, alpha=0.7)
ax.scatter(x2, enhanced, s=20, alpha=0.7)

ax.set_xticks([1, 2])
ax.set_xticklabels(["Typical pipeline", "Enhanced pipeline"])
ax.set_ylabel("Execution time (s)")
ax.set_title("Pipeline Runtime Distribution: Typical vs Enhanced", pad=15)
ax.grid(True, axis="y", linestyle="--", linewidth=0.5, alpha=0.5)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("Figure_5_10_Runtime_Distribution.png", dpi=300, bbox_inches="tight")
plt.show()

# Figure 5.11 - Per-run runtime comparison

fig, ax = plt.subplots(figsize=(8, 4.5))

ax.plot(
    np.arange(1, len(typical) + 1),
    np.array(typical, dtype=float),
    marker="o",
    linestyle="-",
    label="Typical pipeline"
)

ax.plot(
    np.arange(1, len(enhanced) + 1),
    np.array(enhanced, dtype=float),
    marker="s",
    linestyle="-",
    label="Enhanced pipeline"
)

ax.set_xlabel("Run number")
ax.set_ylabel("Execution time (s)")
ax.set_title("Pipeline Runtime by Run", pad=15)
ax.grid(True, axis="y", linestyle="--", linewidth=0.5, alpha=0.5)
ax.legend()

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("Figure_5_11_Runtime_By_Run.png", dpi=300, bbox_inches="tight")
plt.show()


def describe(name, values):
    arr = np.array(values, dtype=float)
    mean = arr.mean()
    std = arr.std(ddof=1)
    median = np.median(arr)
    q1 = np.quantile(arr, 0.25)
    q3 = np.quantile(arr, 0.75)
    var = arr.var(ddof=1)
    print(name)
    print(f"  n = {len(arr)}")
    print(f"  mean = {mean:.2f} s")
    print(f"  std = {std:.2f} s")
    print(f"  median = {median:.2f} s")
    print(f"  IQR = {q3 - q1:.2f} s")
    print(f"  variance = {var:.2f}")
    print()

describe("Typical pipeline", typical)
describe("Enhanced pipeline", enhanced)

typical_mean = np.mean(typical)
enhanced_mean = np.mean(enhanced)
overhead = (enhanced_mean - typical_mean) / typical_mean

print(f"Execution overhead = {overhead:.2f}x typical runtime increase")
