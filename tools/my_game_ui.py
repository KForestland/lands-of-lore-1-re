"""Shared window and offline report for the three Lands of Lore guides."""
import argparse
from base64 import b64encode
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from gzip import compress
from html import escape
from io import BytesIO
from itertools import count
from pathlib import Path
from struct import error as StructError
import sys
import webbrowser

from cli_errors import output_refusal


DESKTOP_TITLE = "Lands of Lore: My Game"
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

async function showPlan(image) {
    try {
        const bytes = Uint8Array.from(atob(image.dataset.svgGzip), character => character.charCodeAt(0));
        const stream = new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'));
        const plan = await new Response(stream, {headers: {'Content-Type': 'image/svg+xml'}}).blob();
        image.src = URL.createObjectURL(plan);
    } catch {
        document.getElementById('plan-browser-message').hidden = false;
    }
}
for (const image of document.querySelectorAll('img[data-svg-gzip]')) showPlan(image);
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
    packed_plans = False
    for key, title, image, format in maps:
        anchor, name = escape(f"level-{key}"), escape(title)
        jumps.append(f'<a href="#{anchor}">{name}</a>')
        if format == "svg+xml":
            packed_plans = True
            encoded = b64encode(compress(image, mtime=0)).decode("ascii")
            source = f'data-svg-gzip="{encoded}"'
        else:
            encoded = b64encode(image).decode("ascii")
            source = f'src="data:image/{format};base64,{encoded}"'
        cards.append(
            f'<article id="{anchor}"><h3>{name}</h3>'
            f'<img {source} loading="lazy" alt="Overhead plan of {name}"></article>'
        )
    message = ""
    if packed_plans:
        message = ('<p id="plan-browser-message" role="status" hidden>'
                   'Open this page in a current browser to see the level plans.</p>'
                   '<noscript><p>Enable JavaScript to see the level plans.</p></noscript>')
    return (
        '<section id="maps"><h2>Level plans</h2><details><summary>Jump to a level</summary>'
        f'<nav class="jump" aria-label="Jump to level">{" ".join(jumps)}</nav></details>'
        f'{legend}{message}<div class="levels">{"".join(cards)}</div></section>'
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
    maps = tuple(maps)
    map_sections = (("maps", "Level plans", maps_section(maps, legend)),) if maps else ()
    sections = (*map_sections, *tables, *extras)
    nav = "".join(f'<a href="#{key}">{escape(label)}</a>' for key, label, _ in sections)
    main = "".join(row[2] for row in map_sections)
    if tables:
        main += '<div class="catalogues">' + "".join(row[2] for row in tables) + '</div>'
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


def write_new_file(out, game_root, page, *protected):
    if any(output_refusal(out, root) for root in (game_root, *protected)):
        raise ValueError("Save the My Game report outside the game and saved-game folders." if protected else
                         "Save the My Game page outside the game folder.")
    stream = out.open("x", encoding="utf-8")
    try:
        with stream:
            stream.write(page)
    except OSError:
        out.unlink(missing_ok=True)
        raise


def save_in_documents(game_root, page, filename, *protected, extension=".html"):
    documents = documents_folder().resolve()
    if documents in protected:
        raise ValueError("Your saved game is in Documents. Move a copy to another folder and open it from there.")
    if any(output_refusal(documents, root) for root in (game_root, *protected)):
        raise ValueError("Your Documents folder is inside a game or saved-game folder." if protected else
                         "Save the My Game page outside the game folder.")
    documents.mkdir(parents=True, exist_ok=True)
    for number in count(1):
        name = (filename if number == 1 else f"{filename} {number}") + extension
        out = documents / name
        try:
            write_new_file(out, game_root, page, *protected)
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


def read_with_progress(parent, read):
    from tkinter import Toplevel, ttk

    progress = Toplevel(parent)
    progress.title(DESKTOP_TITLE)
    progress.transient(parent)
    progress.resizable(False, False)
    progress.protocol("WM_DELETE_WINDOW", lambda: None)
    content = ttk.Frame(progress, padding=20)
    content.pack(fill="both", expand=True)
    ttk.Label(content, text="Reading your game...").pack(anchor="w")
    bar = ttk.Progressbar(content, mode="indeterminate", length=290)
    bar.pack(fill="x", pady=(8, 0))

    previous_grab = parent.grab_current()
    progress.wait_visibility()
    progress.grab_set()
    bar.start(50)

    with ThreadPoolExecutor(max_workers=1) as executor:
        job = executor.submit(read)

        def check_finished():
            if job.done():
                progress.destroy()
            else:
                progress.after(40, check_finished)

        progress.after(40, check_finished)
        parent.wait_window(progress)
        if previous_grab is not None:
            previous_grab.grab_set()
        return job.result()


def close_startup_splash():
    try:
        import pyi_splash
    except ImportError:
        return
    pyi_splash.close()


@dataclass(frozen=True)
class MyGame:
    filename: str
    title: str
    game: str
    data_folder: str
    read_page: Callable[..., str]
    languages: dict[str, str] | None = None
    read_saved: Callable[..., str | tuple[str, str]] | None = None
    faults: tuple[str, ...] = ()

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
        game_root = self.game_root(folder)
        if out is None:
            out = save_in_documents(game_root, page, self.filename)
        else:
            write_new_file(out, game_root, page)
        if open_page and not open_report(out):
            raise ValueError(f"Open the My Game page in your browser from {out}.")
        return out

    def game_root(self, folder):
        folder = folder.resolve()
        if self.languages and folder.name.upper() in self.languages:
            folder = folder.parent
        return folder.parent if folder.name.upper() == self.data_folder else folder

    def open_installation(self, window, filedialog, messagebox):
        while folder := filedialog.askdirectory(parent=window, title=f"Choose your {self.game} folder"):
            try:
                selected = Path(folder)
                language = None
                if self.languages:
                    choices = {"AUTO": "Use the game's language", **self.languages}
                    choice = choose_language(window, choices)
                    if choice is None:
                        messagebox.showinfo(self.title, "No language was chosen, so no page was written.", parent=window)
                        return 0
                    if choice != "AUTO":
                        language = choice
                path = read_with_progress(
                    window, lambda: self.write_page(selected, open_page=False, language=language),
                )
                opened = open_report(path)
            except GameFolderError as error:
                messagebox.showerror(self.title, str(error), parent=window)
            except (OSError, ValueError, ImportError) as error:
                messagebox.showerror(self.title, str(error), parent=window)
                return 1
            else:
                message = "Your My Game page is saved here." if opened else "Open your saved My Game page in your browser."
                messagebox.showinfo(self.title, f"{message}\n\n{path}", parent=window)
                return 0
        messagebox.showinfo(self.title, CANCELLED, parent=window)
        return 0

    def open_saved_game(self, window, filedialog, messagebox):
        picked = filedialog.askopenfilename(parent=window, title=f"Choose your {self.game} saved game")
        if not picked:
            messagebox.showinfo(self.title, "No saved game was chosen, so no report was written.", parent=window)
            return
        source = Path(picked)
        purpose = "to read the game's reference values" if self.faults else "for names and maps"
        folder = filedialog.askdirectory(parent=window, title=f"Choose your {self.game} folder {purpose}")
        if not folder:
            messagebox.showinfo(self.title, "No game folder was chosen, so no report was written.", parent=window)
            return
        folder = Path(folder)
        if self.faults:
            self.fault_dialog(window, source, folder, messagebox)
            return

        def write_saved_page():
            protected = (source.parent.resolve(), source.resolve().parent)
            page = self.read_saved(source, folder)
            return save_in_documents(self.game_root(folder), page, f"{self.filename} Save", *protected)

        try:
            path = read_with_progress(window, write_saved_page)
            open_report(path)
        except (OSError, ValueError, ImportError) as error:
            messagebox.showerror(self.title, str(error), parent=window)
        else:
            messagebox.showinfo(self.title, f"Your saved game page is here.\n\n{path}", parent=window)

    def fault_dialog(self, parent, source, folder, messagebox):
        from tkinter import Text, Toplevel, ttk

        window = Toplevel(parent)
        window.title("Report a fault")
        window.transient(parent)
        window.grab_set()
        frame = ttk.Frame(window, padding=16)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Choose the fault you saw.").pack(anchor="w")
        choice = ttk.Combobox(frame, values=self.faults, state="readonly", width=40)
        choice.pack(fill="x", pady=(4, 8))
        ttk.Label(frame, text="The file contains only the listed game values and no personal data.").pack(anchor="w")
        preview = Text(frame, width=60, height=14, wrap="word", state="disabled")
        preview.pack(fill="both", expand=True, pady=8)
        notes = ttk.Label(frame, wraplength=465)
        notes.pack(anchor="w", pady=(0, 8))
        report_text = None

        def show_preview(_event):
            nonlocal report_text
            try:
                index = choice.current()
                report_text, omitted = read_with_progress(window, lambda: self.read_saved(source, folder, index))
                message = report_text
            except (OSError, ValueError, ImportError) as error:
                report_text = None
                omitted = ""
                message = str(error)
            preview.configure(state="normal")
            preview.delete("1.0", "end")
            preview.insert("1.0", message)
            preview.configure(state="disabled")
            notes.configure(text=omitted)
            save_button.configure(state="normal" if report_text else "disabled")

        def save_report():
            try:
                protected = (source.parent.resolve(), source.resolve().parent)
                path = save_in_documents(self.game_root(folder), report_text, f"{self.filename} Fault Report",
                                         *protected, extension=".txt")
            except (OSError, ValueError) as error:
                messagebox.showerror(self.title, str(error), parent=window)
                return
            messagebox.showinfo(self.title, f"Your fault report is here.\n\n{path}", parent=window)
            window.destroy()

        save_button = ttk.Button(frame, text="Save to Documents", command=save_report, state="disabled")
        save_button.pack(side="left")
        ttk.Button(frame, text="Cancel", command=window.destroy).pack(side="right")
        choice.bind("<<ComboboxSelected>>", show_preview)

    def desktop(self):
        from tkinter import TclError, Tk, filedialog, messagebox, ttk

        try:
            window = Tk()
        except TclError as error:
            raise ValueError("Open My Game from your desktop to choose a game folder.") from error
        try:
            window.title(DESKTOP_TITLE)
            window.minsize(440, 190)
            if sys.platform == "win32":
                icon = Path(__file__).with_name("mygame.ico")
                if icon.is_file():
                    window.iconbitmap(default=str(icon))
            window.protocol("WM_DELETE_WINDOW", window.quit)
            frame = ttk.Frame(window, padding=20)
            frame.pack(fill="both", expand=True)
            ttk.Label(frame, text="Make a guide from your game folder or see what’s in a saved game.",
                      wraplength=400).pack(anchor="w", pady=(0, 14))
            ttk.Button(frame, text="Open a game folder",
                       command=lambda: self.open_installation(window, filedialog, messagebox)).pack(fill="x", pady=(0, 8))
            ttk.Button(frame, text="Open a saved game",
                       command=lambda: self.open_saved_game(window, filedialog, messagebox)).pack(fill="x")
            window.wait_visibility()
            close_startup_splash()
            window.mainloop()
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
