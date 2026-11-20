"""Offline saved-game field page and copy-command builder."""
from html import escape
import json

from modkit_core import output_path


STYLE = """
:root{color-scheme:light dark;--bg:#111b24;--panel:#192936;--ink:#f4f4ed;--border:#526779;--muted:#b9c7d3;--accent:#89dfc3}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 system-ui,sans-serif}
main{max-width:1040px;margin:auto;padding:1.5rem clamp(1rem,4vw,3rem) 2.5rem}
h1{font-size:clamp(1.55rem,5vw,2.25rem);margin:0}
h2{font-size:1.25rem;margin:0 0 .45rem}
h3{font-size:1rem;margin:0}
p{margin:.4rem 0 .85rem}
.muted,dt{color:var(--muted)}
header,section{margin-bottom:1.5rem}
dl{display:grid;grid-template-columns:max-content 1fr;gap:.25rem 1rem;margin:.5rem 0}
dd{margin:0;overflow-wrap:anywhere} .settings,.edits{display:grid;gap:.8rem}
.settings{grid-template-columns:1fr 2fr}
article{background:var(--panel);border:1px solid var(--border);border-radius:8px;padding:.85rem 1rem}
label{display:block;font-weight:600;margin-top:.5rem}
button,input,select,textarea{font:inherit;color:inherit;background:#101a24;border:1px solid var(--border);border-radius:4px;padding:.4rem .55rem}
input,textarea{display:block;width:100%} button{cursor:pointer;margin-top:.35rem}
textarea{font:.85rem/1.45 ui-monospace,monospace;resize:vertical;margin-top:.35rem}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.current{font-weight:400;color:var(--accent);overflow-wrap:anywhere}
@media(max-width:540px){.settings{grid-template-columns:1fr}}
"""

SCRIPT = r"""
const data = JSON.parse(document.getElementById('save-model').textContent);
const list = document.getElementById('edits');
const output = document.getElementById('output');
const shell = document.getElementById('shell');
const make = (tag, text) => {
    const element = document.createElement(tag);
    if (text !== undefined) element.textContent = text;
    return element;
};
const quoteSh = value => "'" + value.replaceAll("'", "'\"'\"'") + "'";
const quotePs = value => "'" + value.replaceAll("'", "''") + "'";
const rows = [];
for (const [id, label, current, value, max, status] of data.fields) {
    const card = make('article');
    const input = make('input');
    input.id = 'value-' + id;
    input.type = typeof value === 'number' ? 'number' : 'text';
    input.value = value ?? '';
    input.required = true;
    if (typeof value === 'number') { input.min = '0'; input.max = max; input.step = '1'; }
    else if (max !== null) input.maxLength = max;
    if (id === 'position-from') input.placeholder = 'Path to the donor save';
    const named = make('label', id === 'position-from' ? 'Donor save from the same level and version' : 'New value');
    named.htmlFor = input.id;
    const command = make('textarea');
    command.readOnly = true;
    command.rows = 2;
    command.setAttribute('aria-label', label + ' command');
    const copy = make('button', 'Copy command');
    copy.type = 'button';
    const note = make('span');
    note.className = 'muted';
    note.setAttribute('role', 'status');
    const displayed = make('span', current);
    displayed.className = 'current';
    const heading = make('h3', label + ' · ');
    heading.append(displayed);
    const evidence = make('p', status);
    evidence.className = 'muted';
    card.append(heading, named, input, command, copy, note, evidence);
    list.append(card);
    function update() {
        const quote = shell.value === 'ps' ? quotePs : quoteSh;
        const python = shell.value === 'ps' ? 'python' : 'python3';
        const valid = output.value.trim() && input.value && input.checkValidity() &&
            (id !== 'name' || /^[ -~]+$/.test(input.value));
        command.value = valid ? python + ' tools/lol.py save set --out ' + quote(output.value) +
            ' -- ' + [data.source, id, input.value].map(quote).join(' ') : '';
        copy.disabled = !valid;
        note.textContent = '';
    }
    input.addEventListener('input', update);
    copy.onclick = async () => {
        try { await navigator.clipboard.writeText(command.value); note.textContent = ' Copied'; }
        catch (_) { command.select(); note.textContent = ' Press Ctrl+C or Command+C to copy.'; }
    };
    rows.push(update);
}
for (const control of [shell, output]) control.addEventListener('input', () => rows.forEach(update => update()));
rows.forEach(update => update());
"""


def render(source, game, fields, facts):
    model = json.dumps({"source": str(source), "fields": fields}, ensure_ascii=True).replace("<", "\\u003c")
    details = "".join(f"<dt>{escape(label)}</dt><dd>{escape(str(value))}</dd>" for label, value in facts)
    return f"""<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(game)} save fields</title><style>{STYLE}</style>
<main>
<header><h1>{escape(game)} save fields</h1><p class="muted">{escape(source.name)}</p></header>
<section aria-labelledby="stored"><h2 id="stored">Stored values</h2><dl>{details}</dl></section>
<section aria-labelledby="commands"><h2 id="commands">Make a copy with one edit</h2>
<p>Enter a value and paste its command into a terminal in the tools repository.
Use a new output path for each command. For a second edit on the same save,
make a page for the first edited copy and use another output name.</p>
<div class="settings">
<div><label for="shell">Terminal</label><select id="shell">
<option value="sh">Linux or macOS</option><option value="ps">PowerShell</option></select></div>
<div><label for="output">New save path</label><input id="output" value="../edited-save{escape(source.suffix, quote=True)}"></div>
</div>
</section>
<section id="edits" class="edits" aria-label="Editable fields"></section>
<p class="muted">This private page includes your save name and local path. It runs offline.</p>
</main><script id="save-model" type="application/json">{model}</script><script>{SCRIPT}</script>
</html>
"""


def write(source, output, game, fields, facts):
    source = source.resolve()
    protected = (source.parent.parent,) if source.parent.name.upper() in ("SAVEGAME", "SAVE") else ()
    path = output_path(output, source.parent, source, *protected)
    if path.suffix.lower() != ".html":
        raise ValueError("Give --out a new .html file.")
    if not path.parent.is_dir():
        raise ValueError(f"The folder {path.parent} does not exist. Choose an existing folder.")
    with path.open("x", encoding="utf-8") as result:
        result.write(render(source, game, fields, facts))
    return path
