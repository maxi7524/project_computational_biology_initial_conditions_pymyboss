#!/bin/bash

# Configuration
## Define paths and URLs
TARGET_URL="https://panglaodb.se/markers/PanglaoDB_markers_27_Mar_2020.tsv.gz"
OUTPUT_DIR="resources/databases"
OUTPUT_FILE="$OUTPUT_DIR/panglaoDB.tsv.gz"
EXTRACTED_FILE="$OUTPUT_DIR/panglaoDB.tsv"
LOG_FILE="resources/logs/download_panglaoDB.log"

# Initialization
## Ensure directory structures exist
mkdir -p "$OUTPUT_DIR"
mkdir -p "resources/logs"

# Logging setup
## Redirect output to log file for auditing
exec > >(tee -a "$LOG_FILE") 2>&1

# Execution
## Download file with User-Agent header to bypass 405 error
echo "[INFO] Starting download from %s" "$TARGET_URL"
wget --user-agent="Mozilla/5.0" -O "$OUTPUT_FILE" "$TARGET_URL"

## Validate file existence before decompression
if [ -f "$OUTPUT_FILE" ]; then
    ## Decompress the file
    echo "[INFO] Decompressing file to %s" "$EXTRACTED_FILE"
    gunzip -c "$OUTPUT_FILE" > "$EXTRACTED_FILE"
    
    ## Cleanup
    rm "$OUTPUT_FILE"
    echo "[INFO] Process completed successfully."
else
    echo "[ERROR] Download failed. File %s not found." "$OUTPUT_FILE"
    exit 1
fi