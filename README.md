# SyllaClaw 📚
### Drop Your Syllabus. Get Your Life.
**Built for STEM students. Free to build. Free to run.**

> "I spent 3 hours setting up my calendar every semester. SyllaClaw does it in 60 seconds — and it told me Week 8 was going to be brutal before I even knew it."

---

## What it does

You drop your syllabus files into a folder (or a Google Drive folder). SyllaClaw reads every one of them, extracts every deadline, builds a complete time-blocked weekly schedule around your job and your life, and outputs everything as a CSV you import directly into Google Calendar.

**What you get:**
- Every deadline, exam, and project loaded into Google Calendar
- A complete weekly schedule: when to study, when to sleep, when to call home, when to protect your free time
- Work shifts locked in as non-negotiable blocks
- Heavy weeks flagged *before* they arrive
- A Sunday evening briefing telling you what to focus on next week

**What it costs:** Nothing. One free NVIDIA API key. Your existing Google account.

---

## Two ways to use it

### Option A — Command Line (for technical students)
Drop files on your laptop. Run one command in your terminal.

### Option B — Google Apps Script (for everyone else)
Works entirely in your browser. No installation. No terminal.
Drop files in Google Drive. Click a menu item. Done.

**Both options produce the same output.**

---

## Option A — Command Line Setup

### Prerequisites
- Python 3.9 or higher
- A free NVIDIA NIM API key (see Step 1)

### Step 1 — Get your free NVIDIA NIM key
1. Go to [build.nvidia.com](https://build.nvidia.com)
2. Sign in or create a free account — no credit card required
3. Search for: `llama-3.3-nemotron-super-49b-v1`
4. Click **Get API Key**
5. Copy your key — it starts with `nvapi-`

### Step 2 — Install
```bash
git clone https://github.com/itsChanelML/syllaclaw
cd syllaclaw
pip3 install -r requirements.txt
```

### Step 3 — Set your API key
```bash
cp .env.example .env
# Open .env and replace the placeholder with your real key
```

### Step 4 — Add your syllabi
Drop your syllabus files into the `syllabi/` folder.

Supported formats: `.pdf`, `.docx`, `.txt`, `.md`

Also add your work schedule as `work_schedule.txt` if you have one.

### Step 5 — Run
```bash
# Full run — reads syllabi/ folder
python3 syllaclaw.py

# Specify your name for personalized output
python3 syllaclaw.py --name "Alex Rivera"

# Use a custom folder
python3 syllaclaw.py --folder ./my_syllabi

# Run with sample files to see how it works
python3 syllaclaw.py --demo

# See the ESCALATE beat (what happens when a file is unreadable)
python3 syllaclaw.py --break
```

### Step 6 — Import to Google Calendar
After running, check the `output/` folder for:
- `weekly_schedule.csv` — your time-blocked week
- `semester_deadlines.csv` — all your deadlines
- `conflict_report.csv` — your heavy weeks and reschedule suggestions

**To import:**
1. Open [calendar.google.com](https://calendar.google.com)
2. Click the ⚙ gear → **Settings**
3. Click **Import & Export** in the left sidebar
4. Click **Select file** → choose `weekly_schedule.csv`
5. Click **Import**
6. Repeat for `semester_deadlines.csv`

Your semester is now in Google Calendar. Done.

---

## Option B — Google Apps Script Setup

No installation needed. Works entirely in your browser.

### Step 1 — Get your free NVIDIA NIM key
Same as Option A Step 1 above.

### Step 2 — Create your Google Sheet
1. Go to [sheets.google.com](https://sheets.google.com)
2. Create a new blank spreadsheet
3. Name it: `SyllaClaw`

### Step 3 — Add the script
1. Click **Extensions → Apps Script**
2. Delete any existing code
3. Copy the entire contents of `scripts/SyllaClaw.gs` from this repo
4. Paste it into the editor
5. Find the `CONFIG` section at the top:
   ```javascript
   const CONFIG = {
     NIM_API_KEY:    "YOUR_NIM_API_KEY_HERE",  // ← replace this
     STUDENT_NAME:   "Your Name",              // ← add your name
     ...
   }
   ```
6. Replace the values with yours
7. Click **Save** (Ctrl+S)
8. Close the Apps Script tab
9. Reload your Google Sheet

A **SyllaClaw** menu will now appear in your Sheet.

### Step 4 — Add your syllabi
Create sheet tabs named `Syllabus_1`, `Syllabus_2`, etc.
Paste your syllabus text into cell **A1** of each tab.

> **Google Drive tip:** Upload your PDF syllabi to Google Drive. Open them with Google Docs (right-click → Open with → Google Docs). Copy all the text. Paste into your Syllabus tab.

### Step 5 — Run
Click **SyllaClaw** in the menu bar and choose:
- **4. Full Run (Steps 1–3)** to do everything at once

Or run each step individually:
1. **1. Parse My Syllabi** — extracts all deadlines
2. **2. Build My Week** — builds your time-blocked schedule
3. **3. Push to Google Calendar** — creates real calendar events instantly

No CSV import needed with Apps Script — events appear in Google Calendar the moment you click Step 3.

---

## Work Schedule Format

Create a file called `work_schedule.txt` (CLI) or a `Work Schedule` sheet tab (Apps Script) with your shifts:

```
Monday:    OFF
Tuesday:   4:00 PM - 9:00 PM  (5 hrs)
Wednesday: OFF
Thursday:  4:00 PM - 9:00 PM  (5 hrs)
Friday:    OFF
Saturday:  8:00 AM - 2:00 PM  (6 hrs)
Sunday:    10:00 AM - 3:00 PM (5 hrs)
```

SyllaClaw will never schedule study time during your work shifts.

---

## How the schedule is built

SyllaClaw uses NVIDIA's Llama-3.3-Nemotron-Super model to reason over your deadlines and build your week. Here is what it considers:

- **Work shifts** — locked as non-negotiable
- **Deadline urgency** — more study time allocated closer to due dates
- **Study block sizing** — 25-minute Pomodoro blocks for memorization, 90-minute deep work blocks for problem sets
- **Sleep** — consistent wake and bedtime every day
- **Meals** — breakfast, lunch, dinner built in
- **Family calls** — 10-minute "Call home" blocks 2–3 times per week
- **Free time** — protected social and rest time, not filled with work
- **Weekly review** — Sunday evening planning block

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `NIM_API_KEY not set` | Add your key to `.env` or run `export NIM_API_KEY=nvapi-xxxx` |
| `No text extracted from PDF` | Your PDF is a scanned image. Open it in Google Docs to get text, then save as `.txt` |
| `No deadlines found` | Make sure your syllabus contains dates and assignment names |
| Timeout on first run | NIM can be slow on the first cold call — the tool retries automatically. Wait. |
| Apps Script: `NIM API error 401` | Your API key is wrong or not set in CONFIG |
| Apps Script: No SyllaClaw menu | Reload the Sheet after saving the script |

---

## Project structure

```
syllaclaw/
├── syllaclaw.py              # Main entry point
├── src/
│   ├── agent.py              # Main orchestrator
│   ├── nim_client.py         # All NVIDIA API calls
│   ├── reader.py             # PDF/DOCX/TXT extraction
│   ├── schedule.py           # Conflict detection, schedule logic
│   ├── exporter.py           # Google Calendar CSV export
│   └── display.py            # Terminal colors and logging
├── scripts/
│   └── SyllaClaw.gs          # Google Apps Script implementation
├── syllabi/
│   ├── samples/              # Sample syllabi for demo mode
│   └── (drop your files here)
├── output/                   # Generated CSV files
├── requirements.txt
├── .env.example
└── README.md
```

---

## The stack

| Component | Role | Cost |
|-----------|------|------|
| NVIDIA NIM | Parses syllabi, builds schedule, writes briefing | Free tier |
| Google Calendar API / Apps Script | Creates real calendar events | Free |
| Apache Airflow (optional) | Runs weekly Sunday briefing automatically | Free |
| Python / Apps Script | Orchestration | Free |

---

## Built by

**Chanel Power** — Senior ML Engineer, Founder of [Mentor Me Collective](https://mentormecollective.org)

- GitHub: [@itsChanelML](https://github.com/itsChanelML)
- LinkedIn: [Chanel Power](https://linkedin.com/in/chanelpower)
- Community: [mentormecollective.org](https://mentormecollective.org)

---

*Drop your syllabus. Get your life.*