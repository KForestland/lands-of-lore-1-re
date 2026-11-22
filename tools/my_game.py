"""Build an offline page from a player's own Lands of Lore installation."""
import argparse
from base64 import b64encode
from html import escape
from io import BytesIO
import os
from pathlib import Path
from struct import error as StructError
import sys
from tempfile import mkdtemp
import webbrowser

from cli_errors import output_refusal
from edition import identify, WITNESSES
from exe_tables import find_images, OFFSETS, spell_names, spells
from game_names import map_names
from level_html import find_data
from level_renderer import level_numbers, render_schematic
from level_report import item_names


TITLE = "Lands of Lore · My Game"
WRONG_FOLDER = "Choose the folder containing your complete Lands of Lore game or its DATA folder."

STYLE = """
:root{font:17px/1.5 system-ui,sans-serif;color:#282923;background:#f8f5ec}
*{box-sizing:border-box}
body{max-width:78rem;margin:auto;padding:1.5rem clamp(1rem,4vw,3rem) 3rem}
h1,h2,h3{font-family:Georgia,serif;line-height:1.15}
h1{font-size:clamp(2rem,5vw,3.5rem);margin:0}
h2{font-size:1.85rem;margin-bottom:.5rem}
h3{margin:0}
a{color:#713712;text-decoration-thickness:1px;text-underline-offset:.2em}
header{border-bottom:1px solid #c8beaa;padding-block:.7rem 1.4rem}
header p{margin:.5rem 0 0}
nav,.legend,.jump{display:flex;align-items:center;flex-wrap:wrap;gap:.35rem 1rem}
nav{margin-top:1.2rem;font-weight:650}nav a{padding-block:.3rem}
section{margin-top:1.8rem}.legend{list-style:none;padding:0}
.legend span{display:inline-block;width:1rem;height:1rem;vertical-align:-.12em;margin-right:.4rem;border:1px solid #514b3e}
.levels{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,16rem),1fr));gap:1rem;margin-top:1rem}
article{background:#fffdf8;border:1px solid #c8beaa;border-radius:.45rem;padding:.8rem;scroll-margin-top:1rem}
article:target{outline:3px solid #713712}
article img{display:block;width:100%;height:auto;margin-top:.65rem;image-rendering:pixelated;border:1px solid #777466}
.catalogues{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,23rem),1fr));gap:1.5rem}
.scroller{overflow:auto;max-height:29rem;border:1px solid #c8beaa;background:#fffdf8;border-radius:.45rem}
table{width:100%;border-collapse:collapse}
th,td{padding:.4rem .65rem;text-align:left;border-bottom:1px solid #ded5c4}
th{background:#efe6d5;position:sticky;top:0}
label{display:block;margin-bottom:.55rem}
input[type=search]{background:#fffdf8;color:inherit;font:inherit;padding:.25rem .5rem;border:1px solid #867a62;border-radius:.3rem}
:focus-visible{outline:3px solid #713712;outline-offset:2px}
"""

SCRIPT = """
for (const search of document.querySelectorAll('[data-search]')) {
    const rows = document.querySelectorAll('#' + search.dataset.search + ' tbody tr');
    search.addEventListener('input', () => {
        const query = search.value.trim().toLocaleLowerCase();
        for (const row of rows) row.hidden = !row.textContent.toLocaleLowerCase().includes(query);
    });
}
"""


class GameFolderError(ValueError):
    """The selection does not contain the files needed for the page."""


def edition_label(fingerprints, image):
    for label, expected in WITNESSES.items():
        if all(fingerprints.get(name) == value for name, value in expected.items()):
            return label
    layout = "Floppy" if image == "floppy" else "CD"
    return f"{layout} edition layout (exact version unverified)"


def map_card(level, data, name):
    with BytesIO() as stream:
        render_schematic(level, data).save(stream, format="PNG")
        image = b64encode(stream.getvalue()).decode("ascii")
    return (
        f'<article id="level-{level}"><h3>{escape(name)}</h3>'
        f'<img src="data:image/png;base64,{image}" loading="lazy" '
        f'width="320" height="320" alt="Overhead plan of {escape(name)}"></article>'
    )


def catalogue(key, title, columns, rows):
    headings = "".join(f'<th scope="col">{escape(column)}</th>' for column in columns)
    body = "".join(
        "<tr>" + "".join(f"<td>{escape(str(cell))}</td>" for cell in row) + "</tr>" for row in rows
    )
    return (
        f'<section id="{key}"><h2>{title}</h2>'
        f'<label>Search {title.lower()} <input type="search" data-search="{key}"></label>'
        f'<div class="scroller" tabindex="0" role="region" aria-label="{title} table"><table>'
        f'<thead><tr>{headings}</tr></thead><tbody>{body}</tbody></table></div></section>'
    )


def spell_catalogue(data, image, program):
    name_of = spell_names(data, "ENG")
    for slot, record in enumerate(spells(program, OFFSETS["spells"][image])):
        if not (name := name_of(record["name id"])):
            continue
        mana = " / ".join(map(str, record["MP"]))
        health = " / ".join(map(str, record["HP"]))
        yield name, slot, mana, health


def game_page(folder):
    try:
        data = find_data(folder, "DATA", "GENERAL.PAK")
        _, fingerprints = identify(data)
        images = find_images(data)
        if not images and data.name.upper() == "DATA":
            images = find_images(data.parent)
        if not images:
            raise GameFolderError(WRONG_FOLDER)
        image, _, _, program = images[0]
        label = edition_label(fingerprints, image)
        items, lands = item_names(data)
        spell_rows = list(spell_catalogue(data, image, program))
        if not items or not spell_rows:
            raise GameFolderError(WRONG_FOLDER)
        levels = level_numbers("all")
        titles = map_names(image, program, lands)
        maps = "\n".join(map_card(level, data, titles.get(level, f"Level {level}")) for level in levels)
    except (ValueError, OSError, StructError, IndexError, KeyError) as error:
        raise GameFolderError(WRONG_FOLDER) from error

    jump = " ".join(
        f'<a href="#level-{level}">{escape(titles.get(level, f"Level {level}"))} ({level})</a>'
        if level in titles else f'<a href="#level-{level}">Level {level}</a>'
        for level in levels
    )
    item_table = catalogue("items", "Items", ("Name", "Item ID"),
                           ((name, number) for number, name in sorted(items.items(), key=lambda row: row[1].casefold())))
    spell_table = catalogue("spells", "Spells", ("Name", "Slot", "MP by rank", "HP by rank"), spell_rows)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{TITLE}</title>
<style>{STYLE}</style>
</head>
<body>
<header>
<h1>{TITLE}</h1>
<p>Edition: <strong>{escape(label)}</strong></p>
<nav aria-label="Page sections"><a href="#maps">Level plans</a><a href="#items">Items</a><a href="#spells">Spells</a></nav>
</header>
<main>
<section id="maps">
<h2>Level plans</h2>
<details>
<summary>Jump to a level</summary>
<nav class="jump" aria-label="Jump to level">{jump}</nav>
</details>
<ul class="legend" aria-label="Map legend">
<li><span style="background:#ebe8dc"></span>Open square</li>
<li><span style="background:#282830"></span>Solid wall</li>
<li><span style="background:#e69632"></span>Partial wall, door or switch</li>
<li><span style="background:#c81e1e"></span>Decoration</li>
</ul>
<div class="levels">{maps}</div>
</section>
<div class="catalogues">{item_table}{spell_table}</div>
</main>
<script>{SCRIPT}</script>
</body>
</html>
"""


def cache_folder():
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA") or Path.home() / "AppData" / "Local")
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Caches"
    else:
        base = Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache")
    return base / "LoL1 My Game"


def write_page(folder, out=None, *, open_page=True):
    page = game_page(folder)
    folder = folder.resolve()
    game_root = folder.parent if folder.name.upper() == "DATA" else folder
    if out is None:
        cache = cache_folder()
        if output_refusal(cache, game_root):
            raise ValueError("The My Game cache must be outside the game folder.")
        cache.mkdir(parents=True, exist_ok=True)
        out = Path(mkdtemp(prefix="report-", dir=cache)) / "My Game.html"
    if output_refusal(out, game_root):
        raise ValueError("Save the My Game page outside the game folder.")
    with out.open("x", encoding="utf-8") as stream:
        try:
            stream.write(page)
        except OSError:
            stream.close()
            out.unlink(missing_ok=True)
            raise
    if open_page and not webbrowser.open(out.resolve().as_uri()):
        raise ValueError(f"Open the My Game page in your browser from {out}.")
    return out


def desktop():
    from tkinter import TclError, Tk, filedialog, messagebox

    try:
        window = Tk()
    except TclError as error:
        raise ValueError("Open My Game from your desktop to choose a game folder.") from error
    window.withdraw()
    try:
        while folder := filedialog.askdirectory(parent=window, title="Choose your Lands of Lore game folder"):
            try:
                write_page(Path(folder))
                return 0
            except GameFolderError as error:
                messagebox.showerror(TITLE, str(error), parent=window)
            except (OSError, ValueError, ImportError) as error:
                messagebox.showerror(TITLE, str(error), parent=window)
                return 1
        return 0
    finally:
        window.destroy()


def main(argv=None):
    parser = argparse.ArgumentParser(prog="lol.py mygame", description=__doc__)
    parser.add_argument("--data", type=Path, help="use a game folder without opening the folder picker")
    parser.add_argument("--out", type=Path, help="save to a new HTML file at this path")
    parser.add_argument("--no-browser", action="store_true", help="save the page without opening the browser")
    args = parser.parse_args(argv)
    if args.data is None and (args.out or args.no_browser):
        parser.error("Use --data with --out or --no-browser.")
    try:
        if args.data is None:
            return desktop()
        path = write_page(args.data, args.out, open_page=not args.no_browser)
        if sys.stdout is not None:
            print(path)
        return 0
    except (OSError, ValueError, ImportError) as error:
        if sys.stderr is not None:
            print(f"{parser.prog}: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
