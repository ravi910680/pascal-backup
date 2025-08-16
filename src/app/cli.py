# src/app/cli.py

import argparse
from .pipeline import summarize_pdf

def main():
    parser = argparse.ArgumentParser(description="Summarize a PDF file using OpenAI.")
    parser.add_argument("--pdf-file", required=True, help="Path to the PDF file")
    args = parser.parse_args()

    summary = summarize_pdf(args.pdf_file)
    print("\n=== SUMMARY ===\n")
    print(summary)

if __name__ == "__main__":
    main()
