#!/bin/bash

# Set target directory for the Cell Fate model
TARGET_DIR="data/maboss/CellFate"
mkdir -p "$TARGET_DIR"

# Define direct links to 10x Genomics data
H5_URL="https://cf.10xgenomics.com/samples/spatial-exp/1.1.0/V1_Breast_Cancer_Block_A_Section_1/V1_Breast_Cancer_Block_A_Section_1_filtered_feature_bc_matrix.h5"
SPATIAL_URL="https://cf.10xgenomics.com/samples/spatial-exp/1.1.0/V1_Breast_Cancer_Block_A_Section_1/V1_Breast_Cancer_Block_A_Section_1_spatial.tar.gz"

echo "=== Step 1/3: Downloading filtered HDF5 matrix ==="
# The -O flag allows renaming the file immediately to the name Scanpy looks for
wget -O "$TARGET_DIR/filtered_feature_bc_matrix.h5" "$H5_URL"

echo -e "\n=== Step 2/3: Downloading spatial data (images and coordinates) ==="
wget -O "$TARGET_DIR/spatial.tar.gz" "$SPATIAL_URL"

echo -e "\n=== Step 3/3: Extracting spatial data ==="
# The -C option extracts the archive directly inside the specified directory.
# The 10x Genomics archive already contains a directory named 'spatial'.
tar -xzf "$TARGET_DIR/spatial.tar.gz" -C "$TARGET_DIR"

# Cleanup - remove the compressed tar.gz archive as it is no longer needed
rm "$TARGET_DIR/spatial.tar.gz"

echo -e "\n[SUCCESS] Data has been successfully downloaded and structured in: $TARGET_DIR"