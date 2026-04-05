#!/usr/bin/env python3
# Creates heatmap based on identity_enforcement csv 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

CSV_PATH = "identity_enforcement.csv"

df = pd.read_csv(CSV_PATH)


for c in ["signing_success", "verification_success", "rekor_entry_present"]:
    df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)

# -----------------------------
# figure 1 evidence availability heatmap
# -----------------------------
summary = df.groupby("scenario")[["signing_success", "verification_success", "rekor_entry_present"]].mean()

preferred = ["control", "no_oidc_token", "identity_mismatch_rejected"]
order = [s for s in preferred if s in summary.index] + [s for s in summary.index if s not in preferred]
summary = summary.loc[order]

mat = summary.to_numpy()

plt.figure(figsize=(8.5, 3.5))
#im = plt.imshow(mat, aspect="auto")
im = plt.imshow(mat, aspect="auto", cmap="Blues")
plt.colorbar(im, label="Proportion (0–1)")

plt.xticks(
    range(mat.shape[1]),
    ["Signing success", "Verification success", "Rekor evidence present"],
    rotation=15, ha="right"
)
plt.yticks(range(mat.shape[0]), summary.index)

# Annotate cells
for i in range(mat.shape[0]):
    for j in range(mat.shape[1]):
        plt.text(j, i, f"{mat[i, j]:.2f}", ha="center", va="center", fontsize=10)

plt.title("Evidence Availability by Identity Scenario")
plt.tight_layout()
plt.savefig("Figure_5_3_3_heatmap.png", dpi=300, bbox_inches="tight")
plt.show()

# -----------------------------
# figure 2 enforcement stability curve
# -----------------------------
unauth = df[df["scenario"] != "control"].copy()

# Deterministic ordering so the curve is reproducible
if "trial" in unauth.columns:
    unauth["trial"] = pd.to_numeric(unauth["trial"], errors="coerce").fillna(0).astype(int)
    unauth = unauth.sort_values(["trial", "scenario"]).reset_index(drop=True)
else:
    unauth = unauth.reset_index(drop=True)

# Blocked if either signing OR verification fails
unauth["blocked"] = ((unauth["signing_success"] == 0) | (unauth["verification_success"] == 0)).astype(int)

blocked = unauth["blocked"].to_numpy()
x = np.arange(1, len(blocked) + 1)
cum_rate = np.cumsum(blocked) / x

plt.figure(figsize=(8, 4))
plt.plot(x, cum_rate, marker="o", linestyle="-")
plt.ylim(0, 1.05)
plt.xlabel("Unauthorised attempt index")
plt.ylabel("Cumulative block rate")
plt.title("Stability of Identity Enforcement Across Unauthorised Attempts")
plt.grid(True, linestyle="--", linewidth=0.5)

if len(cum_rate) > 0:
    plt.text(x[-1], cum_rate[-1], f"  final={cum_rate[-1]:.2f}", va="center")

plt.tight_layout()
plt.savefig("Figure_5_3_3_stability.png", dpi=300, bbox_inches="tight")
plt.show()

total = len(df)
control_n = len(df[df["scenario"] == "control"])
unauth_n = len(df[df["scenario"] != "control"])

blocked_count = int(unauth["blocked"].sum())
block_rate = (blocked_count / unauth_n) if unauth_n else float("nan")

print("\n=== Identity Enforcement Headline Metrics ===")
print(f"Total records: {total}")
print(f"Control records: {control_n}")
print(f"Unauthorised records: {unauth_n}")
print(f"Unauthorised blocked: {blocked_count}")
print(f"Unauthorised block rate: {block_rate:.3f}")
