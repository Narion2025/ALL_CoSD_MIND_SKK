# ALL_CoSD_MIND_SKK

This repository currently holds tooling for working with **markers**. These
markers can be stored as YAML or CSV files. The provided script
`marker_manager.py` scans a directory of marker files, converts CSV files to
YAML, and prints a summary of markers and meta markers.

A simple graphical interface is available with `omni_tool.py` which allows you
to load marker directories, add new marker files, create named combinations, and
run text analyses.

## Usage

Run the CLI marker manager:

```bash
python scripts/marker_manager.py <directory>
```

Run the GUI omni-tool:

```bash
python scripts/omni_tool.py
```

`marker_manager.py` will create YAML versions of any CSV files it finds and
output a count of occurrences for each marker and meta marker. The GUI tool
exposes similar functionality in an adaptable interface for macOS and other
platforms.
