import csv
import yaml
from collections import defaultdict
from pathlib import Path
from typing import Tuple, Dict, Iterable


def load_markers(file_path):
    ext = file_path.suffix.lower()
    markers = []
    if ext == '.yaml' or ext == '.yml':
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if isinstance(data, list):
                markers.extend(data)
            elif isinstance(data, dict) and 'markers' in data:
                markers.extend(data['markers'])
    elif ext == '.csv':
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    markers.append(row[0])
    return markers


def save_markers_yaml(markers, out_path):
    with open(out_path, 'w', encoding='utf-8') as f:
        yaml.dump(sorted(markers), f, allow_unicode=True)


def analyze_markers(directory: str) -> Tuple[Dict[str, int], Dict[str, int]]:
    """Scan `directory` for marker files and return occurrence counts."""
    directory = Path(directory)
    all_markers: Dict[str, int] = defaultdict(int)
    meta_markers: Dict[str, int] = defaultdict(int)

    for file in directory.rglob('*'):
        if file.suffix.lower() in ['.yaml', '.yml', '.csv']:
            markers = load_markers(file)
            for marker in markers:
                if isinstance(marker, dict) and marker.get('meta'):
                    name = marker['meta']
                    meta_markers[name] += 1
                else:
                    all_markers[marker] += 1
            # convert csv to yaml if needed
            if file.suffix.lower() == '.csv':
                yaml_path = file.with_suffix('.yaml')
                save_markers_yaml(set(markers), yaml_path)
    return all_markers, meta_markers


def write_unique_markers(markers: Iterable[str], out_path: Path) -> None:
    """Write unique markers to a YAML file."""
    unique = sorted(set(markers))
    with open(out_path, "w", encoding="utf-8") as f:
        yaml.dump(unique, f, allow_unicode=True)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Manage marker files")
    parser.add_argument("directory", help="Directory with marker files")
    parser.add_argument(
        "--dedup",
        action="store_true",
        help="Write all unique markers to <directory>/consolidated_markers.yaml",
    )
    args = parser.parse_args()

    markers, metas = analyze_markers(args.directory)
    print("Marker summary:")
    for marker, count in sorted(markers.items()):
        print(f"{marker}: {count} examples")
    if metas:
        print("\nMeta markers:")
        for marker, count in sorted(metas.items()):
            print(f"{marker}: {count} examples")

    if args.dedup:
        out_path = Path(args.directory) / "consolidated_markers.yaml"
        write_unique_markers(markers.keys(), out_path)
        print(f"\nSaved {len(set(markers))} unique markers to {out_path}")


if __name__ == '__main__':
    main()
