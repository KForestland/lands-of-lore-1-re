# First ten minutes

Draw a level from your own installed copy of Lands of Lore I.
You need Python 3.10 or later, the Pillow package and a web browser.

## Find your game files

Open the folder for your own copy of the game in your file manager.

- **CD edition:** open `DATA`. Use the folder that contains both `L01.PAK` and `GENERAL.PAK` directly.
- **Floppy edition:** use the installation folder that contains both `CHAPTER8.PAK` and `GENERAL.PAK` directly.

If you have both editions, either works. Start with the CD's `DATA` folder.
If you have several copies of an edition, use the one you normally play.

If a search finds several copies of `GENERAL.PAK`, use the one next to the
edition's marker above. The CD's language folders and demos can have their
own `GENERAL.PAK`. Lowercase names such as `l01.pak` also work. Copy the
full path of the folder itself.

## Download the tools

On the [repository page](https://github.com/KForestland/lands-of-lore-1-re),
choose **Code**, then **Download ZIP**. Extract the whole ZIP to your
Downloads folder. The tools folder should be inside the extracted
repository folder alongside `README.md`. The commands below assume the
extracted folder is `lands-of-lore-1-re-main`. Use the folder name you see
if it differs.

## Windows

Open **Windows PowerShell** from the Start menu. Run `py -3 --version`.
If the command is missing or the version is below 3.10, install a
current Python 3 release with the Python launcher, then reopen PowerShell.
[Python for Windows](https://www.python.org/downloads/windows/)

Run this line, then paste the folder path when PowerShell asks for it.

```powershell
$data = (Read-Host 'Paste the path to your game folder').Trim('"')
```

Then paste these lines.

```powershell
Set-Location "$HOME\Downloads\lands-of-lore-1-re-main"
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
.\.venv\Scripts\python.exe tools/level_renderer.py --data "$data" --level level01 --schematic --out "$out\schematic"
Start-Process "$out\schematic\level01_schematic.png"
```

## Linux

Open a terminal. If `python3 --version` reports a version below 3.10,
install a newer Python with your distribution's package manager. On Ubuntu or Debian, `sudo apt install python3-venv` installs the venv module.
Run this line, paste the folder path and press Enter again.

```sh
IFS= read -r data
```

Then paste these lines.

```sh
cd "$HOME/Downloads/lands-of-lore-1-re-main"
out="$HOME/Downloads/LoL1 output"
mkdir -p "$out"
python3 -m venv .venv
.venv/bin/python -m pip install Pillow
.venv/bin/python tools/level_renderer.py --data "$data" --level level01 --schematic --out "$out/schematic"
xdg-open "$out/schematic/level01_schematic.png"
```

Light squares are open floor, dark squares have walls on all four sides, and orange squares have some walls. Red marks sit on decorated faces.
If the tool cannot find a game file, check the markers in
[Find your game files](#find-your-game-files). If no window opens, open
`level01_schematic.png` from the schematic folder in a browser on your desktop.

To draw the picture again, choose a new schematic folder name in both lines.

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

[Edit walls and item placements](LEVEL_EDITOR.md) when you are ready to make a copy.

## Find another job

Use the same Python command with `tools/lol.py` to list the jobs.
Add a job name and `--help` for its options.
[Interactive plans](COOKBOOK.md#open-an-interactive-level-plan)
