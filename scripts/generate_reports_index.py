import os
import json
import datetime
import math

OUTPUT_DIR = "output"
INDEX_FILE = "frontend/public/reports_index.json"

def get_file_size_str(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

def generate_index():
    print(f"Scanning {OUTPUT_DIR} for reports...")

    reports = []

    if not os.path.exists(OUTPUT_DIR):
        print(f"Directory {OUTPUT_DIR} does not exist.")
        return

    for filename in os.listdir(OUTPUT_DIR):
        filepath = os.path.join(OUTPUT_DIR, filename)

        if os.path.isfile(filepath):
            stats = os.stat(filepath)

            # Determine file type
            ext = os.path.splitext(filename)[1].lower()
            file_type = "unknown"
            if ext == ".md":
                file_type = "markdown"
            elif ext == ".json" or ext == ".jsonl":
                file_type = "json"
            elif ext == ".parquet":
                file_type = "data"
            elif ext == ".gguf":
                file_type = "model"

            report = {
                "filename": filename,
                "path": filepath,
                "size_bytes": stats.st_size,
                "size_str": get_file_size_str(stats.st_size),
                "modified_timestamp": stats.st_mtime,
                "modified_date": datetime.datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                "type": file_type
            }

            reports.append(report)

    # Sort by modification date descending
    reports.sort(key=lambda x: x["modified_timestamp"], reverse=True)

    os.makedirs(os.path.dirname(INDEX_FILE), exist_ok=True)

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(reports, f, indent=2)

    print(f"Reports index saved to {INDEX_FILE} with {len(reports)} entries.")

if __name__ == "__main__":
    generate_index()
