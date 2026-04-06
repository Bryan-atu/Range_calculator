#!/usr/bin/env python3
import os
import json
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

SBOM_DIR = "/home/bgleeson/signed-build/data/sbom_runs"
SBOM_FILES = sorted(glob.glob(os.path.join(SBOM_DIR, "sbom.spdx_*.json")))

if not SBOM_FILES:
    raise SystemExit("No SBOM files found in /data/sbom_runs (expected sbom.spdx_*.json)")

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_component_set(sbom):
    """
    Build a stable component set for comparison across runs.
    Use SPDX packages[].name + files[].fileName(basename).
    """
    comps = set()

    for pkg in sbom.get("packages", []) or []:
        n = pkg.get("name")
        if n:
            comps.add(f"pkg:{str(n).strip()}")

    for fl in sbom.get("files", []) or []:
        fn = fl.get("fileName")
        if fn:
            comps.add(f"file:{os.path.basename(str(fn).strip())}")

    return comps

def jaccard(a, b):
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)

rows = []
component_sets = []

# Load all SBOMs and compute core metrics
for idx, path in enumerate(SBOM_FILES, start=1):
    sbom = load_json(path)

    valid = int(("spdxVersion" in sbom) and ("SPDXID" in sbom) and ("packages" in sbom))

    packages = sbom.get("packages", []) or []
    files = sbom.get("files", []) or []
    rels = sbom.get("relationships", []) or []

    comps = extract_component_set(sbom)
    component_sets.append(comps)

    rows.append({
        "run": idx,
        "sbom_file": os.path.basename(path),
        "valid": valid,
        "package_count": len(packages),
        "file_count": len(files),
        "relationship_count": len(rels),
        "component_set_size": len(comps)
    })

df = pd.DataFrame(rows)

# Define baseline from run 1 and compute similarity
baseline = component_sets[0]
similarities = [jaccard(baseline, s) for s in component_sets]
df["baseline_jaccard"] = similarities

# Save metrics
df.to_csv("sbom_metrics_5_3_4.csv", index=False)

print("=== SBOM Metrics Summary ===")
print(df)

# Structural stability over runs
plt.figure(figsize=(8,4))
plt.plot(df["run"].to_numpy(), df["package_count"].to_numpy(), marker="o", linestyle="-", label="Packages")
plt.plot(df["run"].to_numpy(), df["file_count"].to_numpy(), marker="s", linestyle="-", label="Files")
plt.plot(df["run"].to_numpy(), df["relationship_count"].to_numpy(), marker="^", linestyle="-", label="Relationships")

plt.xlabel("Pipeline run")
plt.ylabel("Count")
plt.title("SBOM Structural Stability Across Pipeline Runs")
plt.grid(True, axis="y", linestyle="--", linewidth=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("Figure_5_3_4A_SBOM_Structural_Stability.png", dpi=300, bbox_inches="tight")
plt.show()

plt.figure(figsize=(8,4))
plt.plot(df["run"].to_numpy(), df["baseline_jaccard"].to_numpy(), marker="o", linestyle="-")
plt.ylim(0, 1.05)
plt.xlabel("Pipeline run")
plt.ylabel("Jaccard similarity vs run 1")
plt.title("SBOM Component-Set Consistency Across Runs (Baseline Similarity)")
plt.grid(True, axis="y", linestyle="--", linewidth=0.5)
plt.tight_layout()
plt.savefig("Figure_5_3_4B_SBOM_Baseline_Similarity.png", dpi=300, bbox_inches="tight")
plt.show()

# stats
print("\n=== Dissertation statistics ===")
print(f"Runs (n): {len(df)}")
print(f"SBOM validation pass rate: {df['valid'].mean():.2f}")
print(f"Package count: mean={df['package_count'].mean():.2f}, std={df['package_count'].std(ddof=1):.2f}, IQR={(df['package_count'].quantile(0.75)-df['package_count'].quantile(0.25)):.2f}")
print(f"File count: mean={df['file_count'].mean():.2f}, std={df['file_count'].std(ddof=1):.2f}, IQR={(df['file_count'].quantile(0.75)-df['file_count'].quantile(0.25)):.2f}")
print(f"Relationship count: mean={df['relationship_count'].mean():.2f}, std={df['relationship_count'].std(ddof=1):.2f}, IQR={(df['relationship_count'].quantile(0.75)-df['relationship_count'].quantile(0.25)):.2f}")
print(f"Baseline similarity (Jaccard): mean={df['baseline_jaccard'].mean():.3f}, std={df['baseline_jaccard'].std(ddof=1):.3f}, min={df['baseline_jaccard'].min():.3f}")
