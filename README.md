# proteomeFilterPipeline

A bioinformatics pipeline that filters non-human proteins from _E. coli_ by removing BLAST homologs against the human proteome and clustering the remaining sequences with CD-HIT.

## Pipeline steps

1. **Download** — fetches _E. coli_ (UP000000625) and human (UP000005640) proteomes from the UniProt REST API
2. **BLAST database** — builds a protein BLAST database from the human proteome (`makeblastdb -dbtype prot`)
3. **BLASTp search** — runs `blastp` with E. coli as query against the human DB (XML output, `-outfmt 5`)
4. **Filter homologs** — removes E. coli proteins that have a BLAST hit below e-value 0.005
5. **CD-HIT clustering** — clusters remaining sequences at 80% identity (`-c 0.8 -n 5`) to remove redundancy

## Quick start

```sh
docker build -t proteome-pipeline .
docker run -v $(pwd)/data:/app/data -v $(pwd)/results:/app/results proteome-pipeline
```

Or with Docker Compose:

```sh
docker-compose up --build
```

## Output

```
results/
├── ecoli_vs_human.xml      — BLASTp results (XML)
├── ecoli_non_human.fasta   — E. coli proteins with no human homolog
└── ecoli_nonredundant.fasta — CD-HIT clustered (80% identity)
```

## Configuration

Edit `app/config.py` to change parameters (no CLI args):

| Variable | Default | Description |
|---|---|---|
| `PROTEOME_ID` | `UP000000625` | E. coli UniProt proteome ID |
| `HUMAN_PROTEOME_ID` | `UP000005640` | Human UniProt proteome ID |
| `EVALUE_THRESHOLD` | `0.005` | BLAST e-value cutoff |
| `CDHIT_IDENTITY` | `0.8` | CD-HIT sequence identity threshold |

## Local execution

Requires system packages `ncbi-blast+`, `cd-hit`, `wget` and Python packages from `requirements.txt`.

```sh
pip install -r requirements.txt
python app/pipeline.py
```

Data (`data/`) and results (`results/`) directories are created automatically. Input proteomes are cached after first download, so the pipeline works offline on subsequent runs.

## License

BSD 3-Clause — see [LICENSE](LICENSE).
