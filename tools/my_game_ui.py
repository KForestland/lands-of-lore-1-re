"""Shared window and offline report for the three Lands of Lore guides."""
import argparse
from base64 import b64encode
from collections.abc import Callable
from dataclasses import dataclass
from html import escape
from io import BytesIO
from itertools import count
from pathlib import Path
from struct import error as StructError
import sys
import webbrowser

from cli_errors import output_refusal


CANCELLED = "No folder was chosen, so no page was written."
DATA_ERRORS = (ValueError, OSError, StructError, IndexError, KeyError)


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
    """The folder does not contain the files needed for the page."""


class LanguageError(ValueError):
    """The selected name language is absent from the game files."""


def edition_label(data, identify, witnesses, fallback):
    _, fingerprints = identify(data)
    for label, expected in witnesses.items():
        if all(fingerprints.get(name) == value for name, value in expected.items()):
            return label
    return fallback


def png_bytes(image):
    with BytesIO() as stream:
        image.save(stream, format="PNG")
        return stream.getvalue()


def maps_section(maps, legend=""):
    jumps, cards = [], []
    for key, title, image, format in maps:
        anchor, name = escape(f"level-{key}"), escape(title)
        jumps.append(f'<a href="#{anchor}">{name}</a>')
        encoded = b64encode(image).decode("ascii")
        cards.append(
            f'<article id="{anchor}"><h3>{name}</h3>'
            f'<img src="data:image/{format};base64,{encoded}" loading="lazy" '
            f'alt="Overhead plan of {name}"></article>'
        )
    return (
        '<section id="maps"><h2>Level plans</h2><details><summary>Jump to a level</summary>'
        f'<nav class="jump" aria-label="Jump to level">{" ".join(jumps)}</nav></details>'
        f'{legend}<div class="levels">{"".join(cards)}</div></section>'
    )


def catalogue(key, title, columns, rows, description=""):
    headings = "".join(f'<th scope="col">{escape(column)}</th>' for column in columns)
    body = "".join(
        "<tr>" + "".join(f"<td>{escape(str(cell))}</td>" for cell in row) + "</tr>" for row in rows
    )
    intro = f"<p>{escape(description)}</p>" if description else ""
    return (
        f'<section id="{key}"><h2>{escape(title)}</h2>{intro}'
        f'<label>Search {escape(title.lower())} <input type="search" data-search="{key}"></label>'
        f'<div class="scroller" tabindex="0" role="region" aria-label="{escape(title)} table"><table>'
        f'<thead><tr>{headings}</tr></thead><tbody>{body}</tbody></table></div></section>'
    )


def report(title, edition, maps, tables, *, legend="", note="", extras=()):
    sections = (("maps", "Level plans", maps_section(maps, legend)), *tables, *extras)
    nav = "".join(f'<a href="#{key}">{escape(label)}</a>' for key, label, _ in sections)
    main = sections[0][2] + '<div class="catalogues">' + "".join(row[2] for row in tables) + '</div>'
    main += "".join(row[2] for row in extras)
    note = f"<p>{escape(note)}</p>" if note else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)}</title>
<style>{STYLE}</style>
</head>
<body>
<header>
<h1>{escape(title)}</h1>
<p>Edition: <strong>{escape(edition)}</strong></p>
{note}<nav aria-label="Page sections">{nav}</nav>
</header>
<main>{main}</main>
<script>{SCRIPT}</script>
</body>
</html>
"""


def documents_folder():
    if sys.platform == "win32":
        from ctypes import create_unicode_buffer, windll
        from ctypes.wintypes import MAX_PATH

        # CSIDL_PERSONAL selects the user's Documents folder, including redirects.
        path = create_unicode_buffer(MAX_PATH)
        if windll.shell32.SHGetFolderPathW(None, 0x0005, None, 0, path) == 0:
            return Path(path.value)
    return Path.home() / "Documents"


def write_new_file(out, game_root, page):
    if output_refusal(out, game_root):
        raise ValueError("Save the My Game page outside the game folder.")
    stream = out.open("x", encoding="utf-8")
    try:
        with stream:
            stream.write(page)
    except OSError:
        out.unlink(missing_ok=True)
        raise


def save_in_documents(game_root, page, filename):
    documents = documents_folder().resolve()
    if output_refusal(documents, game_root):
        raise ValueError("Save the My Game page outside the game folder.")
    documents.mkdir(parents=True, exist_ok=True)
    for number in count(1):
        name = f"{filename}.html" if number == 1 else f"{filename} {number}.html"
        out = documents / name
        try:
            write_new_file(out, game_root, page)
        except FileExistsError:
            continue
        return out


def open_report(path):
    try:
        return webbrowser.open(path.resolve().as_uri())
    except (OSError, webbrowser.Error):
        return False


def choose_language(window, choices):
    from tkinter import StringVar, simpledialog, ttk

    class LanguageDialog(simpledialog.Dialog):
        def body(self, parent):
            ttk.Label(parent, text="Which language do you play in?").pack(padx=12, pady=6)
            self.selected = StringVar(parent, next(iter(choices.values())))
            box = ttk.Combobox(parent, textvariable=self.selected, values=tuple(choices.values()), state="readonly")
            box.pack(padx=12, pady=6)
            return box

        def apply(self):
            self.result = next(code for code, name in choices.items() if name == self.selected.get())

    return LanguageDialog(window, "Names in My Game").result


@dataclass(frozen=True)
class MyGame:
    filename: str
    title: str
    game: str
    data_folder: str
    read_page: Callable[..., str]
    languages: tuple = ()
    language_options: Callable[[Path], dict[str, str]] | None = None

    @property
    def wrong_folder(self):
        return f"Choose the folder containing your complete {self.game} game or its {self.data_folder} folder."

    def write_page(self, folder, out=None, *, open_page=True, language=None):
        try:
            if self.languages:
                page = self.read_page(folder, language)
            else:
                page = self.read_page(folder)
        except LanguageError:
            raise
        except DATA_ERRORS as error:
            raise GameFolderError(self.wrong_folder) from error
        folder = folder.resolve()
        game_root = folder
        if folder.name.upper() == self.data_folder:
            game_root = folder.parent
        elif self.languages and folder.name.upper() in self.languages:
            game_root = folder.parent
            if game_root.name.upper() == self.data_folder:
                game_root = game_root.parent
        if out is None:
            out = save_in_documents(game_root, page, self.filename)
        else:
            write_new_file(out, game_root, page)
        if open_page and not open_report(out):
            raise ValueError(f"Open the My Game page in your browser from {out}.")
        return out

    def desktop(self):
        from tkinter import TclError, Tk, filedialog, messagebox

        try:
            window = Tk()
        except TclError as error:
            raise ValueError("Open My Game from your desktop to choose a game folder.") from error
        window.withdraw()
        try:
            while folder := filedialog.askdirectory(parent=window, title=f"Choose your {self.game} folder"):
                try:
                    selected = Path(folder)
                    language = None
                    if self.language_options:
                        try:
                            choices = self.language_options(selected)
                        except DATA_ERRORS as error:
                            raise GameFolderError(self.wrong_folder) from error
                        if len(choices) > 1:
                            language = choose_language(window, choices)
                            if language is None:
                                messagebox.showinfo(self.title, "No language was chosen, so no page was written.", parent=window)
                                return 0
                        elif choices:
                            language = next(iter(choices))
                    path = self.write_page(selected, open_page=False, language=language)
                    opened = open_report(path)
                except GameFolderError as error:
                    messagebox.showerror(self.title, str(error), parent=window)
                except (OSError, ValueError, ImportError) as error:
                    messagebox.showerror(self.title, str(error), parent=window)
                    return 1
                else:
                    message = "Your My Game page is saved here."
                    if not opened:
                        message = "Open your saved My Game page in your browser."
                    messagebox.showinfo(self.title, f"{message}\n\n{path}", parent=window)
                    return 0
            messagebox.showinfo(self.title, CANCELLED, parent=window)
            return 0
        finally:
            window.destroy()

    def main(self, argv=None):
        parser = argparse.ArgumentParser(prog="lol.py mygame", description="Make an offline page from your game.")
        parser.add_argument("--data", type=Path, help="use a game folder without opening the folder picker")
        parser.add_argument("--out", type=Path, help="save to a new HTML file at this path")
        parser.add_argument("--no-browser", action="store_true", help="save without opening the browser")
        if self.languages:
            parser.add_argument("--language", type=str.upper, choices=self.languages,
                                help="choose a language table present in your game")
        args = parser.parse_args(argv)
        language = getattr(args, "language", None)
        if args.data is None and (args.out or args.no_browser or language):
            parser.error("Use --data with --out, --no-browser or --language." if self.languages else
                         "Use --data with --out or --no-browser.")
        try:
            if args.data is None:
                return self.desktop()
            path = self.write_page(args.data, args.out, open_page=not args.no_browser, language=language)
            if sys.stdout is not None:
                print(path)
            return 0
        except (OSError, ValueError, ImportError) as error:
            if sys.stderr is not None:
                print(f"{parser.prog}: {error}", file=sys.stderr)
            return 1
