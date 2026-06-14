# AGENTS.md — proteomeFilterPipeline

## Quick start

```sh
# Build and run (Docker is the primary execution method)
docker build -t proteome-pipeline .
docker run -v $(pwd)/data:/app/data -v $(pwd)/results:/app/results proteome-pipeline

# Or with compose
docker-compose up --build
```

## Pipeline steps

1. Downloads _E. coli_ (UP000000625) and human (UP000005640) proteomes from UniProt REST API (`rest.uniprot.org`)
2. Builds a BLAST protein DB from human proteome (`makeblastdb -dbtype prot`)
3. Runs `blastp -outfmt 5` (XML output) — E. coli query vs human DB
4. Filters out E. coli proteins with BLAST hits (e-value < 0.005)
5. Clusters remaining sequences with CD-HIT at 80% identity (`-c 0.8 -n 5`)

## Architecture

- **Entrypoint:** `app/pipeline.py` — single script, no CLI args
- **Config:** `app/config.py` — proteome IDs, e-value threshold, CD-HIT identity, I/O paths
- **Modules:** `download_utils.py`, `blast_utils.py`, `clustering_utils.py`
- **Output:** `results/ecoli_vs_human.xml`, `ecoli_non_human.fasta`, `ecoli_nonredundant.fasta`

## Dependencies

- **System:** `ncbi-blast+`, `cd-hit`, `wget`
- **Python:** `biopython`, `requests`, `tqdm`

## Important notes

- No tests, no linting, no type checking — pure script pipeline
- Data directory `data/` and results directory `results/` are created automatically
- Works offline after initial download: inputs cached in `data/`
- Modify `app/config.py` to change targets or parameters (no CLI args)
