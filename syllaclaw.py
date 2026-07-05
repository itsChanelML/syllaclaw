#!/usr/bin/env python3
"""
SyllaClaw — Academic Life Management Agent
==========================================
Drop your syllabi in a folder. Run one command.
Get your entire semester organized in Google Calendar.

Usage:
  python3 syllaclaw.py                    # reads syllabi/ folder
  python3 syllaclaw.py --folder ./myfiles # custom folder
  python3 syllaclaw.py --demo             # runs on sample syllabi
  python3 syllaclaw.py --break            # ESCALATE demo beat

Requirements:
  pip3 install -r requirements.txt
  NIM_API_KEY in your .env file (free at build.nvidia.com)

Output:
  output/weekly_schedule.csv   → import directly to Google Calendar
  output/semester_deadlines.csv → full deadline list

Free to use. Free to run. Open source.
github.com/itsChanelML/syllaclaw
"""

import argparse
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).parent

# Add src to path
sys.path.insert(0, str(ROOT / "src"))

from agent import SyllaClawAgent
from display import banner, log_t, log_g, log_r, log_gr, TEAL, RESET, BOLD, AMBER

def main():
    parser = argparse.ArgumentParser(
        description="SyllaClaw — Drop your syllabus. Get your life.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 syllaclaw.py                       # reads syllabi/ folder
  python3 syllaclaw.py --folder ./my_docs    # custom folder
  python3 syllaclaw.py --demo                # sample syllabi
  python3 syllaclaw.py --break               # ESCALATE demo beat
  python3 syllaclaw.py --name "Alex Rivera"  # personalize output
        """
    )
    parser.add_argument("--folder",  type=str, default=str(ROOT / "syllabi"),
                        help="Folder containing your syllabus files (PDF, DOCX, TXT)")
    parser.add_argument("--name",    type=str, default=os.environ.get("STUDENT_NAME", "Student"),
                        help="Your name (for personalized output)")
    parser.add_argument("--email",   type=str, default=os.environ.get("STUDENT_EMAIL", ""),
                        help="Your email (for the CSV import)")
    parser.add_argument("--demo",    action="store_true", help="Run on sample syllabi")
    parser.add_argument("--break",   dest="broken", action="store_true",
                        help="Demo ESCALATE beat — simulates a broken syllabus file")
    parser.add_argument("--week",    type=str, default="",
                        help="Target week start date YYYY-MM-DD (default: next Monday)")
    parser.add_argument("--output",  type=str, default=str(ROOT / "output"),
                        help="Output folder for CSV files")
    args = parser.parse_args()

    # Check API key
    api_key = os.environ.get("NIM_API_KEY")
    if not api_key:
        print(f"\n{BOLD}Error: NIM_API_KEY not set.{RESET}")
        print(f"  Get your free key at: https://build.nvidia.com")
        print(f"  Then: export NIM_API_KEY=nvapi-xxxx")
        print(f"  Or add it to your .env file.\n")
        sys.exit(1)

    # Demo mode — use sample syllabi
    if args.demo or args.broken:
        folder = ROOT / "syllabi" / "samples"
        if args.broken:
            folder = ROOT / "syllabi" / "samples_broken"
        if not folder.exists():
            log_r("Sample syllabi not found. Run: python3 setup_samples.py")
            sys.exit(1)
        args.folder = str(folder)

    # Run the agent
    agent = SyllaClawAgent(
        api_key=api_key,
        student_name=args.name,
        student_email=args.email,
        output_dir=Path(args.output),
        week_start=args.week,
    )

    agent.run(folder=Path(args.folder))


if __name__ == "__main__":
    main()