import os
import json

REPO_ROOT = "."
OUTPUT_FILE = "frontend/public/repo_map.json"

EXCLUDE_DIRS = {
    ".git", "__pycache__", "node_modules", "dist", "venv", "env", ".idea", ".vscode", "frontend/dist"
}

EXCLUDE_EXTENSIONS = {
    ".pyc", ".ico", ".png", ".jpg", ".jpeg", ".svg", ".parquet", ".zip", ".tar", ".gz", ".woff", ".woff2", ".ttf", ".eot"
}

TEXT_EXTENSIONS = {
    ".py", ".ts", ".tsx", ".js", ".jsx", ".md", ".json", ".txt", ".sql", ".yml", ".yaml", ".css", ".html", ".sh", ".gitignore"
}

MAX_FILE_SIZE = 100 * 1024  # 100 KB

def get_file_type(filename):
    if filename.startswith("."):
        return "config"
    ext = os.path.splitext(filename)[1]
    if ext in TEXT_EXTENSIONS:
        return "text"
    return "binary"

def build_tree(path):
    name = os.path.basename(path)
    if name == "":
        name = "root"

    node = {
        "name": name,
        "path": path,
        "type": "folder",
        "children": []
    }

    try:
        entries = sorted(os.listdir(path))
    except PermissionError:
        return None

    for entry in entries:
        full_path = os.path.join(path, entry)

        if os.path.isdir(full_path):
            if entry in EXCLUDE_DIRS:
                continue
            child = build_tree(full_path)
            if child:
                node["children"].append(child)
        else:
            ext = os.path.splitext(entry)[1]
            if ext in EXCLUDE_EXTENSIONS:
                continue

            size = os.path.getsize(full_path)
            file_node = {
                "name": entry,
                "path": full_path,
                "type": "file",
                "size": size,
                "file_type": get_file_type(entry)
            }

            if size < MAX_FILE_SIZE and get_file_type(entry) in ["text", "config"]:
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        file_node["content"] = f.read()
                except Exception as e:
                    file_node["content"] = f"Error reading file: {str(e)}"

            node["children"].append(file_node)

    return node

def main():
    print(f"Generating repo map from {REPO_ROOT}...")

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    tree = build_tree(REPO_ROOT)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(tree, f, indent=2)

    print(f"Repo map saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
