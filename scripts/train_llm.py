"""Example fine-tuning script for a 7B model on your dataset."""
import argparse
from pathlib import Path

from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer


def main(dataset_path: str, model_name: str = "mistralai/Mistral-7B-v0.1", output_dir: str = "model_out"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    dataset = load_dataset("json", data_files=dataset_path, split="train")

    def tokenize_fn(example):
        return tokenizer(example["text"], truncation=True, max_length=1024)

    tokenized = dataset.map(tokenize_fn, batched=True, remove_columns=["file", "text"])

    args = TrainingArguments(
        output_dir=output_dir,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=8,
        num_train_epochs=1,
        fp16=True,
        logging_steps=10,
        save_steps=500,
    )

    trainer = Trainer(model=model, args=args, train_dataset=tokenized)
    trainer.train()
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fine-tune a 7B model on your dataset")
    parser.add_argument("dataset_path", help="Path to JSONL dataset created by build_dataset.py")
    parser.add_argument("--model_name", default="mistralai/Mistral-7B-v0.1")
    parser.add_argument("--output_dir", default="model_out")
    args = parser.parse_args()

    main(args.dataset_path, args.model_name, args.output_dir)
