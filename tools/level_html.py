"""Write self-contained, interactive plans from level geometry and reader notes."""
from collections import Counter
from html import escape
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from cli_errors import ReaderArgumentParser
from modkit_core import output_folder

WIDTH, HEIGHT = 900, 630

STYLE = """
:root{color-scheme:dark;--ground:#101b24;--panel:#192b38;--ink:#f0eee7;--muted:#b4c4ce;
      --accent:#76dec6;--exit:#b8eb79;--border:#3d5665;font:16px system-ui,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--ground);color:var(--ink)}
header,main,footer{max-width:1440px;margin:auto;padding:1rem 1.5rem}
h1{margin:.1rem 0 .45rem;font-size:clamp(1.6rem,3vw,2.6rem)}h2{font-size:1.08rem;margin:0 0 .65rem}
p{margin:.5rem 0;line-height:1.45}.muted,footer{color:var(--muted)}
main{display:grid;grid-template-columns:minmax(0,1fr) minmax(250px,320px);gap:1rem;padding-block:0}
figure,aside{margin:0;border:1px solid var(--border);border-radius:.65rem;background:var(--panel)}
figure{overflow:hidden}aside{padding:1rem;min-width:0}svg{width:100%;height:auto;display:block;background:#132330;touch-action:none}
.toolbar,.legend{display:flex;gap:.55rem 1rem;align-items:center;flex-wrap:wrap;padding:.65rem .8rem}
.toolbar{border-bottom:1px solid var(--border)}.legend{border-top:1px solid var(--border);font-size:.84rem}
button,input,select{font:inherit;color:inherit;background:#101e28;border:1px solid #688391;border-radius:.3rem}
button{padding:.32rem .65rem;cursor:pointer}button:enabled:hover{border-color:var(--accent)}
button:disabled{opacity:.45;cursor:default}
label input[type=checkbox]{vertical-align:middle}aside input,aside select{padding:.35rem;width:100%;margin:.25rem 0 .75rem}
input[type=checkbox]{accent-color:var(--accent)}:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
dt{color:var(--muted);font-size:.8rem;line-height:1.35;margin-top:.55rem}dd{margin:.06rem 0;overflow-wrap:anywhere}
.region{fill:#294554;stroke:#567481;stroke-width:.45;vector-effect:non-scaling-stroke}
.wall,.door,.route{pointer-events:none;vector-effect:non-scaling-stroke;fill:none}
.wall{stroke:#9ab0bb;stroke-width:.85}.door{stroke:var(--exit);stroke-width:1.15}
.route{stroke:#83a6ff;stroke-width:1.2;stroke-dasharray:3 3}
.exit-region{fill:#425d31;stroke:var(--exit)}
.cell{fill:transparent;vector-effect:non-scaling-stroke}
.cell.exit-region{fill:var(--exit);fill-opacity:.53;stroke-width:1.15}
.hit{cursor:pointer}.hit:hover{stroke:#a9f4e2;stroke-width:1.55}
.marker{r:var(--marker-size,3.1px);stroke:#10232a;stroke-width:1;vector-effect:non-scaling-stroke}
.chosen,.marker.chosen,.cell.chosen{stroke:#fff;stroke-width:2.2}
.num{fill:#fff;stroke:#172531;stroke-width:calc(var(--label-size,8px) * .3);paint-order:stroke;font:var(--label-size,8px) system-ui,sans-serif;pointer-events:none;display:none}
.show-numbers .num,.chosen + .num{display:block}.dim{opacity:.25}
.swatch{display:inline-block;width:.7rem;height:.7rem;margin-right:.3rem;border-radius:.12rem;vertical-align:baseline}
@media(max-width:760px){main{grid-template-columns:1fr}header,main,footer{padding-inline:.75rem}}
"""

SCRIPT = """
const map = document.querySelector('#map');
const details = document.querySelector('#details');
const results = document.querySelector('#results');
const filter = document.querySelector('#filter');
const query = document.querySelector('#query');
const numberFormat = new Intl.NumberFormat('en-US');
const records = JSON.parse(document.querySelector('#records').textContent);
const byId = new Map(records.map(record => [record.id, record]));
const linked = new Map();
for (const record of records) {
    if (!record.target || record.kind !== 'Exits') continue;
    if (!linked.has(record.target)) linked.set(record.target, []);
    linked.get(record.target).push(record);
}
const base = [0, 0, 900, 630];
let box = [...base], selected = null, drag = null, moved = false;
function view() {
    map.setAttribute('viewBox', box.join(' '));
    map.style.setProperty('--marker-size', (3.1 * box[2]/900) + 'px');
    map.style.setProperty('--label-size', (8 * box[2]/900) + 'px');
}
function zoom(factor) {
    const width = Math.max(9, Math.min(1800, box[2] * factor));
    const height = width * base[3] / base[2];
    box = [box[0]+(box[2]-width)/2, box[1]+(box[3]-height)/2, width, height]; view();
}
function focus(record) {
    const shape = document.getElementById(record.target || record.id);
    if (!shape) return;
    const geom = shape.getBBox();
    const width = Math.max(75, Math.min(900, geom.width*1.6 + 25));
    const height = Math.max(width*630/900, geom.height*1.6 + 15);
    const w = Math.min(1800, height*900/630);
    box = [geom.x+geom.width/2-w/2, geom.y+geom.height/2-height/2, w, height]; view();
}
function select(id) {
    const record = byId.get(id);
    if (!record) return;
    if (selected) selected.classList.remove('chosen');
    selected = document.getElementById(record.target || id);
    if (selected) selected.classList.add('chosen');
    document.querySelector('#detail-title').textContent = record.label;
    document.querySelector('#center').disabled = !selected;
    document.querySelector('#center').onclick = () => focus(record);
    details.replaceChildren();
    const fields = Object.entries(record.details);
    for (const exit of linked.get(id) || []) {
        fields.push([exit.label, exit.details.Gate]);
    }
    for (const [label, value] of fields) {
        const term = document.createElement('dt'), description = document.createElement('dd');
        term.textContent = label; description.textContent = value;
        details.append(term, description);
    }
    if ([...results.options].some(option => option.value === id)) results.value = id;
}
function update() {
    const wanted = query.value.trim().toLowerCase();
    const kind = filter.value;
    const matches = records.filter(r => (!kind || kind === r.kind) &&
        (!wanted || r.label.toLowerCase().includes(wanted) || r.id.toLowerCase() === wanted ||
            Object.values(r.details).some(value => String(value).toLowerCase().includes(wanted))));
    results.replaceChildren(...matches.slice(0,500).map(r => new Option(r.label, r.id)));
    if (results.options.length) results.selectedIndex = -1;
    document.querySelector('#found').textContent = matches.length > 500
        ? numberFormat.format(matches.length) + ' matches. Refine your search to see more than the first 500.'
        : numberFormat.format(matches.length) + (matches.length === 1 ? ' match' : ' matches');
}
filter.addEventListener('change', update);
query.addEventListener('input', update);
results.addEventListener('change', () => select(results.value));
document.querySelector('#in').onclick = () => zoom(.7);
document.querySelector('#out').onclick = () => zoom(1/.7);
document.querySelector('#reset').onclick = () => { box = [...base]; view(); };
document.querySelector('#numbers').onchange = event => map.classList.toggle('show-numbers', event.target.checked);
map.addEventListener('click', e => { if (!moved) select(e.target.closest('.hit')?.id); });
map.addEventListener('pointerdown', e => { moved = false; drag = [e.clientX, e.clientY, ...box]; });
map.addEventListener('pointermove', e => {
    if (!drag) return;
    const dx = e.clientX - drag[0], dy = e.clientY - drag[1];
    if (!moved && Math.hypot(dx,dy) < 4) return;
    moved = true;
    const scale = box[2] / map.clientWidth;
    box[0] = drag[2] - dx * scale; box[1] = drag[3] - dy * scale; view();
});
window.addEventListener('pointerup', () => { drag = null; });
window.addEventListener('pointercancel', () => { drag = null; });
update();
"""


def counted(count, singular, plural=None):
    return f"{count:,} {singular if count == 1 else (plural or singular + 's')}"


def feature_count(kind, count):
    if kind == "Automap legend":
        return counted(count, "automap symbol")
    if kind == "Script entries":
        return counted(count, "script entry", "script entries")
    plural = kind.lower()
    return counted(count, plural[:-1], plural)


class Plan:
    """Store readable details alongside the shapes they identify."""
    def __init__(self, title, points, source, *, north_up=True, fixed=False):
        self.title, self.source = title, source
        self.shapes, self.records, self.legend = [], [], {}
        self.counts = Counter()
        self.fixed = fixed
        x, y = zip(*points)
        self.left, self.top, self.bottom = min(x), max(y), min(y)
        self.scale = min(856 / max(1, max(x) - self.left), 586 / max(1, self.top - self.bottom))
        self.xpad = (WIDTH - (max(x) - self.left) * self.scale) / 2
        self.ypad = (HEIGHT - (self.top - self.bottom) * self.scale) / 2
        self.north_up = north_up

    def point(self, xy):
        x, y = xy
        if self.fixed:
            return x, y
        dy = self.top - y if self.north_up else y - self.bottom
        return self.xpad + (x - self.left) * self.scale, self.ypad + dy * self.scale

    def points(self, coords):
        return " ".join(f"{x:.3f},{y:.3f}" for x, y in map(self.point, coords))

    def note(self, key, label, kind, details, target=None):
        if kind == "Exits" and target is None:
            details = {**details, "Location": "No location on the plan."}
        self.counts[kind] += 1
        self.records.append(dict(id=key, label=label, kind=kind, details=details, target=target))

    def polygon(self, points, key, label, kind, details, style="region"):
        self.note(key, label, kind, details)
        self.shapes.append(f'<polygon id="{key}" class="hit {style}" points="{self.points(points)}"/>')

    def line(self, points, style):
        self.shapes.append(f'<polyline class="{style}" points="{self.points(points)}"/>')

    def dot(self, xy, key, label, kind, details, color, number):
        self.note(key, label, kind, details)
        self.legend[kind] = color
        x, y = self.point(xy)
        self.shapes.append(f'<circle id="{key}" class="hit marker" cx="{x:.3f}" cy="{y:.3f}" r="3.1" fill="{color}"/>'
                           f'<text class="num" x="{x:.3f}" y="{y:.3f}" dx=".5em" dy="-.5em">{escape(str(number))}</text>')

    def render(self):
        title = escape(self.title)
        source = escape(self.source)
        shapes = "\n".join(self.shapes)
        legends = " ".join(f'<span><i class="swatch" style="background:{color}"></i>{escape(name)}</span>'
                           for name, color in self.legend.items())
        options = "".join(f'<option>{escape(kind)}</option>' for kind in self.counts)
        records = json.dumps(self.records, separators=(",", ":"), ensure_ascii=True).replace("<", "\\u003c")
        summary = " · ".join(feature_count(kind, count) for kind, count in self.counts.items())
        return f"""<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>{STYLE}</style>
<header><h1>{title}</h1><p class="muted">{escape(summary)}</p></header>
<main>
<figure>
<div class="toolbar"><button id="in">Zoom in</button><button id="out">Zoom out</button><button id="reset">Reset view</button>
<label><input id="numbers" type="checkbox"> Map numbers</label></div>
<svg id="map" viewBox="0 0 {WIDTH} {HEIGHT}" aria-label="Level plan">{shapes}</svg>
<figcaption class="legend">{legends}</figcaption>
</figure>
<aside>
<h2>Find on the plan</h2>
<label for="filter">Show</label><select id="filter"><option value="">Everything</option>{options}</select>
<label for="query">Name or number</label><input id="query" type="search" placeholder="Filter the list">
<p id="found" class="muted" aria-live="polite"></p>
<select id="results" aria-label="Matching features" size="5"></select>
<h2 id="detail-title">Details</h2><button id="center" disabled>Zoom to selection</button>
<dl id="details" aria-live="polite"><dd>Choose a row or click the plan.</dd></dl>
</aside>
</main>
<footer>{source}</footer>
<script id="records" type="application/json">{records}</script>
<script>{SCRIPT}</script>
</html>
"""


def find_data(path, child, marker):
    root = Path(path).resolve()
    if root.is_dir():
        for folder in (root, *(entry for entry in root.iterdir()
                               if entry.is_dir() and entry.name.upper() == child)):
            if any(entry.is_file() and entry.name.upper() == marker for entry in folder.iterdir()):
                return folder
    raise ValueError(f"Cannot find {marker} in {root}. Give --data the game folder or its {child} folder.")


def installation_root(data):
    if data.name.upper() == "DAT" or (
        data.name.upper() == "DATA" and (data.parent / "WESTWOOD.001").is_file()
    ):
        return data.parent
    return data


def write_plan(folder, stem, plan):
    path = folder / f"{stem}.html"
    path.write_text(plan.render(), encoding="utf-8")
    return path


def check_plan(stem, plan):
    with TemporaryDirectory(prefix="lol-level-check-") as temp:
        html = write_plan(Path(temp), stem, plan).read_text(encoding="utf-8")
    marker = '<script id="records" type="application/json">'
    if '<svg id="map"' not in html or marker not in html or not plan.records or not plan.shapes:
        raise ValueError(f"{stem} did not produce a map with searchable entries.")
    rows = json.loads(html.split(marker, 1)[1].split("</script>", 1)[0])
    if len(rows) != len(plan.records):
        raise ValueError(f"{stem} page lost searchable entries.")
    print(f"CHECK level viewer: {stem} page written and read back with {counted(len(rows), 'entry', 'entries')}.")
    return 0


def main(description, child, marker, default, levels, build, progression=None):
    parser = ReaderArgumentParser(description=description)
    parser.add_argument("--data", required=True, help=f"your game folder or its {child} folder")
    parser.add_argument("--level", default=default, help=f"level to show (default: {default}; use all for every level)")
    destination = parser.add_mutually_exclusive_group(required=True)
    destination.add_argument("--out", help="new output folder for the HTML pages")
    destination.add_argument("--check", action="store_true", help="write and verify one level page in a temporary folder")
    args = parser.parse_args()
    if args.check and args.level.upper() == "ALL":
        parser.error("--check takes one level.")
    data = find_data(args.data, child, marker)
    selected = levels(data, args.level.upper())
    if args.check:
        stem, = selected
        gates = progression(data, selected) if progression else {}
        return check_plan(stem, build(data, stem, gates.get(stem, ())))
    total = 0
    with output_folder(args.out, installation_root(data), args.data) as folder:
        if args.level.upper() == "ALL":
            print(f"Reading {counted(len(selected), 'level')}...", flush=True)
        gates = progression(data, selected) if progression else {}
        for stem in selected:
            plan = build(data, stem, gates.get(stem, ()))
            write_plan(folder, stem, plan)
            total += len(plan.records)
    print(f"Wrote {counted(len(selected), 'level page')} with {counted(total, 'entry', 'entries')} to {args.out}.")
    print(f"Open {selected[0]}.html in your browser.")
    return 0
