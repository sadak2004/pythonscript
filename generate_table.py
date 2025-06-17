import os
import json
from datetime import datetime

DATASETS_DIR = 'datasets'
OUTPUT_FILE = 'datasets_table.md'

def get_last_updated(dataset_path):
    timestamps = []
    for root, _, files in os.walk(dataset_path):
        for f in files:
            full_path = os.path.join(root, f)
            timestamps.append(os.path.getmtime(full_path))
    if timestamps:
        return datetime.fromtimestamp(max(timestamps)).strftime('%Y-%m-%d')
    return 'Unknown'

def get_num_data_points(dataset_path):
    data_file = os.path.join(dataset_path, 'data.csv')
    if os.path.exists(data_file):
        with open(data_file) as f:
            # count lines excluding header
            return sum(1 for _ in f) - 1
    return 'Unknown'

def main():
    rows = []
    for dataset in os.listdir(DATASETS_DIR):
        dataset_path = os.path.join(DATASETS_DIR, dataset)
        if os.path.isdir(dataset_path):
            meta_file = os.path.join(dataset_path, 'metadata.json')
            if os.path.exists(meta_file):
                with open(meta_file) as f:
                    meta = json.load(f)
            else:
                meta = {}
            name = meta.get('name', dataset)
            last_updated = get_last_updated(dataset_path)
            num_points = get_num_data_points(dataset_path)
            properties = ", ".join(meta.get('properties', []))
            cite = meta.get('cite', '')
            doi = meta.get('doi', '')
            if doi:
                doi = f"[{doi}](https://doi.org/{doi})"
            rows.append(f"| {name} | {last_updated} | {num_points} | {properties} | {cite} | {doi} |")

    with open(OUTPUT_FILE, 'w') as out:
        out.write("| Name | Last Updated | # Data Points | Properties | Cite | DOI |\n")
        out.write("|------|--------------|---------------|------------|------|-----|\n")
        for row in rows:
            out.write(row + "\n")

if __name__ == "__main__":
    main()
