#### 📁 Estrutura do Projeto
```sh
proteome-filter-pipeline/
│
├── app/
│   ├── pipeline.py
│   ├── blast_utils.py
│   ├── download_utils.py
│   ├── clustering_utils.py
│   └── config.py
│
├── data/
│
├── results/
│
├── Dockerfile
├── requirements.txt
├── docker-compose.yml
└── README.md

```

#### ▶️ Como Executar

- Build
```sh
docker build -t proteome-pipeline .
```

- Run
```sh
docker run -v $(pwd)/data:/app/data \
           -v $(pwd)/results:/app/results \
           proteome-pipeline
```

- Ou com compose:
```sh
docker-compose up --build
```

#### 🧪 Resultado Esperado
```sh
results/
│
├── ecoli_vs_human.xml
├── ecoli_non_human.fasta
└── ecoli_nonredundant.fasta
```
