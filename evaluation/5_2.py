import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

CSV_PATH = "tamper_detection.csv"
OUT_DIR = Path("figures")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FIG_CONFUSION = OUT_DIR / "Figure_5_3_Confusion_Matrix.png"
FIG_STABILITY = OUT_DIR / "Figure_5_4_Detection_Stability.png"
FIG_FINGERPRINT = OUT_DIR / "Figure_5_5_Failure_Fingerprint.png"

# Load data
df = pd.read_csv(CSV_PATH)

required_cols = {"trial", "tamper_type", "verification_result", "error_snippet"}
missing = required_cols - set(df.columns)
if missing:
    raise ValueError(f"CSV is missing required columns: {sorted(missing)}")

# Ensure trial is numeric
df["trial"] = pd.to_numeric(df["trial"], errors="coerce")

# Expected outcomes...control should PASS, tamper should FAIL
df["expected"] = np.where(df["tamper_type"] == "none", "pass", "fail")
df["success"] = (df["verification_result"] == df["expected"]).astype(int)

# -------------------------
# Confusion matrix (Expected vs Observed)
# -------------------------
cm = pd.crosstab(df["expected"], df["verification_result"])

for col in ["pass", "fail"]:
    if col not in cm.columns:
        cm[col] = 0
cm = cm[["pass", "fail"]]

mat = cm.values

plt.figure(figsize=(6, 4.5))
plt.imshow(mat, cmap="Blues")
plt.colorbar(label="Count")

plt.xticks([0, 1], ["Observed PASS", "Observed FAIL"])
plt.yticks([0, 1], ["Expected PASS (Control)", "Expected FAIL (Tamper)"])

for i in range(mat.shape[0]):
    for j in range(mat.shape[1]):
        plt.text(j, i, str(mat[i, j]), ha="center", va="center")

plt.title("Verification Outcome Confusion Matrix (Control vs Tamper)")
plt.tight_layout()
plt.savefig(FIG_CONFUSION, dpi=300, bbox_inches="tight")
plt.close()

# -------------------------
# Stability across trials (success per scenario over time)
# -------------------------
order = ["none", "binary_modification", "bundle_missing", "bundle_substitution"]
order = [c for c in order if c in df["tamper_type"].unique()]

plt.figure(figsize=(8, 4.5))
for t in order:
    sub = df[df["tamper_type"] == t].sort_values("trial")
    x = sub["trial"].to_numpy()
    y = sub["success"].to_numpy()
    plt.plot(x, y, marker="o", linestyle="-", color="steelblue")
    #plt.plot(x, y, marker="o", linestyle="-", label=t)

plt.yticks([0, 1], ["Unexpected", "Expected"])
plt.ylim(-0.1, 1.1)
plt.xlabel("Trial number")
plt.ylabel("Outcome correctness")
plt.title("Tamper Detection Stability Across Trials")
#plt.grid(True, axis="y", linestyle="--", linewidth=0.5)
plt.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)
plt.legend(title="Scenario", loc="lower right")
plt.tight_layout()
plt.savefig(FIG_STABILITY, dpi=300, bbox_inches="tight")
plt.close()

# -------------------------
# Failure mode fingerprint (tamper_type x failure snippets)
# -------------------------
tamper = df[df["tamper_type"] != "none"].copy()

tamper["error_short"] = tamper["error_snippet"].astype(str).str.slice(0, 60)

counts = pd.crosstab(tamper["tamper_type"], tamper["error_short"])

if counts.shape[1] > 8:
    top_cols = counts.sum(axis=0).sort_values(ascending=False).head(8).index
    counts = counts[top_cols]

mat2 = counts.values

plt.figure(figsize=(9, 4.5))
plt.imshow(mat2, cmap="coolwarm", aspect="auto")
plt.colorbar(label="Count")

plt.yticks(range(len(counts.index)), counts.index)
plt.xticks(range(len(counts.columns)), counts.columns, rotation=25, ha="right")

for i in range(mat2.shape[0]):
    for j in range(mat2.shape[1]):
        plt.text(j, i, str(mat2[i, j]), ha="center", va="center", fontsize=9)

plt.xlabel("Failure mode (error snippet, truncated)")
plt.ylabel("Tamper scenario")
plt.title("Failure mode fingerprint by tamper scenario")
plt.tight_layout()
plt.savefig(FIG_FINGERPRINT, dpi=300, bbox_inches="tight")
plt.close()

print("Generated figures:")
print(f" - {FIG_CONFUSION}")
print(f" - {FIG_STABILITY}")
print(f" - {FIG_FINGERPRINT}")
