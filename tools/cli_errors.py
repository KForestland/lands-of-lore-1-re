"""Command-line diagnostics shared by the file readers."""
import argparse
import os
import struct
import sys
from pathlib import Path


def one_line(message):
    return " ".join(str(message).splitlines()).strip()


REPOSITORY = Path(__file__).resolve().parents[1]
# Options through which a tool writes a file or a folder of files.
OUTPUT_OPTIONS = ("out", "out_dir", "walls_png")


def holds_game_data(folder):
    """True when folder or a folder above it holds a game archive (PAK or TLK)."""
    for place in (folder, *folder.parents):
        try:
            if any(entry.suffix.upper() in (".PAK", ".TLK") for entry in place.iterdir()):
                return True
        except OSError:
            continue
    return False


def output_refusal(path, data=None, repository=False):
    """Why a tool may not write path (a file or a folder), or None. Refused: the
    --data folder and anything below it, any folder holding a PAK or TLK archive
    or lying below one, and, with repository=True, this repository."""
    target = Path(path).resolve()
    roots = [REPOSITORY] if repository else []
    if isinstance(data, (str, os.PathLike)):
        roots.append(Path(data).resolve())
    if any(root == target or root in target.parents for root in roots) or holds_game_data(target):
        where = "the game data and repository" if repository else "the game data"
        return f"give an output path outside {where}: {path}"
    return None


class ReaderArgumentParser(argparse.ArgumentParser):
    def parse_args(self, args=None, namespace=None):
        options = super().parse_args(args, namespace)
        for name in ("data", "game_dat"):
            folder = getattr(options, name, None)
            if isinstance(folder, (str, os.PathLike)) and not Path(folder).is_dir():
                self.error(f"game data folder does not exist: {folder}")
        for name in OUTPUT_OPTIONS:
            path = getattr(options, name, None)
            if isinstance(path, (str, os.PathLike)) and str(path):
                refusal = output_refusal(path, getattr(options, "data", None))
                if refusal:
                    self.error(refusal)
        return options

    def error(self, message):
        self.exit(2, message)

    def exit(self, status=0, message=None):
        if message:
            message = one_line(message)
            print(f"{self.prog}: {message}", file=sys.stderr)
        super().exit(status)


def run_cli(main, *args):
    try:
        result = main(*args)
        sys.stdout.flush()
        return result
    except BrokenPipeError:
        # Flush can fail again during interpreter shutdown after a pipe closes.
        with open(os.devnull, "w") as sink:
            os.dup2(sink.fileno(), sys.stdout.fileno())
        return 0
    except (OSError, EOFError, ImportError, ValueError, struct.error, IndexError, KeyError) as error:
        message = one_line(error) or type(error).__name__
        print(f"{Path(sys.argv[0]).name}: {message}", file=sys.stderr)
        return 1
