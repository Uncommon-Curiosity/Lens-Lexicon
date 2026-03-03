#!/usr/bin/env python3

"""
Lens & Lexicon: Photo Tagging Tool
----------------------------------
A Python script that takes your photos from being just images to searchable memories 
by automatically generating and applying descriptive keywords to the metadata.

Created by Uncommon Curiosity author Joy Cicman Liuzzo
Date: 2026-03-02

"""

# ---------------------------------------------------------
# Attribution & Credits
# ---------------------------------------------------------
# Created by: Uncommon Curiosity author Joy Cicman Liuzzo
# Date:       2026-03-02
# Project:    Lens & Lexicon (Photo Tagging with AI)
# Description: Auto-tagging tool for HEIC/JPG/PNG using BLIP AI.
# ---------------------------------------------------------

import csv
import re
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from shutil import which
import argparse
import time

STOPWORDS = {'this','is','a','an','the','that','there','with','are','and','on','in','by','of','to','for'}

def find_exiftool():
    """Locates the exiftool binary."""
    candidates = [
        which("exiftool"),
        Path("/usr/local/bin/exiftool"),      # Intel Homebrew
        Path("/opt/homebrew/bin/exiftool"),   # Apple Silicon Homebrew
    ]
    
    for p in candidates:
        if p and Path(p).exists():
            return str(Path(p))
            
    raise RuntimeError("❌ ExifTool not found. Please install via: brew install exiftool")

def run_blip_tagger(script_dir, image_dir):
    # Try the specific filename requested first, fall back to standard name if needed
    possible_names = [
        "blip_tagger_universal_final_2026_03_02.py",
        "blip_tagger_universal.py" 
    ]
    
    tagger_script_path = None
    for name in possible_names:
        candidate = script_dir / name
        if candidate.exists():
            tagger_script_path = candidate
            break
            
    if not tagger_script_path:
        print(f"❌ ERROR: Could not find blip_tagger script (tried {possible_names})")
        sys.exit(1)

    # Run the tagger script
    cmd = [sys.executable, str(tagger_script_path), str(image_dir)]
    
    print(f"\n🚀 Stage 1: Running BLIP Tagger ({tagger_script_path.name})...")
    print("⏳ Progress will appear below:")
    print("-" * 40)
    
    # 🔑 KEY CHANGE: Stream output directly to console
    result = subprocess.run(
        cmd, 
        stdout=sys.stdout, 
        stderr=sys.stderr
    )
    
    if result.returncode != 0:
        print(f"\n❌ BLIP Tagger execution failed!")
        sys.exit(1)

    # Wait for blip_tags.csv to appear (this loop will now be very fast because we saw the output above)
    csv_path = script_dir / "blip_tags.csv"
    
    max_wait_time = 2000
    start_time = time.time()
    
    while not csv_path.exists():
        elapsed = int(time.time() - start_time)
        
        if elapsed >= max_wait_time:
            print(f"\n❌ TIMEOUT: 'blip_tags.csv' was not created after {max_wait_time} seconds.")
            sys.exit(1)
            
        if elapsed % 30 == 0 and elapsed > 0:
            print(f"   ... still checking for file ({elapsed}s)...")
            
        time.sleep(2)
        
    print("-" * 40)
    print(f"✅ BLIP Tagger finished! 'blip_tags.csv' created after {int(time.time() - start_time)}s.")


def main(image_dir: Path, output_csv=None):
    script_dir = Path(__file__).resolve().parent
    
    print(f"📁 Working directory: {script_dir}")
    
    image_dir = Path(image_dir).expanduser().resolve()
    if not image_dir.exists():
        print(f"❌ Image folder does not exist: {image_dir}")
        sys.exit(1)
    print(f"✅ Target image folder: {image_dir}")

    try:
        EXIFTOOL = find_exiftool()
    except RuntimeError as e:
        print(e)
        sys.exit(1)

    # --- STAGE 1: Run BLIP Tagger & Wait for CSV ---
    run_blip_tagger(script_dir, image_dir)
    
    csv_path = script_dir / "blip_tags.csv"
    
    # --- STAGE 2: Process Tags & Apply EXIF ---
    print("\n📂 Stage 2: Processing tags and applying metadata...")

    if output_csv is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_csv = f"exif_keywords_{ts}.csv"
    
    output_csv_path = script_dir / output_csv

    print("✂️ Filtering and formatting keywords...")
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f_in, \
             open(output_csv_path, 'w', newline='', encoding='utf-8') as f_out:
            
            reader = csv.reader(f_in)
            writer = csv.writer(f_out)
            writer.writerow(['SourceFile', 'IPTC:Keywords'])

            header_skipped = False
            for row in reader:
                if not header_skipped and row == ['filename', 'fullpath', 'blip_caption', 'blip_tags']:
                    header_skipped = True
                    continue
                
                if not row or all(not cell.strip() for cell in row):
                    continue
                
                if not header_skipped:
                    continue

                if len(row) < 4:
                    print(f"⚠️ Skipping malformed row: {row}")
                    continue

                fullpath = row[1].strip()
                caption_text = (row[2] or "").strip() + " " + (row[3] or "").strip()
                
                # Extract only 3+ letter English words, dedup & filter stopwords
                words = re.findall(r"\b[a-zA-Z]{3,}\b", caption_text.lower())
                seen = set()
                unique_words = []
                for w in words:
                    if w not in STOPWORDS and w not in seen:
                        seen.add(w)
                        unique_words.append(w)
                
                # Limit to 8 keywords for clean metadata
                keywords = ",".join(unique_words[:8])
                if not keywords:
                    continue

                writer.writerow([fullpath, keywords])
        
        print(f"✅ Tag CSV created: {output_csv_path}")
    except Exception as e:
        print(f"❌ Error processing CSV: {e}")
        sys.exit(1)

    # Apply EXIF tags — HEIC-aware (XMP for HEIC, IPTC for others)
    print("🏷️ Applying EXIF keywords using correct namespaces...")
    
    with open(output_csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            fullpath = row['SourceFile'].strip()
            keywords = row.get('IPTC:Keywords', '').strip()

            # Normalize paths to fix "File not found" errors (spaces, slashes, ~)
            fullpath = re.sub(r'\s+', ' ', fullpath).strip()
            fullpath = os.path.expanduser(fullpath)
            fullpath = os.path.normpath(fullpath)

            if not os.path.exists(fullpath):
                print(f"⚠️ File not found (skipping): {fullpath}")
                continue

            # Determine file extension case-insensitively
            ext = Path(fullpath).suffix.lower()
            
            if ext == '.heic':
                target_field = 'XMP:Keywords'
                ns_name = "XMP"
                exiftool_args = [f"-{target_field}={keywords}", f"-XMP:Subject={keywords}"]
            else:
                target_field = 'IPTC:Keywords'
                ns_name = "IPTC"
                exiftool_args = [f"-{target_field}={keywords}"]

            cmd = [
                EXIFTOOL,
                "-overwrite_original_in_place",   
                "-P",                              
            ] + exiftool_args + [fullpath]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                print(f"⚠️ Failed on {os.path.basename(fullpath)} ({ns_name}):")
                print(f"   stderr: {result.stderr}")
            else:
                # Optional: show success per-file (comment out for speed on large sets)
                print(f"[{i}] ✅ {os.path.basename(fullpath)} ({ns_name}) → \"{keywords}\"")

    print("\n✅ Tagging complete!")
    print("💡 Tip: Restart Photos.app or use ⌘R in Finder to see updated keywords.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Auto-tag photos with AI (BLIP) + ExifTool. HEIC support included."
    )
    parser.add_argument("image_dir", help="Path to folder with images")
    parser.add_argument("--output", nargs="?", default=None, help="Custom output CSV name (optional)")
    
    args = parser.parse_args()
    main(Path(args.image_dir), output_csv=args.output)