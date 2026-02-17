import os
from config import *
from download_utils import download_proteome
from blast_utils import make_blast_db, run_blast, filter_non_human
from clustering_utils import run_cdhit

def main():

    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)

    ecoli_fasta = f"{DATA_DIR}/ecoli.fasta"
    human_fasta = f"{DATA_DIR}/human.fasta"

    print("Downloading proteomes...")
    download_proteome(PROTEOME_ID, ecoli_fasta)
    download_proteome(HUMAN_PROTEOME_ID, human_fasta)

    print("Creating BLAST database...")
    make_blast_db(human_fasta, f"{DATA_DIR}/human_db")

    blast_xml = f"{RESULTS_DIR}/ecoli_vs_human.xml"

    print("Running BLASTp...")
    run_blast(ecoli_fasta, f"{DATA_DIR}/human_db", blast_xml, EVALUE_THRESHOLD)

    filtered_fasta = f"{RESULTS_DIR}/ecoli_non_human.fasta"

    print("Filtering homologs...")
    filter_non_human(blast_xml, ecoli_fasta, filtered_fasta, EVALUE_THRESHOLD)

    final_fasta = f"{RESULTS_DIR}/ecoli_nonredundant.fasta"

    print("Running CD-HIT...")
    run_cdhit(filtered_fasta, final_fasta, CDHIT_IDENTITY)

    print("Pipeline complete.")

if __name__ == "__main__":
    main()
