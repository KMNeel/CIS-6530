import os
import re
import csv
from collections import Counter

# ====== CONFIG ======
INPUT_FOLDERS = ["."]   
OUTPUT_DIR = "processed_dataset"
CLEANED_DIR = os.path.join(OUTPUT_DIR, "cleaned_sequences")

GRAM1_CSV = os.path.join(OUTPUT_DIR, "1gram_features.csv")
GRAM2_CSV = os.path.join(OUTPUT_DIR, "2gram_features.csv")
LABELS_CSV = os.path.join(OUTPUT_DIR, "labels.csv")

# ====== HELPERS ======
def extract_label(filename):
    """
    Extract APT label from filename of format:
    APTname_virusshare_md5.opcode
    """
    base = os.path.basename(filename)
    match = re.match(r"(.+?)_virusshare_", base, re.IGNORECASE)
    if match:
        return match.group(1)
    return "UNKNOWN"

def extract_sample_id(filename):
    return os.path.splitext(os.path.basename(filename))[0]

def extract_opcodes_from_file(filepath):
    """
    Keep only the first token (opcode mnemonic) from each non-empty line.
    Example:
        'mov rbp,rsp' -> 'mov'
        'jmp 0x401000' -> 'jmp'
    """
    opcodes = []
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip().lower()
            if not line:
                continue

            parts = line.split()
            if not parts:
                continue

            opcode = parts[0].strip()
            if opcode:
                opcodes.append(opcode)

    return opcodes

def make_ngrams(tokens, n):
    return ["_".join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]

def collect_opcode_files(input_folders):
    files = []
    for folder in input_folders:
        if not os.path.exists(folder):
            print(f"Warning: folder not found -> {folder}")
            continue

        for root, _, filenames in os.walk(folder):
            for name in filenames:
                if name.lower().endswith(".opcode"):
                    files.append(os.path.join(root, name))
    return files

# ====== MAIN ======
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(CLEANED_DIR, exist_ok=True)

    opcode_files = collect_opcode_files(INPUT_FOLDERS)
    print(f"Found {len(opcode_files)} .opcode files")

    samples = []
    vocab_1gram = set()
    vocab_2gram = set()

    # Step 1: clean files and collect n-grams
    for filepath in opcode_files:
        sample_id = extract_sample_id(filepath)
        label = extract_label(filepath)

        opcodes = extract_opcodes_from_file(filepath)

        if not opcodes:
            print(f"Skipping empty opcode sequence: {filepath}")
            continue

        grams1 = opcodes
        grams2 = make_ngrams(opcodes, 2)

        vocab_1gram.update(grams1)
        vocab_2gram.update(grams2)

        # save cleaned sequence
        cleaned_path = os.path.join(CLEANED_DIR, sample_id + ".txt")
        with open(cleaned_path, "w", encoding="utf-8") as f:
            f.write(" ".join(opcodes))

        samples.append({
            "sample_id": sample_id,
            "label": label,
            "grams1": Counter(grams1),
            "grams2": Counter(grams2),
        })

    vocab_1gram = sorted(vocab_1gram)
    vocab_2gram = sorted(vocab_2gram)

    print(f"Usable samples: {len(samples)}")
    print(f"1-gram vocabulary size: {len(vocab_1gram)}")
    print(f"2-gram vocabulary size: {len(vocab_2gram)}")

    # Step 2: write labels.csv
    with open(LABELS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["sample_id", "label"])
        for s in samples:
            writer.writerow([s["sample_id"], s["label"]])

    # Step 3: write 1gram_features.csv
    with open(GRAM1_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["sample_id"] + vocab_1gram)
        for s in samples:
            row = [s["sample_id"]] + [s["grams1"].get(term, 0) for term in vocab_1gram]
            writer.writerow(row)

    # Step 4: write 2gram_features.csv
    with open(GRAM2_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["sample_id"] + vocab_2gram)
        for s in samples:
            row = [s["sample_id"]] + [s["grams2"].get(term, 0) for term in vocab_2gram]
            writer.writerow(row)

    print("Preprocessing complete.")
    print(f"Saved cleaned sequences to: {CLEANED_DIR}")
    print(f"Saved labels to: {LABELS_CSV}")
    print(f"Saved 1-gram features to: {GRAM1_CSV}")
    print(f"Saved 2-gram features to: {GRAM2_CSV}")

if __name__ == "__main__":
    main()