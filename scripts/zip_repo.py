#!/usr/bin/env python3
import io
import os
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

repo_dir = Path(__file__).parent.parent
addon_dir = repo_dir / "files" / "repository.fentastic"
addon_xml = addon_dir / "addon.xml"

version = ET.parse(addon_xml).getroot().get("version")
if not version:
    print(f"Could not read version from {addon_xml}", file=sys.stderr)
    sys.exit(1)

zip_name = f"repository.fentastic-{version}.zip"
output_path = repo_dir / zip_name

with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    for root, _, files in os.walk(addon_dir):
        root_path = Path(root)
        arc_root = Path("repository.fentastic") / root_path.relative_to(addon_dir)
        zf.write(root, arc_root)
        for file in files:
            zf.write(root_path / file, arc_root / file)

print(f"Packed: {zip_name}")

index_path = repo_dir / "index.html"
with io.open(index_path, "w", newline="\n") as f:
    f.write(f'<!DOCTYPE html>\n<a href="{zip_name}">{zip_name}</a>\n')
print(f"Updated index.html (v{version})")
