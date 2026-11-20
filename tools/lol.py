#!/usr/bin/env python3
"""Find and run an original Lands of Lore file tool."""
from argparse import RawDescriptionHelpFormatter
from pathlib import Path
import subprocess
import sys

from cli_errors import ReaderArgumentParser, run_cli

JOBS = {
    "level": ("level_viewer.py", (), "Look at an interactive level plan"),
    "text": ("decode_dialogue.py", (), "Read a dialogue or language table"),
    "music": ("xmi_to_midi.py", (), "Convert one XMIDI music member to MIDI"),
    "save": ("save_edit.py", (), "Edit a copy of a saved game"),
    "patch": ("patch.py", (), "Make or apply a patch and its undo"),
    "mod": ("modkit.py", (), "Unpack or build an editable workspace"),
}


def main():
    menu = "\n".join(f"  {name:7} {spec[2]}" for name, spec in JOBS.items())
    parser = ReaderArgumentParser(
        description="Choose a job for your copy of the original game.",
        usage="python tools/lol.py JOB [OPTIONS]",
        epilog="Jobs\n" + menu + "\n\nUse python tools/lol.py JOB --help for the job's options.",
        formatter_class=RawDescriptionHelpFormatter,
    )
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        parser.print_help()
        return 0
    if args[0] not in JOBS:
        parser.error(f"Unknown job {args[0]}. Run python tools/lol.py to see the choices.")
    job, options = args[0], args[1:]
    script, prefix, label = JOBS[job]
    if not options or options[-1] in ("-h", "--help"):
        print(f"{label}. Use python tools/lol.py {job} [OPTIONS].", flush=True)
    program = Path(__file__).resolve().with_name(script)
    return subprocess.run([sys.executable, str(program), *prefix, *(options or ["--help"])]).returncode


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
