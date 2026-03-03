from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import csv
import os
import re
from pathlib import Path
import sys  # Added for command-line arguments

# Register HEIF opener for .heic support if not already done globally
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    print("⚠️ Warning: pillow-heif not found. HEIC files may not be processed.")

print("🚀 Loading BLIP-2 (flowers, bees, scenes)...")
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

def blip_tag_folder(input_folder):
    results = []
    
    # ✅ FIXED: Expand ~ AND strip ALL quotes properly
    input_folder = os.path.expanduser(input_folder)
    input_folder = re.sub(r'["\']+', '', input_folder).strip()  # Remove ALL quotes
    input_folder = os.path.normpath(input_folder)
    print(f"✅ Cleaned path: {input_folder}")
    
    # Verify directory
    if not os.path.exists(input_folder):
        print(f"❌ Directory doesn't exist: {input_folder}")
        return
    if not os.path.isdir(input_folder):
        print(f"❌ Not a directory: {input_folder}")
        return
    
    print(f"✅ Directory confirmed: {input_folder}")
    
    # Show contents (first few)
    dir_contents = os.listdir(input_folder)
    print(f"📂 Top-level items: {dir_contents[:8]}")
    
    # Find all images
    folder_path = Path(input_folder)
    extensions = ['*.JPG', '*.jpg', '*.JPEG', '*.jpeg', '*.PNG', '*.png', '*.HEIC', '*.heic']
    image_files = []
    
    for ext in extensions:
        found = list(folder_path.rglob(ext))
        image_files.extend(found)
        print(f"🔍 Found {len(found)} {ext} files")
    
    # Deduplicate and sort
    image_files = list(set(str(f) for f in image_files))
    image_files.sort()
    
    if not image_files:
        print("❌ No image files found!")
        print(f"💡 Check: find '{input_folder}' -iname '*.[jJ][pP][gG]'")
        return
    
    print(f"\n🎉 Found {len(image_files)} images! Tagging...")
    
    # Process images
    for i, img_path in enumerate(image_files, 1):
        print(f"[{i}/{len(image_files)}] {os.path.basename(img_path)}")
        try:
            image = Image.open(img_path).convert('RGB')
            inputs = processor(image, return_tensors="pt")
            out = model.generate(**inputs, max_length=50, num_beams=5)
            caption = processor.decode(out[0], skip_special_tokens=True)
            
            keywords = [w.strip('.,!?') for w in caption.lower().split() if len(w) > 3]
            unique_keywords = list(set(keywords))
            
            results.append({
                'filename': os.path.basename(img_path),
                'fullpath': img_path,
                'blip_caption': caption,
                'blip_tags': ','.join(unique_keywords) if unique_keywords else 'none'
            })
        except Exception as e:
            print(f"⚠️ Error processing {os.path.basename(img_path)}: {e}")
            continue
    
    # Save CSV (with skip row for batch_tagger)
    csv_filename = 'blip_tags.csv'
    with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['filename', 'fullpath', 'blip_caption', 'blip_tags'])
        writer.writerow([])  # Skip row for batch_tagger to skip easily
        for r in results:
            writer.writerow([r['filename'], r['fullpath'], r['blip_caption'], r['blip_tags']])
    
    print(f"\n✅ Tagged {len(results)} photos!")
    print(f"📄 {csv_filename} ready for batch_tagger.py!")
    if results:
        for r in results[:3]:
            print(f"  {r['filename']}: {r['blip_tags']}")

# 🔧 MODIFIED MAIN EXECUTION: Accepts arguments or asks interactively
if __name__ == "__main__":
    # Check if an argument was passed (e.g., from batch_tagger)
    if len(sys.argv) > 1:
        input_folder = sys.argv[1]
        print(f"📁 Running with provided path: {input_folder}")
    else:
        # Fallback to interactive mode for manual use
        input_folder = input("📁 Folder path (Enter = current): ").strip() or '.'

    blip_tag_folder(input_folder)
