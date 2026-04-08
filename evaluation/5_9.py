import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = {
    "Evidence Type": [
        "Artifact hash",
        "Signature",
        "Rekor UUID",
        "SBOM",
        "SBOM attestation",
        "Traceability report"
    ],
    "Baseline": [1, 0, 0, 0, 0, 0],
    "Enhanced": [1, 1, 1, 1, 1, 1]
}

df = pd.DataFrame(data)
df.set_index("Evidence Type", inplace=True)

matrix = df.values

plt.figure(figsize=(7,4))

heatmap = plt.imshow(matrix, cmap="RdYlGn", aspect="auto")

plt.colorbar(label="Evidence Present (1=yes, 0=no)")

plt.xticks(
    range(len(df.columns)),
    df.columns
)

plt.yticks(
    range(len(df.index)),
    df.index
)

for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        plt.text(j, i, str(matrix[i, j]),
                 ha="center",
                 va="center",
                 fontsize=11)

plt.title("Baseline vs Enhanced CI Pipeline Evidence Coverage")

plt.tight_layout()

plt.savefig("Figure_5_9_pipeline_evidence_heatmap.png", dpi=300)
plt.show()
