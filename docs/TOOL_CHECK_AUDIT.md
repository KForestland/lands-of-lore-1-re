# Reader tool check audit

On 20 November 2026, this repository's tests were run on scratch copies with one deliberate mistake at a time. The tests used generated data. The broken evidence link was checked with `python tools/doc_links.py --check`.

The original checks caught 10 of 19 planted mistakes. The revised checks caught all 19.

| Planted mistake | Original result | Check after the audit |
|---|---|---|
| Skip old-span hash | Caught | [`test_patch.py`](../tests/test_patch.py) |
| Restore difflib autojunk | Missed | [`test_patch.py`](../tests/test_patch.py) |
| Omit undo | Caught | [`test_kit_cli.py`](../tests/test_kit_cli.py) |
| Skip program fingerprint | Caught | [`test_patch.py`](../tests/test_patch.py) |
| Ignore changed output bytes | Caught | [`test_modkit.py`](../tests/test_modkit.py) |
| Ignore changed entry identity | Missed | [`test_modkit.py`](../tests/test_modkit.py) |
| Ignore changed original CSV text or ID | Missed | [`test_translation_tools.py`](../tests/test_translation_tools.py) |
| Discard changed text | Caught | [`test_translation_tools.py`](../tests/test_translation_tools.py) |
| Allow unexpected output files | Missed | [`test_translation_tools.py`](../tests/test_translation_tools.py) |
| Drop map records | Caught | [`test_kit_cli.py`](../tests/test_kit_cli.py) |
| Replace feature labels in the page | Missed | [`test_kit_cli.py`](../tests/test_kit_cli.py) |
| Ignore source checksum | Missed | [`test_kit_cli.py`](../tests/test_kit_cli.py) |
| Skip moved coordinates | Missed | [`test_kit_cli.py`](../tests/test_kit_cli.py) |
| Lose HTML escaping of stored values | Caught | [`test_translation_tools.py`](../tests/test_translation_tools.py) |
| Lose HTML escaping of save names | Missed | [`test_translation_tools.py`](../tests/test_translation_tools.py) |
| Treat any equal-sized file as a match | Caught | [`test_edition.py`](../tests/test_edition.py) |
| Skip missing witnesses | Caught | [`test_edition.py`](../tests/test_edition.py) |
| Break an unused-page evidence link | Caught | [`doc_links.py`](../tools/doc_links.py) |
| Wrong stored opcode count | Missed | [`test_unused.py`](../tests/test_unused.py) |

The factual check covers the opcode summary. The other prose on the unused-content page still depends on the original evidence linked there and on review.
