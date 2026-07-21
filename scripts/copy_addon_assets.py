#!/usr/bin/env python3

import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

ASSET_TAGS = ("icon", "fanart", "banner", "clearlogo", "screenshot")


def declared_assets(addon):
    assets = addon.find("./extension[@point='xbmc.addon.metadata']/assets")
    if assets is None:
        return []
    return [
        e.text.strip()
        for e in assets
        if e.tag in ASSET_TAGS and e.text and e.text.strip()
    ]


def copy_catalog_assets(catalog_dir):
    catalog = Path(catalog_dir)
    info = catalog / "addons.xml"
    if not info.is_file():
        sys.exit(f"No addons.xml in {catalog}")

    copied = 0
    for addon in ET.parse(info).getroot():
        addon_id = addon.get("id")
        version = addon.get("version")
        addon_dir = catalog / addon_id
        archive = addon_dir / f"{addon_id}-{version}.zip"

        wanted = declared_assets(addon)
        if not wanted or not archive.is_file():
            continue

        with zipfile.ZipFile(archive) as zf:
            names = set(zf.namelist())
            for rel in wanted:
                member = f"{addon_id}/{rel}"
                if member not in names:
                    print(f"  MISSING {addon_id}: {rel} not in zip")
                    continue
                target = addon_dir / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(zf.read(member))
                copied += 1
                print(f"  {addon_id}/{rel}")

    print(f"{catalog}: copied {copied} assets")
    return copied


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: copy_addon_assets.py CATALOG_DIR [CATALOG_DIR ...]")
    total = sum(copy_catalog_assets(d) for d in sys.argv[1:])
    print(f"total: copied {total} assets")


if __name__ == "__main__":
    main()
