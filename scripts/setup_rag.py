"""Simple example of setting up a retrieval-augmented generation (RAG) pipeline."""
import argparse
from pathlib import Path

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def build_vector_store(dataset_path: str, persist_dir: str = "faiss_index") -> None:
    loader = JSONLoader(dataset_path, jq_schema=".text")
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings()
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(persist_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build FAISS index from dataset")
    parser.add_argument("dataset_path", help="Path to JSONL dataset")
    parser.add_argument("--persist_dir", default="faiss_index")
    args = parser.parse_args()

    build_vector_store(args.dataset_path, args.persist_dir)
