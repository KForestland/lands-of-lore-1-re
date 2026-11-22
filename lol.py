"""Run the Lands of Lore file tools from the repository root."""
from pathlib import Path
import sys
from runpy import run_path

if __name__ == "__main__":
    tools = Path(__file__).resolve().with_name("tools")
    sys.path.insert(0, str(tools))
    run_path(str(tools / "lol.py"), run_name="__main__")
