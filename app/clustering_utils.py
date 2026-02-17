import subprocess

def run_cdhit(input_fasta, output_fasta, identity):
    subprocess.run([
        "cd-hit",
        "-i", input_fasta,
        "-o", output_fasta,
        "-c", str(identity),
        "-n", "5"
    ], check=True)
