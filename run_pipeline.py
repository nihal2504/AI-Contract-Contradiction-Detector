import argparse
from src.clause_splitter import split_clauses
from src.pair_generator import generate_pairs
from src.contradiction_detector import detect_contradictions
from src.report import save_report

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--top-k", type=int, default=30)
    parser.add_argument("--threshold", type=float, default=0.65)
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read()

    clauses = split_clauses(text)
    pairs = generate_pairs(clauses, top_k=args.top_k)
    results = detect_contradictions(pairs, threshold=args.threshold)

    save_report(results)

    print("Done. Reports saved in outputs/")
    print(f"Clauses found: {len(clauses)}")
    print(f"Contradictions found: {len(results)}")

if __name__ == "__main__":
    main()