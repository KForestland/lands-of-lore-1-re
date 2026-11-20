# First ten minutes

Draw a level from your own installed copy of Lands of Lore I.
You need Python 3.10 or later with the Pillow package, a web browser, and the
game's `DATA` folder. Find the folder containing `GENERAL.PAK`.
For the floppy edition, the folder containing `GENERAL.PAK` may be the installation folder itself.

## Download the tools

On the [repository page](https://github.com/KForestland/lands-of-lore-1-re),
choose **Code**, then **Download ZIP**. Extract the whole ZIP to your
Downloads folder. The tools folder should be inside the extracted
repository folder alongside `README.md`. The commands below assume the
extracted folder is `lands-of-lore-1-re-main`. Use the folder name you see
if it differs.

## Windows

Open **Windows PowerShell** from the Start menu. Run `py -3 --version`.
If the command is missing or the version is below 3.8, install a
current Python 3 release with the Python launcher, then reopen PowerShell.
[Python for Windows](https://www.python.org/downloads/windows/)

Paste these lines, replacing the path after `$data =` with
the folder you found above. Keep the quotation marks around paths.

```powershell
Set-Location "$HOME\Downloads\lands-of-lore-1-re-main"
$data = 'C:\Games\Lands of Lore I\DATA'
$out = "$HOME\Downloads\LoL1 output"
New-Item -ItemType Directory -Force "$out" | Out-Null
```

Prepare a Python environment and install Pillow once.

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install Pillow
```

Draw the level and open the picture.

```powershell
.\.venv\Scripts\python.exe tools/level_renderer.py --data "$data" --level 1 --schematic --out "$out"
Start-Process "$out\level01_schematic.png"
```

## Linux

Open a terminal. If `python3 --version` reports a version below 3.8,
install a newer Python with your distribution's package manager. On Ubuntu or Debian, `sudo apt install python3-venv` installs the venv module.
Paste these lines, replacing the path after `data=` with the folder you
found above.

```sh
cd "$HOME/Downloads/lands-of-lore-1-re-main"
data="$HOME/Games/Lands of Lore I/DATA"
out="$HOME/Downloads/LoL1 output"
mkdir -p "$out"
python3 -m venv .venv
.venv/bin/python -m pip install Pillow
.venv/bin/python tools/level_renderer.py --data "$data" --level 1 --schematic --out "$out"
xdg-open "$out/level01_schematic.png"
```

You should see a grid of light floor squares, dark walls, and orange wall features.
If the tool cannot find a game file, check that the path points to the
folder containing `GENERAL.PAK`. If the open command fails, open
`level01_schematic.png` from the output folder in your browser.

[More recipes](COOKBOOK.md) · [Terms used in the guides](GLOSSARY.md)

## Open an interactive level plan

Use a new subfolder of the output folder you created above.

Windows PowerShell

```powershell
.\.venv\Scripts\python.exe tools/lol.py level --data "$data" --out "$out\plans"
Start-Process "$out\plans\level01.html"
```

Linux

```sh
.venv/bin/python tools/lol.py level --data "$data" --out "$out/plans"
xdg-open "$out/plans/level01.html"
```

Click a square or a marker to see its details. Turn on **Map numbers**
to show the placement numbers. To repeat the command, choose a new
subfolder such as `plans-2` in both lines.

## Find another job

Use the same Python command with `tools/lol.py` to list the jobs.
Add a job name and `--help` for its options.
[Interactive plans](COOKBOOK.md#open-an-interactive-level-plan)
