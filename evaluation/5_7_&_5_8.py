#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(".")
TRACE_CSV = BASE_DIR / "traceability_metrics.csv"
REPRO_CSV = BASE_DIR / "reproducibility_metrics.csv"
REPORTS_DIR = Path("/home/bgleeson/signed-build/traceability-reports")

OUT_DIR = BASE_DIR / "figures"
OUT_DIR.mkdir(exist_ok=True)

trace_df = pd.read_csv(TRACE_CSV)
repro_df = pd.read_csv(REPRO_CSV)


trace_cols = [
    "commit_match",
    "artifact_hash_match",
    "rekor_uuid_present",
    "rekor_uuid_match",
    "bundle_present",
    "sbom_present",
    "workflow_metadata_present",
]

for c in trace_cols:
    trace_df[c] = pd.to_numeric(trace_df[c], errors="coerce").fillna(0).astype(int)

if "ecs" not in trace_df.columns:
    trace_df["ecs"] = trace_df[trace_cols].sum(axis=1) / len(trace_cols)
else:
    trace_df["ecs"] = pd.to_numeric(trace_df["ecs"], errors="coerce")

metadata_cols = ["commit_match", "artifact_hash_match", "rekor_uuid_match", "workflow_metadata_present"]
if "metadata_consistency_rate" not in trace_df.columns:
    trace_df["metadata_consistency_rate"] = trace_df[metadata_cols].sum(axis=1) / len(metadata_cols)
else:
    trace_df["metadata_consistency_rate"] = pd.to_numeric(
        trace_df["metadata_consistency_rate"], errors="coerce"
    )

trace_df["rekor_reference_validity"] = trace_df["rekor_uuid_match"]

repro_df["artifact_sha256"] = repro_df["artifact_sha256"].astype(str)
repro_df["rekor_uuid"] = repro_df["rekor_uuid"].astype(str)

# Independent run reproducibility logic
unique_hashes = repro_df["artifact_sha256"].nunique()
total_runs = len(repro_df)

# All rows get the same reproducibility result based on global consistency
if unique_hashes == 1:
    repro_df["reproducibility_rate"] = 1.0
    repro_df["artifact_hash_determinism"] = 1.0
    repro_df["hash_match_global"] = 1
else:
    repro_df["reproducibility_rate"] = (total_runs - (unique_hashes - 1)) / total_runs
    repro_df["artifact_hash_determinism"] = 1.0 / unique_hashes
    most_common_hash = repro_df["artifact_sha256"].mode().iloc[0]
    repro_df["hash_match_global"] = (repro_df["artifact_sha256"] == most_common_hash).astype(int)

unique_rekor = repro_df["rekor_uuid"].nunique()

repro_df.to_csv("reproducibility_metrics_enriched.csv", index=False)


# Traceability completeness heatmap
trace_labels = [
    "Commit SHA",
    "Artifact hash",
    "Rekor present",
    "Rekor match",
    "Bundle present",
    "SBOM present",
    "Workflow metadata",
]

trace_matrix = trace_df[trace_cols].to_numpy()

plt.figure(figsize=(9, 4.5))
im = plt.imshow(trace_matrix, aspect="auto", cmap="RdYlGn", vmin=0, vmax=1)
cbar = plt.colorbar(im)
cbar.set_label("Verified field (1=yes, 0=no)")

plt.xticks(range(len(trace_labels)), trace_labels, rotation=25, ha="right")
plt.yticks(range(len(trace_df)), [f"Run {r}" for r in trace_df["run"]])

for i in range(trace_matrix.shape[0]):
    for j in range(trace_matrix.shape[1]):
        plt.text(j, i, str(int(trace_matrix[i, j])), ha="center", va="center", fontsize=9)

plt.title("Traceability Evidence Completeness Across Independent Runs", pad=12)
plt.tight_layout()
plt.savefig(OUT_DIR / "Figure_5_2_7A_Traceability_Heatmap.png", dpi=300, bbox_inches="tight")
plt.show()

# Rekor UUID uniqueness and validity
valid_rekor_matches = int(trace_df["rekor_reference_validity"].sum())

labels = ["Unique Rekor UUIDs", "Valid report-to-Rekor matches"]
values = [unique_rekor, valid_rekor_matches]

plt.figure(figsize=(6.8, 4.2))
plt.bar(labels, values)
plt.ylabel("Count")
plt.title("Rekor UUID Uniqueness and Traceability Report Validity", pad=12)
plt.grid(True, axis="y", linestyle="--", linewidth=0.5, alpha=0.5)

for i, v in enumerate(values):
    plt.text(i, v + 0.05, str(int(v)), ha="center", fontsize=10)

plt.tight_layout()
plt.savefig(OUT_DIR / "Figure_5_2_7B_Rekor_Uniqueness_and_Validity.png", dpi=300, bbox_inches="tight")
plt.show()


# Build reproducibility heatmap
repro_heatmap_cols = [
    "hash_match_global",
]

repro_heatmap_labels = [
    "Artifact hash match",
]

repro_matrix = repro_df[repro_heatmap_cols].to_numpy()

plt.figure(figsize=(5.2, 4.0))
im = plt.imshow(repro_matrix, aspect="auto", cmap="RdYlGn", vmin=0, vmax=1)
cbar = plt.colorbar(im)
cbar.set_label("Match (1=yes, 0=no)")

plt.xticks(range(len(repro_heatmap_labels)), repro_heatmap_labels)
plt.yticks(range(len(repro_df)), [f"Run {r}" for r in repro_df["run"]])

for i in range(repro_matrix.shape[0]):
    for j in range(repro_matrix.shape[1]):
        plt.text(j, i, str(int(repro_matrix[i, j])), ha="center", va="center", fontsize=9)

plt.title("Artifact Hash Reproducibility Across Independent Runs", pad=12)
plt.tight_layout()
plt.savefig(OUT_DIR / "Figure_5_2_8A_Reproducibility_Heatmap.png", dpi=300, bbox_inches="tight")
plt.show()


# Unique hash vs unique Rekor UUIDs

labels = ["Unique artifact hashes", "Unique Rekor UUIDs"]
values = [unique_hashes, unique_rekor]

plt.figure(figsize=(6.8, 4.2))
plt.bar(labels, values)
plt.ylabel("Count")
plt.title("Unique Identifiers Across Independent Builds", pad=12)
plt.grid(True, axis="y", linestyle="--", linewidth=0.5, alpha=0.5)

for i, v in enumerate(values):
    plt.text(i, v + 0.05, str(int(v)), ha="center", fontsize=10)

plt.tight_layout()
plt.savefig(OUT_DIR / "Figure_5_2_8B_Unique_Identifiers.png", dpi=300, bbox_inches="tight")
plt.show()

report_count = 0
if REPORTS_DIR.exists() and REPORTS_DIR.is_dir():
    report_count = len(list(REPORTS_DIR.glob("traceability_report_*.txt")))

print("\n=== Test 5.2.7 Summary ===")
print(f"Traceability runs analysed: {len(trace_df)}")
print(f"Traceability reports found: {report_count}")
print(f"Mean ECS: {trace_df['ecs'].mean():.3f}")
print(f"Mean metadata consistency rate: {trace_df['metadata_consistency_rate'].mean():.3f}")
print(f"Rekor reference validity: {trace_df['rekor_reference_validity'].mean():.3f}")

print("\n=== Test 5.2.8 Summary ===")
print(f"Reproducibility runs analysed: {len(repro_df)}")
print(f"Unique artifact hashes: {unique_hashes}")
print(f"Unique Rekor UUIDs: {unique_rekor}")
print(f"Reproducibility rate: {repro_df['reproducibility_rate'].iloc[0]:.3f}")
print(f"Artifact hash determinism: {repro_df['artifact_hash_determinism'].iloc[0]:.3f}")
