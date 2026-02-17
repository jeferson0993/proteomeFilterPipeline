import subprocess
from Bio import SearchIO
from Bio import SeqIO

def make_blast_db(fasta_file, db_name):
    subprocess.run([
        "makeblastdb",
        "-in", fasta_file,
        "-dbtype", "prot",
        "-out", db_name
    ], check=True)

def run_blast(query, db, output_xml, evalue):
    subprocess.run([
        "blastp",
        "-query", query,
        "-db", db,
        "-out", output_xml,
        "-outfmt", "5",
        "-evalue", str(evalue)
    ], check=True)

def filter_non_human(blast_xml, original_fasta, output_fasta, evalue):
    proteins_with_hits = set()

    for qresult in SearchIO.parse(blast_xml, "blast-xml"):
        for hit in qresult.hits:
            for hsp in hit.hsps:
                if hsp.evalue < evalue:
                    proteins_with_hits.add(qresult.id)

    filtered = [
        record for record in SeqIO.parse(original_fasta, "fasta")
        if record.id not in proteins_with_hits
    ]

    SeqIO.write(filtered, output_fasta, "fasta")
