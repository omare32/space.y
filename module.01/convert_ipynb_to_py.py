import json
import sys
import os


def extract_code_cells(ipynb_path: str, py_path: str) -> None:
    with open(ipynb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    lines = []
    lines.append(f"# Auto-generated from {os.path.basename(ipynb_path)}")
    lines.append("# Conversion: code cells only. Markdown omitted.")

    cell_no = 0
    for cell in nb.get('cells', []):
        if cell.get('cell_type') == 'code':
            cell_no += 1
            lines.append("")
            lines.append(f"# %% [code] - Cell {cell_no}")
            source = cell.get('source', [])
            if isinstance(source, list):
                # Ensure clean newlines
                for s in source:
                    if s.endswith('\n'):
                        lines.append(s[:-1])
                    else:
                        lines.append(s)
            elif isinstance(source, str):
                lines.append(source.rstrip('\n'))

    # Ensure trailing newline
    content = "\n".join(lines) + "\n"
    with open(py_path, 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == '__main__':
    ipynb = sys.argv[1] if len(sys.argv) > 1 else os.path.join('module.01', 'jupyter-labs-spacex-data-collection-api.ipynb')
    outpy = sys.argv[2] if len(sys.argv) > 2 else os.path.join('module.01', 'jupyter-labs-spacex-data-collection-api.py')
    extract_code_cells(ipynb, outpy)
