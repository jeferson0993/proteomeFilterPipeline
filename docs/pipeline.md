# Pipeline steps

The pipeline is orchestrated by `app/pipeline.py` and runs 5 sequential steps. Configuration is read from `app/config.py`.

---

## Step 1 — Download proteomes

**Module:** `app/download_utils.py` — `download_proteome()`

Fetches two FASTA files from the UniProt REST API:

```
https://rest.uniprot.org/uniprotkb/stream?format=fasta&query=proteome:{PROTEOME_ID}
```

| Input | Proteome ID | Output |
|---|---|---|
| _E. coli_ K-12 MG1655 | `UP000000625` | `data/ecoli.fasta` |
| Human | `UP000005640` | `data/human.fasta` |

Uses `requests.get()` and writes the response body directly as FASTA. No streaming or chunking.

**Caching:** If the files already exist in `data/`, they are overwritten. To avoid redundant downloads, run offline — delete the files to force a fresh download.

---

## Step 2 — Build BLAST database

**Module:** `app/blast_utils.py` — `make_blast_db()`

Runs `makeblastdb` on the human proteome:

```
makeblastdb -in data/human.fasta -dbtype prot -out data/human_db
```

Creates BLAST-formatted database files (`data/human_db.phr`, `data/human_db.pin`, `data/human_db.psq`, etc.) from the human FASTA.

Requires `ncbi-blast+` installed on the system.

---

## Step 3 — BLASTp search

**Module:** `app/blast_utils.py` — `run_blast()`

Runs `blastp` with E. coli sequences as query against the human database:

```
blastp -query data/ecoli.fasta -db data/human_db -out results/ecoli_vs_human.xml -outfmt 5 -evalue 0.005
```

Output format is **XML** (`-outfmt 5`) for programmatic parsing. The `-evalue` threshold is passed directly to BLAST to limit output size.

---

## Step 4 — Filter human homologs

**Module:** `app/blast_utils.py` — `filter_non_human()`

Parses the BLAST XML output with `Bio.SearchIO` and identifies every E. coli protein that has **any** HSP with e-value < 0.005 against the human database.

```python
for qresult in SearchIO.parse(blast_xml, "blast-xml"):
    for hit in qresult.hits:
        for hsp in hit.hsps:
            if hsp.evalue < evalue:
                proteins_with_hits.add(qresult.id)
```

Proteins with hits are removed. The remaining sequences are written to `results/ecoli_non_human.fasta` using `Bio.SeqIO`.

**Behavior:** If an E. coli protein has multiple HSPs, a single HSP below threshold is enough to exclude it. The threshold is applied a second time in Python (BLAST already used it at step 3, but the filter re-applies it for correctness).

---

## Step 5 — CD-HIT clustering

**Module:** `app/clustering_utils.py` — `run_cdhit()`

Runs CD-HIT to remove redundant sequences at 80% identity:

```
cd-hit -i results/ecoli_non_human.fasta -o results/ecoli_nonredundant.fasta -c 0.8 -n 5
```

| Flag | Value | Meaning |
|---|---|---|
| `-c` | `0.8` | Sequence identity threshold (80%) |
| `-n` | `5` | Word size (must be 5 for `-c >= 0.8`) |

Output is `results/ecoli_nonredundant.fasta`. A `.clstr` cluster file is also produced alongside the output.

---

## Output files

| File | Contents |
|---|---|
| `results/ecoli_vs_human.xml` | Raw BLASTp results (XML format, parsable by `Bio.SearchIO`) |
| `results/ecoli_non_human.fasta` | E. coli proteins with no significant similarity to human proteins |
| `results/ecoli_nonredundant.fasta` | CD-HIT clustered set at 80% identity (final output) |
