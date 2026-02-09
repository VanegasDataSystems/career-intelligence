This folder contains scripts for embedding job descriptions, running vector search,
and aggregating skills from search results.

- embed.py: generate and store job embeddings
- vector_search.py: append vector search results for queries
- skill_agg.py: aggregate skills for all stored searches
- verify_embedding.py: sanity checks for DuckDB embeddings

## Embedding Model Setup

This project uses the sentence-transformer model:
`sentence-transformers/all-MiniLM-L6-v2`.

Due to restricted network access, the model is downloaded manually and loaded
from a local directory.

Expected folder structure:

models/
  └── all-MiniLM-L6-v2/
      ├── config.json
      ├── pytorch_model.bin
      ├── tokenizer.json
      └── ...

The `models/` directory is not committed to Git.
If missing, download the model from:
https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2 ; or https://www.kaggle.com/datasets/sircausticmail/all-minilm-l6-v2zip, then extract and place it under `models/all-MiniLM-L6-v2/`.
