### ▶️ Como Executar

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
