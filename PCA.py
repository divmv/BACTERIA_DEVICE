# PCAAnalysis.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA, KernelPCA
from sklearn.preprocessing import StandardScaler
import time
import os

def run_pca(master_file_path):
    """
    Run PCA analysis on a master CSV file and plot the first 3 components in 3D.
    Produces two plots:
      - Linear PCA
      - Non-linear PCA (Kernel PCA with RBF kernel)
    """
    file_path = 'PlotData/PCA'
    if not os.path.exists(file_path):
        os.makedirs(file_path)
        print(f"Created directory: {file_path}")
    # Load the data
    if not os.path.isfile(master_file_path):
        print(f"File not found: {master_file_path}")
        return

    df = pd.read_csv(master_file_path)
    print(f"Loaded data shape: {df.shape}")

    # Optionally drop non-numeric columns
    numeric_df = df.select_dtypes(include=[np.number])
    print(f"Numeric columns used for PCA: {numeric_df.columns.tolist()}")

    # Standardize the data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(numeric_df)

    # ---------------- Linear PCA ----------------
    pca_linear = PCA(n_components=3)
    X_pca_linear = pca_linear.fit_transform(X_scaled)
    print("Linear PCA explained variance ratios:", pca_linear.explained_variance_ratio_)

    # Plot Linear PCA in 3D
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(
        X_pca_linear[:, 0],
        X_pca_linear[:, 1],
        X_pca_linear[:, 2],
        c='blue',
        s=20,
        alpha=0.7
    )
    ax.set_title("Linear PCA: First 3 Components")
    ax.set_xlabel("PCA1")
    ax.set_ylabel("PCA2")
    ax.set_zlabel("PCA3")
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    plot_filename_base = f"PCA_Linear_{timestamp}"
    plot_path = os.path.join(file_path, f"{plot_filename_base}.png")
    fig.savefig(plot_path) 

    # ---------------- Non-linear PCA (Kernel PCA) ----------------
    kpca = KernelPCA(n_components=3, kernel='rbf', gamma=0.1, fit_inverse_transform=True)
    X_kpca = kpca.fit_transform(X_scaled)

    # Plot Non-linear PCA in 3D
    fig2 = plt.figure(figsize=(10, 7))
    ax2 = fig2.add_subplot(111, projection='3d')
    ax2.scatter(
        X_kpca[:, 0],
        X_kpca[:, 1],
        X_kpca[:, 2],
        c='red',
        s=20,
        alpha=0.7
    )
    ax2.set_title("Non-linear PCA (Kernel PCA, RBF) First 3 Components")
    ax2.set_xlabel("KPC1")
    ax2.set_ylabel("KPC2")
    ax2.set_zlabel("KPC3")
    # plt.show()
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    plot_filename_base = f"PCA_NonLinear_{timestamp}"
    plot_path = os.path.join(file_path, f"{plot_filename_base}.png")
    fig.savefig(plot_path) 

    print("PCA analysis complete.")


# Example usage
if __name__ == "__main__":
    master_file = input("Enter path to master CSV file from Processor.py: ")
    run_pca(master_file)
