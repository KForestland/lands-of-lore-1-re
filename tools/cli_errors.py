"""Command-line diagnostics shared by the file readers."""
import argparse
import os
import struct
import sys
from pathlib import Path


def one_line(message):
    return " ".join(str(message).splitlines()).strip()


class ReaderArgumentParser(argparse.ArgumentParser):
    def parse_args(self, args=None, namespace=None):
        options = super().parse_args(args, namespace)
        for name in ("data", "game_dat"):
            folder = getattr(options, name, None)
            if isinstance(folder, (str, os.PathLike)) and not Path(folder).is_dir():
                self.error(f"game data folder does not exist: {folder}")
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
    except (OSError, EOFError, ValueError, struct.error, IndexError, KeyError) as error:
        message = one_line(error) or type(error).__name__
        print(f"{Path(sys.argv[0]).name}: {message}", file=sys.stderr)
        return 1
