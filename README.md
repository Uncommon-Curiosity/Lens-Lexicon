# Lens & Lexicon
A Python script that takes your photos from being just images to searchable memories by automatically generating and applying descriptive keywords to the metadata
---
It all started with cows.

I was sketching out a new painting and needed cow images to use as a reference. I’ve taken a million photos of cows, I just needed to find them.

I use PhotoPrism on my NAS. The visual thumbnails and search has made finding images oodles easier.

Except, when I searched for “cow,” I got nothing.

PhotoPrism’s AI tagging didn’t include cows.

This is some bullsh*t, I said. There’s got to be a way to get better tags on my photos.

And now here we are.

---
Using AI (qwen3-coder-next and qwen3.5-35b-a3b and running them locally in LM Studio), we now have a Python script that tags photos (.jpg, png, and .heic) with descriptive keywords that make it easier to search and find.

### Before & After: Categorical Keywords vs. Descriptive Observations
![Cow Example 1](https://github.com/Uncommon-Curiosity/Lens-Lexicon/blob/cc0990912f9bb4fcf6e3f5a78c3e742ce69254d6/Cow%201%20with%20before%20and%20after%20keywords.jpg)

![Cow Example 2](https://github.com/Uncommon-Curiosity/Lens-Lexicon/blob/cc0990912f9bb4fcf6e3f5a78c3e742ce69254d6/Cow%202%20with%20before%20and%20after%20keywords.jpg)

***

# Lens & Lexicon: Installation & Use Guide for Mac Users
**Automatically tag thousands of photos (including HEIC) with AI.**

The guide below takes your through installing and running the Python script.

> **Setup takes about 15 minutes. Running it after that takes ~1 minute.**
> *No coding experience needed.*

---

## 🎯 What You'll Get
By the end of this guide, you will be able to:
*   **Automatically scan thousands of photos** (including Apple's HEIC format) and generate smart keywords like "flower," "sunset," "golden retriever," or "beach."
*   **Apply tags directly** to your image files so they show up in **Photos.app, Finder search, Lightroom**, and more.
*   **Keep original photo dates, names, and files completely untouched.**

### ✅ Key Benefits
*   **Safe & Local:** Uses the BLIP AI model locally—no photos are ever uploaded to the cloud.
*   **Private:** Everything runs on your own Mac.
*   **Non-Destructive:** All steps are optional and reversible. Your original photos never change unless you choose to apply tags.

---

## 📋 What You'll Need (and Why)
All tools listed below are free, open-source, and standard for this workflow.
| Item | Why We Need It | Estimated Time |
|------|----------------|----------------|
| **Mac with macOS 12 (Monterey) or newer** | Older systems may lack support for modern AI tools. Most Macs from 2017+ qualify. | Check via Apple menu > About This Mac |
| **Homebrew** (a package manager) | Makes installing tools like `exiftool` and Python *easy* — just one command. Like an "app store" for developers (but safe!). | ~3 minutes |
| **Python 3.9 or newer** | The programming language this tool uses. macOS has Python, but we'll make sure it's compatible. | ~2 minutes |
| **The BLIP AI model** | Runs locally on your Mac to *describe what's in each photo*. (~200 MB download, **one-time**). | ~5–10 minutes (depends on Wi-Fi) |
| **ExifTool** | Reads/writes photo metadata (tags), dates, locations — *safely*. Preserves original file info. | ~1 minute (via Homebrew) |
| **`pillow-heif` library** | Adds native support for **HEIC files** — Apple's modern image format. (Small add-on, also one-time.) | ~1 minute |

> 💡 **Important**: All of this is *optional*, *non-destructive*, and fully reversible. Your original photos never change unless you choose to apply tags.


### 📥 Step 1: Install Homebrew (One-Time Setup)
Homebrew lets you install tools with simple commands. Think of it like the App Store, but for powerful helper tools.

**1. Open Terminal:**
*   Press `Cmd + Space`, type **Terminal**, and press Enter.
*   You'll see a window with blinking text (e.g., `YourName@MacBook ~ %`).

**2. Paste this command into Terminal:**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**3. What you'll see:**
*   A warning: *"This script requires the command line developer tools."* → Type **Y** and press Enter (safe!).
*   A progress bar (~3–5 minutes).
*   Success message: `Brew is installed successfully!`

**4. Add Homebrew to Your Path (Mac-Specific Fix)**
Crucial for Mac users. Check your chip type first: **Apple Menu () > About This Mac**.

*   **Option A: For Apple Silicon (M1, M2, M3)**
    Run these two lines in Terminal:
    ```bash
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
    eval "$(/opt/homebrew/bin/brew shellenv)"
    ```

*   **Option B: For Intel Macs**
    Run these two lines in Terminal:
    ```bash
    echo 'eval "$(/usr/local/Homebrew/bin/brew shellenv)"' >> ~/.zprofile
    eval "$(/usr/local/Homebrew/bin/brew shellenv)"
    ```

> 💡 **Note:** If unsure, try Option A first. If it says "command not found," restart Terminal and try Option B.
> **Verify:** Type `brew --version`. You should see a version number (e.g., Homebrew 4.x.x).

---

### 🐍 Step 2: Install Python (If Needed)
We want Python 3.9+ for best HEIC support.

**1. Check Version:**
```bash
python3 --version
```
*   ✅ **Good:** `Python 3.9.x` or higher.
*   ❌ **Too old:** `Python 2.7.x` or nothing.
*   ⚠️ **Missing:** `zsh: python3: command not found`.

**2. Install/Update with Homebrew (if needed):**
```bash
brew install python
```
Verify again: `python3 --version`. You should see something like `Python 3.12.1`.

---

### 🧰 Step 3: Install ExifTool
ExifTool is the gold standard for safely editing photo metadata (including HEIC).

**Run in Terminal:**
```bash
brew install exiftool
```
*   **Verify:** Type `exiftool -ver` → You should see a version number like `12.70`.

---

### 📦 Step 4: Get the AI & Python Tools Ready
We will create a safe workspace and download the scripts.

**1. Create a New Folder:**
*   Go to **Desktop**.
*   Right-click > **New Folder** → Name it `PhotoTaggerAI`.
*   Double-click to open.

**2. Download the Two Scripts:**

*Option A: Manual Download from GitHub*
Download these files and move them into your folder:
1.  [`batch_tagger_universal_final_2026_03_02.py`](https://raw.githubusercontent.com/Uncommon-Curiosity/Lens-Lexicon/refs/heads/main/batch_tagger_universal_final_2026_03_02.py)
2.  [`blip_tagger_universal_final_2026_03_02.py`](https://raw.githubusercontent.com/Uncommon-Curiosity/Lens-Lexicon/refs/heads/main/blip_tagger_universal_final_2026_03_02.py)

*Option B: Using Terminal (Recommended)*
Ensure you are in the folder (`cd ~/Desktop/PhotoTaggerAI`) and run:
```bash
curl -O "https://raw.githubusercontent.com/Uncommon-Curiosity/Lens-Lexicon/refs/heads/main/batch_tagger_universal_final_2026_03_02.py"
curl -O "https://raw.githubusercontent.com/Uncommon-Curiosity/Lens-Lexicon/refs/heads/main/blip_tagger_universal_final_2026_03_02.py"
```

> 🧠 **Why two scripts?** The `batch_tagger` is the main runner; it automatically calls the `blip_tagger`.

---

### 🧠 Step 5: Create a Safe Environment & Download AI Model
We use a "virtual environment" so the AI tools don't mess with your system.

**1. Activate Terminal in Folder:**
```bash
cd ~/Desktop/PhotoTaggerAI
```

**2. Create Virtual Environment:**
```bash
python3 -m venv venv
```
*(A new folder named `venv` will appear).*

**3. Activate the "Workspace":**
```bash
source venv/bin/activate
```
*You should see `(venv)` at the start of your prompt.*

**4. Install Required Tools:**
```bash
pip install --upgrade pip
pip install transformers pillow torch torchvision pillow-heif
```
> ⚠️ **Expect a wait time (5–10 mins):** `torch` is large (~2GB). You may see warnings about retries; this is normal. Wait for: `Successfully installed...`.

**Why so long?**
Your Mac downloads the BLIP AI model and PyTorch framework once. After this, tagging is instant! The `pillow-heif` library ensures native support for iPhone (HEIC) files.

---

### 🧪 Step 6: Test That Everything Works & DDTC
Let's run a test before touching your real library.

**1. Create a Test Folder:**
*   On Desktop, create `test photos/`.
*   Put at least one **HEIC**, one **PNG**, and one **JPG** inside (e.g., `IMG_1234.HEIC`, `photo.jpg`).

**2. Run the Script:**
In Terminal (ensure `(venv)` is active):
```bash
python batch_tagger_universal_final_2026_03_02.py ~/Desktop/"test photos"
```
*(Quotes are required because of the space in the folder name).*

**Expected Output:**
```text
🚀 Loading BLIP-2 (flowers, bees, scenes)...
✅ pillow-heif HEIC support registered.
🔍 Found 2 image files (JPG/JPEG/PNG/HEIC).
[1/2] photo.jpg
[2/2] IMG_1234.HEIC
✅ Tagged 2 photos!
```

**3. Verify Tags:**
*   In Finder, press `Cmd + I` on a test photo → Look in **Keywords**.
*   You should see words like: `beach`, `child`, `sunset`.

#### ⚠️ DDTC (Double Double Triple Check)
![DDTC](https://github.com/Uncommon-Curiosity/Lens-Lexicon/blob/e64929a74291b95a847da245fb1b615319b75d70/DDTC_logo.png)

Time to double double triple check (DDTC) before you send this off on the rest of your photos.

**Why DDTC?**

The first test doesn't count; never trust the first test.

> 🧠 Remember, using the up arrow brings back the last command you used in Terminal.

Double check 1: Replace the photos in the test folder and run the script again. Check and make sure the keywords match what you would expect.

Double check 2: Replace the photos in the test folder again and run the script. Check and make sure the keywords match what you would expect.

Triple check: Replace the photos in the test folder again (maybe add a few more) and run the script. Check and make sure the keywords match what you would expect.

**Delete** the `test photos/` folder when done.

---

### 🖼️ Step 7: Tag ALL Your Photos! (Including HEIC)

Now for the fun part—tagging your real library.

**1. Choose a Folder:**
*   e.g., `~/Pictures/2024 Photos`, `~/Desktop/Vacation`.
*   *(The tool handles thousands of files easily).*

**2. Run the Pipeline:**
In Terminal:
```bash
python batch_tagger_universal_final_2026_03_02.py ~/Pictures/"Family 2019-2024"
```
*(Use quotes if your path has spaces, or drag the folder into Terminal to auto-fill).*

**Expected Output:**
```text
📁 Working directory: /Users/you/Desktop/PhotoTaggerAI
✅ Target image folder: /Users/you/Pictures/Family 2019-2024
🚀 Generating tags via blip_tagger_universal.py...
🔍 Found 324 image files (JPG/JPEG/PNG/HEIC).
[1/324] IMG_0123.jpg
...
✅ Tagged 324 photos!
📄 Output saved to: /Users/you/Desktop/PhotoTaggerAI/blip_tags.csv
💡 Tip: Restart Photos.app or use ⌘R in Finder to see updated keywords.
```

> ✅ **Congratulations!** Your photos now have AI-generated keywords attached.
> *   Original dates preserved? ✅
> *   Files renamed/moved? No.
> *   HEIC tags visible? Yes (using XMP:Keywords).

---

## 🔍 How to See & Use the New Tags

*   **In Finder:** Select photo > `Cmd + I` > Look in **Keywords**.
*   **In Photos.app:** Select photo > `Cmd + I` > Under Keywords, you'll see the tags.
*   **In Lightroom/Bridge:** They automatically recognize IPTC (JPG/PNG) or XMP (HEIC) keywords.

**Verify a HEIC file manually:**
```bash
exiftool -XMP:Keywords "/path/to/IMG_7061.HEIC"
# Output: XMP:Keywords : ocean,sunset,smiling
```

---

## ❓ Troubleshooting & Tips
| Problem | What to Do (Mac-Specific) |
|--------|-------------|
| `zsh: command not found: brew` | Re-run the Homebrew install script. Then restart your Terminal window and try again. |
| `ModuleNotFoundError: No module named 'PIL'` | Ensure you are inside the `(venv)` workspace, then run `pip install pillow transformers torch pillow-heif`. |
| `-bash: python3: command not found` | Install Python via `brew install python`, then restart Terminal. |
| `exiftool not found` | Run `brew reinstall exiftool`, then confirm with `exiftool -ver`. |
| Script says "Permission denied" | In Finder, right-click the `.py` file → **Open** → click "Open" again (this overrides Gatekeeper warning once). |
| HEIC files skipped or show errors | Run `pip install pillow-heif` — and double-check you see `✅ pillow-heif HEIC support registered.` in output. |
| Tagging is slow (e.g., 1 photo/second) | That's normal! BLIP runs on your CPU (not GPU). 300 photos may take ~10–15 minutes. Take a break ☕ |
| Finder doesn't show keywords yet | Quit and re-open Photos.app, or press `Cmd + Option + Esc` → Force Quit Finder → relaunch it to refresh. |

### 🧩 Bonus: How to Use It Again (Future Runs)
Next time you want to tag more photos:
```bash
cd ~/Desktop/PhotoTaggerAI
source venv/bin/activate
python batch_tagger_universal_final_2026_03_02.py "/your/new/photo/folder"
```

### 🚨 Good to Know Tidbits
1.  **Timeout:** The script has a default timeout of 1200 seconds (20 mins). If you have a massive folder, edit `line 89` in `batch_tagger_universal_final_2026_03_02.py` to increase the limit.
2.  **Dates:** This does not overwrite created dates for files.
3.  **CSV Files:** Two CSVs are generated:
    *   `blip_tags.csv`: Full descriptive sentences from AI analysis.
    *   `exif_keywords_date_time.csv`: The keywords applied to the photos.

### ⭐️ Why Requirements Matter (The "Cow" Discovery)

The full process in a nutshell and why knowing your requirements is important

Blip tagger script (called from batch tagger) looks at the photo, figures out what’s in the photo, and writes a descriptive sentence about it. In the blip_tags.csv, it drops in that sentence and then writes keywords.

The script takes that and strips out all the stop words and looks for just nouns and verbs and adjectives to use as keywords. That goes into exif_keywords_.csv.

Now, here’s the important bit that I discovered and why requirements are a must have. Initially, the script was looking keywords with four letters or more. Do you know what’s wrong with having keywords of 4 letters or more? Yeah, you miss cow. I fixed the script to use 3 or more letters and magically cow came in, bee came in. It’s a glorious thing.

> This is why iterating and figuring out your requirements is important before starting.

---

## 🎁 Final Notes & Community

✅ Everything stays local on your Mac. No uploads, no tracking.

### Need Help?
If something breaks, don't panic!
1.  Ask your favorite AI tool for help with the error message.
2.  Leave a comment with:
    *   Screenshot of the error.
    *   Step you were on (e.g., "after typing pip install").
    *   Your Mac model & macOS version.

> **Does it feel like it'd be more fun to learn these skills as part of a group?**
> I think so too. If you’re interested in getting together with others to start from nothing, figure things out, and build something real, reach out or drop a comment. No experience required—just curiosity and good energy.

**Happy tagging!** — Joy 🙌
