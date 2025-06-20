import os
import csv
import yaml
from pathlib import Path
from collections import defaultdict
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

from marker_manager import load_markers, save_markers_yaml


class OmniTool(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Marker Omni-Tool")
        self.geometry("600x500")

        self.markers = {}
        self.combinations = {}

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        btn_load_dir = tk.Button(frame, text="Load Marker Directory", command=self.load_directory)
        btn_load_dir.pack(fill=tk.X)

        btn_add_file = tk.Button(frame, text="Add Marker File", command=self.add_file)
        btn_add_file.pack(fill=tk.X, pady=(5,0))

        btn_combo = tk.Button(frame, text="Create Combination", command=self.create_combination)
        btn_combo.pack(fill=tk.X, pady=(5,0))

        btn_analyze = tk.Button(frame, text="Analyze Text", command=self.analyze_text)
        btn_analyze.pack(fill=tk.X, pady=(5,0))

        self.text_output = tk.Text(frame, height=20)
        self.text_output.pack(fill=tk.BOTH, expand=True, pady=(10,0))

    def log(self, msg):
        self.text_output.insert(tk.END, msg + "\n")
        self.text_output.see(tk.END)

    def load_directory(self):
        directory = filedialog.askdirectory(title="Select Marker Directory")
        if not directory:
            return
        self.markers.clear()
        dir_path = Path(directory)
        for file in dir_path.rglob('*'):
            if file.suffix.lower() in ['.yaml', '.yml', '.csv']:
                m = load_markers(file)
                if file.suffix.lower() == '.csv':
                    save_markers_yaml(set(m), file.with_suffix('.yaml'))
                for marker in m:
                    self.markers.setdefault(marker, 0)
                    self.markers[marker] += 1
        self.log(f"Loaded {len(self.markers)} markers from {directory}")

    def add_file(self):
        file_path = filedialog.askopenfilename(title="Select Marker File", filetypes=[("Marker files", "*.yaml *.yml *.csv")])
        if not file_path:
            return
        m = load_markers(Path(file_path))
        if file_path.lower().endswith('.csv'):
            save_markers_yaml(set(m), Path(file_path).with_suffix('.yaml'))
        for marker in m:
            self.markers.setdefault(marker, 0)
            self.markers[marker] += 1
        self.log(f"Added markers from {file_path}")

    def create_combination(self):
        if not self.markers:
            messagebox.showinfo("Info", "No markers loaded")
            return
        combo_name = simpledialog.askstring("Combination", "Enter combination name:")
        if not combo_name:
            return
        top = tk.Toplevel(self)
        top.title("Select Markers")
        lb = tk.Listbox(top, selectmode=tk.MULTIPLE)
        for m in sorted(self.markers.keys()):
            lb.insert(tk.END, m)
        lb.pack(fill=tk.BOTH, expand=True)
        def save_combo():
            selected = [lb.get(i) for i in lb.curselection()]
            if selected:
                self.combinations[combo_name] = selected
                self.log(f"Created combination '{combo_name}' with {len(selected)} markers")
            top.destroy()
        btn = tk.Button(top, text="Save", command=save_combo)
        btn.pack()

    def analyze_text(self):
        if not self.markers and not self.combinations:
            messagebox.showinfo("Info", "Load markers first")
            return
        text = simpledialog.askstring("Analyze Text", "Enter text or path to text file:")
        if not text:
            return
        if os.path.isfile(text):
            with open(text, 'r', encoding='utf-8') as f:
                text = f.read()
        counts = defaultdict(int)
        for marker in self.markers:
            if marker in text:
                counts[marker] += text.count(marker)
        for name, combo in self.combinations.items():
            combo_count = sum(text.count(m) for m in combo)
            counts[name] = combo_count
        self.log("Analysis result:")
        for k, v in counts.items():
            self.log(f"  {k}: {v}")


def main():
    app = OmniTool()
    app.mainloop()


if __name__ == "__main__":
    main()
