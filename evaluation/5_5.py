import pandas as pd
import matplotlib.pyplot as plt

CSV_FILE = "sbom_attestation_metrics.csv"

# Load CSV

df = pd.read_csv(CSV_FILE)

required = {
    "run",
    "attestation_verified",
    "rekor_entry_present",
    "verification_latency_ms",
    "rekor_uuid",
    "failure_reason",
}
missing = required - set(df.columns)
if missing:
    raise SystemExit(f"CSV missing required columns: {sorted(missing)}")

# Ensure types
df["run"] = pd.to_numeric(df["run"], errors="coerce")
df["attestation_verified"] = pd.to_numeric(df["attestation_verified"], errors="coerce").fillna(0).astype(int)
df["rekor_entry_present"] = pd.to_numeric(df["rekor_entry_present"], errors="coerce").fillna(0).astype(int)
df["verification_latency_ms"] = pd.to_numeric(df["verification_latency_ms"], errors="coerce")

n = len(df)
lat = df["verification_latency_ms"].dropna()


# Summary stats

p95 = lat.quantile(0.95)
q1 = lat.quantile(0.25)
q3 = lat.quantile(0.75)
iqr = q3 - q1

attest_rate = df["attestation_verified"].mean() * 100
rekor_rate = df["rekor_entry_present"].mean() * 100

uuid_unique = df["rekor_uuid"].nunique(dropna=True)
uuid_stability = (1.0 if uuid_unique == 1 else 0.0) * 100

print("=== SBOM Attestation Integrity (Test 5) Summary ===")
print(f"runs (n): {n}")
print(f"attestation verification rate: {attest_rate:.1f}%")
print(f"rekor inclusion rate: {rekor_rate:.1f}%")
print(f"latency mean: {lat.mean():.2f} ms")
print(f"latency std dev: {lat.std(ddof=1):.2f} ms")
print(f"latency median: {lat.median():.2f} ms")
print(f"latency IQR: {iqr:.2f} ms")
print(f"latency p95: {p95:.2f} ms")
print(f"latency min/max: {lat.min():.2f}/{lat.max():.2f} ms")
print(f"rekor UUIDs unique: {uuid_unique}")
print(f"rekor UUID stability (all identical?): {uuid_stability:.0f}%")

# Evidence rates (attestation + rekor inclusion)
plt.figure(figsize=(6, 3))

labels = ["Attestation verified", "Rekor entry present"]
values = [attest_rate, rekor_rate]

plt.barh(labels, values)
plt.xlim(0, 100)
plt.xlabel("Rate (%)")
plt.title("SBOM Attestation Evidence Rates Across Runs")
plt.grid(True, axis="x", linestyle="--", linewidth=0.5)

for i, v in enumerate(values):
    plt.text(v + 1, i, f"{v:.0f}%", va="center", fontsize=9)

plt.tight_layout()
plt.savefig("Figure_5_2_5B_Evidence_Rates.png", dpi=300, bbox_inches="tight")
plt.show()
