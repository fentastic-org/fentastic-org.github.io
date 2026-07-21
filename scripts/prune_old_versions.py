#!/usr/bin/env python3

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def prune_catalog(catalog_dir):
    catalog = Path(catalog_dir)
    info = catalog / "addons.xml"
    if not info.is_file():
        sys.exit(f"No addons.xml in {catalog}")

    removed = 0
    freed = 0
    for addon in ET.parse(info).getroot():
        addon_id = addon.get("id")
        keep = addon.get("version")
        addon_dir = catalog / addon_id
        if not addon_dir.is_dir():
            continue

        # Files this add-on may own, with the version each one is stamped with.
        patterns = (
            re.compile(r"^" + re.escape(addon_id) + r"-(.+)\.zip$"),
            re.compile(r"^" + re.escape(addon_id) + r"-(.+)\.zip\.md5$"),
            re.compile(r"^changelog-(.+)\.txt$"),
        )

        for path in sorted(addon_dir.iterdir()):
            if not path.is_file():
                continue
            for pattern in patterns:
                match = pattern.match(path.name)
                if match and match.group(1) != keep:
                    size = path.stat().st_size
                    path.unlink()
                    removed += 1
                    freed += size
                    print(f"  removed {path.relative_to(catalog)}")
                    break

        print(f"  kept {addon_id} {keep}")

    print(f"{catalog}: removed {removed} files, freed {freed / 1048576:.1f} MB")
    return removed, freed


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: prune_old_versions.py CATALOG_DIR [CATALOG_DIR ...]")

    total_removed = 0
    total_freed = 0
    for catalog_dir in sys.argv[1:]:
        removed, freed = prune_catalog(catalog_dir)
        total_removed += removed
        total_freed += freed

    print(f"total: removed {total_removed} files, freed {total_freed / 1048576:.1f} MB")


if __name__ == "__main__":
    main()
