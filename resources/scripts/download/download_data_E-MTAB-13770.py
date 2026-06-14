# Heading 1 (Broad context / Top-level block / Script section)
# Targeted data ingestion script for E-MTAB-13770 EBI repository.

import os
from pathlib import Path
import urllib.request
from OmniPhysiBoSS.utils.logger import get_custom_logger

logger = get_custom_logger(__name__)

# Base URL for EBI FTP
BASE_URL = "https://ftp.ebi.ac.uk/biostudies/fire/E-MTAB-/770/E-MTAB-13770/Files/"

# official site:
# https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-13770


# Complete list of files extracted from EBI directory listing
FILE_LIST = [
    "E-MTAB-13770.idf.txt", "E-MTAB-13770.sdrf.txt", "genes.tsv",
    "P11_PBMC.loom", "P11_PBMC_barcodes.tsv", "P11_PBMC_matrix.mtx",
    "P11_digest_CD45pos.loom", "P11_digest_CD45pos_barcodes.tsv", "P11_digest_CD45pos_matrix.mtx",
    "P12_PBMC.loom", "P12_PBMC_barcodes.tsv", "P12_PBMC_matrix.mtx",
    "P12_digest_CD45pos.loom", "P12_digest_CD45pos_barcodes.tsv", "P12_digest_CD45pos_matrix.mtx",
    "P13_PBMC.loom", "P13_PBMC_barcodes.tsv", "P13_PBMC_matrix.mtx",
    "P13_digest_CD45pos.loom", "P13_digest_CD45pos_barcodes.tsv", "P13_digest_CD45pos_matrix.mtx",
    "P29_PBMC.loom", "P29_PBMC_barcodes.tsv", "P29_PBMC_matrix.mtx",
    "P29_digest_CD45pos.loom", "P29_digest_CD45pos_barcodes.tsv", "P29_digest_CD45pos_matrix.mtx",
    "P33_PBMC.loom", "P33_PBMC_barcodes.tsv", "P33_PBMC_matrix.mtx",
    "P33_digest_CD45pos.loom", "P33_digest_CD45pos_barcodes.tsv", "P33_digest_CD45pos_matrix.mtx",
    "P34_PBMC.loom", "P34_PBMC_barcodes.tsv", "P34_PBMC_matrix.mtx",
    "P34_digest_CD45pos.loom", "P34_digest_CD45pos_barcodes.tsv", "P34_digest_CD45pos_matrix.mtx",
    "P38_PBMC.loom", "P38_PBMC_barcodes.tsv", "P38_PBMC_matrix.mtx",
    "P38_digest_CD45pos.loom", "P38_digest_CD45pos_barcodes.tsv", "P38_digest_CD45pos_matrix.mtx",
    "P40_PBMC.loom", "P40_PBMC_barcodes.tsv", "P40_PBMC_matrix.mtx",
    "P40_digest_CD45pos.loom", "P40_digest_CD45pos_barcodes.tsv", "P40_digest_CD45pos_matrix.mtx",
    "P43_PBMC.loom", "P43_PBMC_barcodes.tsv", "P43_PBMC_matrix.mtx",
    "P43_digest_2_CD45pos.loom", "P43_digest_2_CD45pos_barcodes.tsv", "P43_digest_2_CD45pos_matrix.mtx",
    "P43_digest_CD45pos.loom", "P43_digest_CD45pos_barcodes.tsv", "P43_digest_CD45pos_matrix.mtx",
    "P63_PBMC.loom", "P63_PBMC_barcodes.tsv", "P63_PBMC_matrix.mtx",
    "P63_digest_CD45pos.loom", "P63_digest_CD45pos_barcodes.tsv", "P63_digest_CD45pos_matrix.mtx",
    "P64_PBMC.loom", "P64_PBMC_barcodes.tsv", "P64_PBMC_matrix.mtx",
    "P64_digest_2_CD45pos.loom", "P64_digest_2_CD45pos_barcodes.tsv", "P64_digest_2_CD45pos_matrix.mtx",
    "P64_digest_CD45pos.loom", "P64_digest_CD45pos_barcodes.tsv", "P64_digest_CD45pos_matrix.mtx",
    "P67_PBMC.loom", "P67_PBMC_barcodes.tsv", "P67_PBMC_matrix.mtx",
    "P67_digest_2_CD45pos.loom", "P67_digest_2_CD45pos_barcodes.tsv", "P67_digest_2_CD45pos_matrix.mtx",
    "P67_digest_CD45pos.loom", "P67_digest_CD45pos_barcodes.tsv", "P67_digest_CD45pos_matrix.mtx",
    "P68_PBMC.loom", "P68_PBMC_barcodes.tsv", "P68_PBMC_matrix.mtx",
    "P68_digest_CD45pos.loom", "P68_digest_CD45pos_barcodes.tsv", "P68_digest_CD45pos_matrix.mtx",
    "P69_digest_CD45pos.loom", "P69_digest_CD45pos_barcodes.tsv", "P69_digest_CD45pos_matrix.mtx",
    "P72_PBMC.loom", "P72_PBMC_barcodes.tsv", "P72_PBMC_matrix.mtx",
    "P72_digest_CD45pos.loom", "P72_digest_CD45pos_barcodes.tsv", "P72_digest_CD45pos_matrix.mtx",
    "P77_digest_CD45pos.loom", "P77_digest_CD45pos_barcodes.tsv", "P77_digest_CD45pos_matrix.mtx",
    "P79_PBMC.loom", "P79_PBMC_barcodes.tsv", "P79_PBMC_matrix.mtx",
    "P79_digest_2_CD45pos.loom", "P79_digest_2_CD45pos_barcodes.tsv", "P79_digest_2_CD45pos_matrix.mtx",
    "P79_digest_CD45pos.loom", "P79_digest_CD45pos_barcodes.tsv", "P79_digest_CD45pos_matrix.mtx",
    "P82_PBMC.loom", "P82_PBMC_barcodes.tsv", "P82_PBMC_matrix.mtx",
    "P82_digest_CD45pos_and_CD45neg.loom", "P82_digest_CD45pos_and_CD45neg_barcodes.tsv", "P82_digest_CD45pos_and_CD45neg_matrix.mtx",
    "P83_PBMC.loom", "P83_PBMC_barcodes.tsv", "P83_PBMC_matrix.mtx",
    "P83_digest_CD45pos.loom", "P83_digest_CD45pos_barcodes.tsv", "P83_digest_CD45pos_matrix.mtx",
    "P86_PBMC.loom", "P86_PBMC_barcodes.tsv", "P86_PBMC_matrix.mtx",
    "P86_digest_CD45pos.loom", "P86_digest_CD45pos_barcodes.tsv", "P86_digest_CD45pos_matrix.mtx",
    "P87_PBMC.loom", "P87_PBMC_barcodes.tsv", "P87_PBMC_matrix.mtx",
    "P87_digest_CD45pos.loom", "P87_digest_CD45pos_barcodes.tsv", "P87_digest_CD45pos_matrix.mtx",
    "P91_PBMC.loom", "P91_PBMC_barcodes.tsv", "P91_PBMC_matrix.mtx",
    "P91_digest_CD45pos.loom", "P91_digest_CD45pos_barcodes.tsv", "P91_digest_CD45pos_matrix.mtx"
]

def download_files(target_dir: str):
    """Iterate and download the file list."""
    os.makedirs(target_dir, exist_ok=True)
    for filename in FILE_LIST:
        dest = os.path.join(target_dir, filename)
        if not os.path.exists(dest):
            logger.info("Fetching: %s", filename)
            url = f"{BASE_URL}{filename}"
            urllib.request.urlretrieve(url, dest)
        else:
            logger.debug("File %s already exists, skipping.", filename)

if __name__ == "__main__":
    output_path = Path("../../../data/data_E-MTAB-13770/")
    os.mkdir(output_path.parent)
    download_files("../../../data/data_E-MTAB-13770/")