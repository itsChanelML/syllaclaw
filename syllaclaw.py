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
  python3 syllaclaw.py --checkin          # Sunday check-in — update your profile

Requirements:
  pip3 install -r requirements.txt
  NIM_API_KEY in your .env file (free at build.nvidia.com)

Output:
  output/weekly_schedule.csv    → import directly to Google Calendar
  output/semester_deadlines.csv → full deadline list
  output/conflict_report.csv    → heavy weeks and reschedule suggestions
  output/student_profile.json   → your behavioral profile (created after first --checkin)

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
  python3 syllaclaw.py --demo                # run on sample syllabi
  python3 syllaclaw.py --break               # trigger ESCALATE demo beat
  python3 syllaclaw.py --name "Alex Rivera"  # personalize output
  python3 syllaclaw.py --checkin             # Sunday check-in
        """
    )
    parser.add_argument("--folder",   type=str, default=str(ROOT / "syllabi"),
                        help="Folder containing your syllabus files (PDF, DOCX, TXT)")
    parser.add_argument("--name",     type=str, default=os.environ.get("STUDENT_NAME", "Student"),
                        help="Your name (for personalized output)")
    parser.add_argument("--email",    type=str, default=os.environ.get("STUDENT_EMAIL", ""),
                        help="Your email (for the CSV import)")
    parser.add_argument("--demo",     action="store_true", help="Run on sample syllabi")
    parser.add_argument("--break",    dest="broken", action="store_true",
                        help="Demo ESCALATE beat — simulates a broken syllabus file")
    parser.add_argument("--checkin",  action="store_true",
                        help="Sunday evening check-in — tell SyllaClaw how your week went. Creates/updates output/student_profile.json")
    parser.add_argument("--week",     type=str, default="",
                        help="Target week start date YYYY-MM-DD (default: next Monday)")
    parser.add_argument("--output",   type=str, default=str(ROOT / "output"),
                        help="Output folder for CSV files")
    args = parser.parse_args()

    # ── Check-in mode — no API key required ───────────────────────────────────
    if args.checkin:
        _run_checkin(
            student_name=args.name,
            output_dir=Path(args.output),
        )
        return

    # ── API key required for all other modes ──────────────────────────────────
    api_key = os.environ.get("NIM_API_KEY")
    if not api_key:
        print(f"\n{BOLD}Error: NIM_API_KEY not set.{RESET}")
        print(f"  Get your free key at: https://build.nvidia.com")
        print(f"  Then: export NIM_API_KEY=nvapi-xxxx")
        print(f"  Or add it to your .env file.\n")
        sys.exit(1)

    # ── Demo / ESCALATE mode ──────────────────────────────────────────────────
    if args.demo or args.broken:
        folder = ROOT / "syllabi" / ("samples_broken" if args.broken else "samples")
        if not folder.exists():
            log_r(f"Sample folder not found: {folder}")
            log_r("Make sure syllabi/samples/ and syllabi/samples_broken/ exist.")
            sys.exit(1)
        args.folder = str(folder)

    # ── Run the agent ─────────────────────────────────────────────────────────
    agent = SyllaClawAgent(
        api_key=api_key,
        student_name=args.name,
        student_email=args.email,
        output_dir=Path(args.output),
        week_start=args.week,
    )

    agent.run(folder=Path(args.folder))


def _run_checkin(student_name: str, output_dir: Path):
    """
    Sunday evening check-in.
    Loads or creates student_profile.json, asks 5 questions,
    saves updated profile. No API key needed.
    """
    from memory import load_profile, run_checkin as do_checkin, save_profile

    output_dir.mkdir(parents=True, exist_ok=True)

    # Override default profile path to use the output dir
    import memory as mem_module
    mem_module.PROFILE_FILE = output_dir / "student_profile.json"

    profile = load_profile(student_name=student_name)
    updated = do_checkin(profile)
    save_profile(updated)

    print(f"\n  Profile saved to: {mem_module.PROFILE_FILE}")
    print(f"  Run python3 syllaclaw.py to build next week with your updated profile.\n")


if __name__ == "__main__":
    main()