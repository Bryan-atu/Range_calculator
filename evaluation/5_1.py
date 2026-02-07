import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("verify_latency.csv")
lat = df["latency_ms"]

# Summary statistics
p95 = lat.quantile(0.95)
q1 = lat.quantile(0.25)
q3 = lat.quantile(0.75)
iqr = q3 - q1

print(f"n={len(lat)}")
print(f"mean={lat.mean():.2f} ms")
print(f"std={lat.std(ddof=1):.2f} ms")
print(f"median={lat.median():.2f} ms")
print(f"IQR={iqr:.2f} ms")
print(f"p95={p95:.2f} ms")
print(f"min={lat.min()} ms, max={lat.max()} ms")

x = [1 + (0.03 * ((i % 7) - 3)) for i in range(len(lat))]

# Full view
plt.figure(figsize=(7,4))

plt.boxplot(lat, vert=True, showfliers=True, widths=0.4)
plt.scatter(x, lat, s=20)

plt.axhline(p95, linestyle="--", linewidth=1)
plt.text(1.02, p95, f"95th percentile = {p95:.0f} ms", va="center")

plt.ylabel("Verification latency (ms)")
plt.xticks([1], [f"cosign verify-blob\n(n={len(lat)})"])
plt.title("Artifact Verification Latency Distribution (Full Range)")
plt.grid(True, axis="y", linestyle="--", linewidth=0.5)

plt.savefig("Figure_5_1_Full_Verification_Latency.png", dpi=300, bbox_inches="tight")
plt.show()


# Zoomed IQR view
plt.figure(figsize=(7,4))

plt.boxplot(lat, vert=True, showfliers=False, widths=0.4)
plt.scatter(x, lat, s=20)

lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr
plt.ylim(lower, upper)

plt.ylabel("Verification latency (ms)")
plt.xticks([1], [f"cosign verify-blob\n(n={len(lat)})"])
plt.title("Verification Latency")
plt.grid(True, axis="y", linestyle="--", linewidth=0.5)

plt.savefig("Figure_5_2_Zoomed_Verification_Latency.png", dpi=300, bbox_inches="tight")
plt.show()

