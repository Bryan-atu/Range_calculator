#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

CSV_FILE = "vulnerability_scan_metrics.csv"
OUT_DIR = Path("figures")
OUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(CSV_FILE)

df["detected"] = pd.to_numeric(df["detected"], errors="coerce").fillna(0)
df["false_negative"] = pd.to_numeric(df["false_negative"], errors="coerce").fillna(0)

# Figure 1: Detection Performance
detection_rate = df["detected"].mean()
false_negatives = df["false_negative"].sum()

plt.figure(figsize=(6,4))

labels = ["Detected Vulnerabilities", "False Negatives"]
values = [detection_rate, false_negatives]

plt.bar(labels, values)

plt.ylabel("Value")
plt.title("Vulnerability Detection Performance", pad=20)
plt.ylim(0, 1)

for i,v in enumerate(values):
    plt.text(i, v + 0.02, f"{v:.2f}", ha="center")

plt.tight_layout()

plt.savefig(OUT_DIR / "Figure_5_6_Vulnerability_Detection_Rate.png", dpi=300)
plt.show()


# Figure 2: Severity Distribution
severity_counts = df["severity"].value_counts()

plt.figure(figsize=(6,4))

severity_counts.plot(kind="bar")

plt.xlabel("Severity")
plt.ylabel("Number of Vulnerabilities")
plt.title("Detected Vulnerability Severity Distribution")

plt.tight_layout()

plt.savefig(OUT_DIR / "Figure_5_7_Vulnerability_Severity.png", dpi=300)
plt.show()

print("\n=== Vulnerability Detection Summary ===")
print("Detection rate:", detection_rate)
print("False negatives:", false_negatives)
print("Total vulnerabilities detected:", df["detected"].sum())
