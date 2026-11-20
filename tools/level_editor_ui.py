"""Offline controls for editing a LoL1 plan made by level_viewer.py."""
import json


CONTROLS = """
<button id="edit-toggle" type="button" aria-controls="editor" aria-expanded="false">Edit level</button>
<section id="editor" hidden>
<h2>Level edits</h2>
<p class="muted">Click a square or enter its number. The original files are read only.</p>
<label for="edit-square">Square (0–1023)</label>
<input id="edit-square" type="number" min="0" max="1023" step="1">
<fieldset id="edit-walls" disabled><legend>Walls of this square</legend>
<label>North <select aria-label="North wall"></select></label>
<label>East <select aria-label="East wall"></select></label>
<label>South <select aria-label="South wall"></select></label>
<label>West <select aria-label="West wall"></select></label>
</fieldset>
<label for="edit-item">Placed item</label><select id="edit-item"></select>
<p class="muted">Items placed by other scripts remain on the plan as read-only markers.</p>
<p id="edit-position" class="muted" role="status" hidden></p>
<div class="edit-buttons"><button id="edit-move" disabled>Move to square</button>
<button id="edit-remove" disabled>Remove item</button></div>
<label for="edit-type">Item type to add</label><select id="edit-type"></select>
<div class="edit-buttons"><button id="edit-add" disabled>Add to square</button></div>
<p id="edit-count" role="status"></p>
<div class="edit-buttons"><button id="edit-export">Download changes</button>
<button id="edit-reset" disabled>Clear edits</button></div>
<p class="muted">Apply the downloaded file with <code>tools/level_edit.py</code>. See the Level Editor guide for the command.</p>
</section>
"""

STYLE = """
#edit-toggle{margin-bottom:.8rem}#editor{padding:.6rem 0;border-bottom:1px solid var(--border);margin-bottom:.8rem}
#editor fieldset{border:1px solid var(--border);border-radius:.3rem;padding:.45rem .65rem;margin:0 0 .65rem}
#editor fieldset select{margin-bottom:.4rem}#editor label{font-size:.9rem}
.edit-buttons{display:flex;gap:.35rem;flex-wrap:wrap;margin-bottom:.65rem}
.edit-buttons button{font-size:.87rem}#edit-count{font-weight:600}
.editing .editable-item,.editing .editable-item + .num{display:none}
.editing .read-only-item:not(.chosen){opacity:.65}
#edit-overlay{pointer-events:none}
"""

SCRIPT = """
{
const model = JSON.parse(document.querySelector('#edit-model').textContent);
const panel = document.querySelector('#editor');
const squareField = document.querySelector('#edit-square');
const placed = document.querySelector('#edit-item');
const types = document.querySelector('#edit-type');
const wallPanel = document.querySelector('#edit-walls');
const wallFields = [...wallPanel.querySelectorAll('select')];
const button = id => document.querySelector('#edit-' + id);
const wallTypes = new Map(model.types.map(type => [type[0], type]));
const names = new Map(model.names);
const original = new Map(model.items.map(([site, type, block, x, y, height]) => [site, {site, type, block, x, y, height}]));
const pending = new Map();
const added = new Map();
const walls = new Map();
const svgNS = 'http://www.w3.org/2000/svg';
let square = null, nextItem = -1;
const overlay = document.createElementNS(svgNS, 'g');
overlay.id = 'edit-overlay';
map.append(overlay);

function element(tag, attributes) {
    const element = document.createElementNS(svgNS, tag);
    for (const [key, value] of Object.entries(attributes)) element.setAttribute(key, value);
    return element;
}
function point(block) {
    const [left, top, cell] = model.grid;
    return [left + (block % 32) * cell, top + Math.floor(block / 32) * cell, cell];
}
function savedItems() {
    const kept = [...original.values()].map(item =>
        pending.has(item.site) ? {...item, block: pending.get(item.site)} : item);
    return [...kept.filter(item => item.block !== null), ...added.values()];
}
function renderEdits() {
    overlay.replaceChildren();
    if (panel.hidden) return;
    for (const [block, sides] of walls) {
        const [x, y, size] = point(block);
        const visible = sides.map(id => wallTypes.get(id)?.[2]);
        const fill = visible.every(Boolean) ? '#282830' : visible.some(Boolean) ? '#e69632' : '#ebe8dc';
        overlay.append(element('rect', {x: x+.8, y: y+.8, width: size-1.6, height: size-1.6, fill}));
        const positions = [[.5,.17],[.83,.5],[.5,.83],[.17,.5]];
        sides.forEach((id, i) => {
            if (!wallTypes.get(id)?.[3]) return;
            const [dx, dy] = positions[i];
            overlay.append(element('rect', {x:x+(dx-.11)*size, y:y+(dy-.11)*size,
                                          width:size*.22, height:size*.22, fill:'#c81e1e'}));
        });
    }
    const chosen = placed.value === '' ? null : Number(placed.value);
    for (const item of savedItems()) {
        const [x, y, size] = point(item.block);
        const cx = x+.68*size, cy = y+.30*size;
        overlay.append(element('circle', {
            cx, cy, class: item.site === chosen ? 'marker chosen' : 'marker', fill: '#79e3c8'
        }));
        const label = element('text', {x:cx, y:cy, class:'num', dx:'.5em', dy:'-.5em'});
        label.textContent = 'I' + item.type;
        overlay.append(label);
    }
}
function syncButtons() {
    const chosen = placed.value !== '';
    const item = chosen ? original.get(Number(placed.value)) : null;
    const notice = button('position');
    notice.hidden = !item;
    if (item) {
        const position = 'A move keeps this item’s X/Y (' + item.x + '/' + item.y + ') and height (' + item.height + ').';
        notice.textContent = item.height === 0 ? position : position + ' Choose a matching niche or ledge, or add a new floor placement instead.';
    }
    button('move').disabled = square === null || !chosen;
    button('remove').disabled = !chosen;
    button('add').disabled = square === null || types.value === '';
    button('reset').disabled = !(walls.size || pending.size || added.size);
    const count = (n, one, many) => n + ' ' + (n === 1 ? one : many);
    button('count').textContent = count(walls.size, 'square edited', 'squares edited') + ' · ' +
        count(pending.size + added.size, 'item edit', 'item edits');
    renderEdits();
}
function updateItems(preferred = placed.value) {
    placed.replaceChildren(new Option('Choose an item', ''),
        ...savedItems().map(row => new Option(
            (names.get(row.type) || 'Item ' + row.type) + ' · square ' + row.block, row.site)));
    if ([...placed.options].some(option => option.value === preferred)) placed.value = preferred;
    syncButtons();
}
function updateSquare(block) {
    square = Number.isInteger(block) && block >= 0 && block < 1024 ? block : null;
    squareField.value = square === null ? '' : square;
    wallPanel.disabled = square === null;
    const values = walls.get(square) || model.squares[square];
    wallFields.forEach((field, k) => {
        field.replaceChildren(...model.types.map(type => new Option(type[1], type[0])));
        if (!values) return;
        const id = values[k];
        if (!wallTypes.has(id)) field.add(new Option(id + ' · Stored wall without a local definition', id));
        field.value = String(id);
    });
    syncButtons();
}

button('toggle').onclick = () => {
    panel.hidden = !panel.hidden;
    button('toggle').textContent = panel.hidden ? 'Edit level' : 'Close editor';
    button('toggle').setAttribute('aria-expanded', String(!panel.hidden));
    map.classList.toggle('editing', !panel.hidden);
    renderEdits();
};
document.addEventListener('plan-selected', event => {
    const id = event.detail;
    if (id.startsWith('block-')) updateSquare(Number(id.slice(6)));
});
squareField.onchange = () => updateSquare(squareField.valueAsNumber);
wallPanel.onchange = () => {
    const values = wallFields.map(field => Number(field.value));
    if (values.every((id, k) => id === model.squares[square][k])) walls.delete(square);
    else walls.set(square, values);
    syncButtons();
};
types.replaceChildren(new Option('Choose an item type', ''),
    ...model.names.map(([id, name]) => new Option(name + ' · type ' + id, id)));
types.onchange = placed.onchange = syncButtons;
button('move').onclick = () => {
    const id = Number(placed.value);
    if (id < 0) added.get(id).block = square;
    else if (square === original.get(id).block) pending.delete(id);
    else pending.set(id, square);
    updateItems();
};
button('remove').onclick = () => {
    const id = Number(placed.value);
    if (id < 0) added.delete(id);
    else pending.set(id, null);
    updateItems('');
};
button('add').onclick = () => {
    const site = nextItem--;
    added.set(site, {site, type: Number(types.value), block: square});
    updateItems(String(site));
};
button('reset').onclick = () => {
    walls.clear(); pending.clear(); added.clear();
    updateSquare(square);
    updateItems('');
};
function changeFile() {
    return {
        format: model.format, level: model.level, source: model.source,
        walls: [...walls].sort((a,b) => a[0]-b[0]),
        items: [...pending].sort((a,b) => a[0]-b[0]),
        add: [...added.values()].map(({type, block}) => [type, block])
    };
}
button('export').onclick = () => {
    const raw = JSON.stringify(changeFile(), null, 2) + '\\n';
    const url = URL.createObjectURL(new Blob([raw], {type: 'application/json'}));
    const link = document.createElement('a');
    link.href = url;
    link.download = 'level' + String(model.level).padStart(2, '0') + '-changes.json';
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
};
updateItems();
}
"""


def sections(model, plan):
    model = {**model, "grid": [*plan.point((0, 0)), plan.scale]}
    raw = json.dumps(model, ensure_ascii=True, separators=(",", ":")).replace("<", "\\u003c")
    return (CONTROLS, f'<style>{STYLE}</style><script id="edit-model" type="application/json">{raw}</script>'
                      f'<script>{SCRIPT}</script>')
