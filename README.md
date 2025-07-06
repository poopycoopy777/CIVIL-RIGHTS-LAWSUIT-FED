# CIVIL-RIGHTS-LAWSUIT-FED

This repository contains documents related to an ongoing civil rights case. The scripts in the `scripts/` directory help build a local legal research assistant using a 7B language model.

## Preparing a Dataset
Extract text from the PDFs in this repository and save them as a JSONL file:

```bash
python scripts/build_dataset.py . dataset.jsonl
```

## Training a 7B Model
Fine-tune a 7B base model (for example `mistralai/Mistral-7B-v0.1`) on the dataset:

```bash
python scripts/train_llm.py dataset.jsonl --output_dir my_model
```

This uses the HuggingFace `transformers` library and expects a GPU such as an RTX 3060.

## Building a Retrieval System
Create a simple FAISS index for retrieval-augmented generation:

```bash
python scripts/setup_rag.py dataset.jsonl --persist_dir index
```

You can then load the index with your fine-tuned model to answer questions about the case documents.

## Fetching Colorado Caselaw
Use the CourtListener API to download opinions for Colorado courts and store them as JSONL:

```bash
python scripts/fetch_caselaw.py opinions.jsonl --court colo --page_size 100
```

Provide an API key with `--api_key` if your requests require authentication.

## Extracting IPs from Logs
The `parse_log.py` script finds all IPv4 addresses in a log file:

```bash
python scripts/parse_log.py path/to/logfile.log
```

This can help identify network activity related to your case documents.
