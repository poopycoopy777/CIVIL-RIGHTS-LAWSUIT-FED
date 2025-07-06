import os
import json
from pathlib import Path
from typing import List, Dict

import pdfplumber


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extracts text from a single PDF file."""
    with pdfplumber.open(pdf_path) as pdf:
        pages = [page.extract_text() or "" for page in pdf.pages]
    return "\n".join(pages)


def build_dataset(input_dir: str, output_file: str) -> None:
    """Walk through input_dir and save extracted text to a JSONL dataset."""
    records: List[Dict[str, str]] = []
    for root, _, files in os.walk(input_dir):
        for fname in files:
            if fname.lower().endswith('.pdf'):
                pdf_path = Path(root) / fname
                text = extract_text_from_pdf(pdf_path)
                records.append({"file": str(pdf_path), "text": text})

    with open(output_file, 'w', encoding='utf-8') as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Build a JSONL dataset from PDFs")
    parser.add_argument("input_dir", help="Directory containing PDFs")
    parser.add_argument("output_file", help="Path to output JSONL file")
    args = parser.parse_args()

    build_dataset(args.input_dir, args.output_file)
