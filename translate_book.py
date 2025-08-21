#!/usr/bin/env python3
import os, sys, argparse, hashlib, shutil
from pathlib import Path
import deepl

def sha1(path: Path) -> str:
    import hashlib
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:12]

def main():
    ap = argparse.ArgumentParser(description="Translate DOCX/PDF with DeepL API Free/Pro")
    ap.add_argument("input", help="Input .docx or .pdf")
    ap.add_argument("--target", default="EN-GB", help="Target language (EN-GB or EN-US)")
    ap.add_argument("--source", default="SV", help="Source language (default: SV)")
    ap.add_argument("--out", help="Output file (default: <stem>_EN.docx)")
    args = ap.parse_args()

    in_path = Path(args.input).resolve()
    if not in_path.exists():
        sys.exit("Input not found")

    out_path = Path(args.out) if args.out else in_path.with_name(f"{in_path.stem}_EN{in_path.suffix}")

    auth = os.getenv("DEEPL_AUTH_KEY")
    if not auth:
        sys.exit("Please set DEEPL_AUTH_KEY env variable")

    client = deepl.DeepLClient(auth)

    print(f"[i] Translating {in_path.name} → {out_path.name}")
    client.translate_document_from_filepath(
        str(in_path), str(out_path),
        source_lang=args.source, target_lang=args.target
    )
    print(f"[✓] Done: {out_path}")

if __name__ == "__main__":
    main()
