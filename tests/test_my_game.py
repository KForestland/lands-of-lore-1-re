"""Check the one-page guide with invented maps and names."""
from dataclasses import replace
from importlib.util import find_spec
import re
from pathlib import Path
from struct import pack_into
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import Mock, patch

from tests.test_level_tools import TOOLS
from tests.kit_fixture import call, make_fixture, script, TRANSLATE_FROM

from decode_dialogue import encode_string
from lol1_script_writer import write_strings
from my_game import TITLE, app, write_page
from my_game_ui import CANCELLED, GameFolderError


def make_my_game_fixture(folder):
    make_fixture(folder)
    data = folder / "DATA"
    program = bytearray(0x57240)
    program[:2] = b"MZ"
    pack_into("<HH", program, 0x2B5E0, 0x4000, 3)
    pack_into("<HH", program, 0x287D0, 0xFFFF, 0x4000)
    (data / "MAIN.EXE").write_bytes(program)


@unittest.skipUnless(find_spec("PIL"), "Pillow not installed")
class MyGame(unittest.TestCase):
    def test_page_for_game_root_using_local_names_and_embedded_plans(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            game = root / "example game"
            make_my_game_fixture(game)
            path = write_page(game, root / "My game.html", open_page=False)
            page = path.read_text(encoding="utf-8")
            self.assertIn("CD edition layout (exact version unverified)", page)
            self.assertEqual(re.findall(r'<article id="level-(\d+)">', page), [str(i) for i in range(1, 30)])
            self.assertEqual(page.count('src="data:image/png;base64,'), 29)
            self.assertIn('aria-label="Map legend"', page)
            self.assertIn(f'<article id="level-1"><h3>{TRANSLATE_FROM}</h3>', page)
            self.assertIn(f'<td>{TRANSLATE_FROM}</td><td>121</td>', page)
            self.assertIn(f'<td>{TRANSLATE_FROM}</td><td>0</td><td>3 / 0 / 0 / 0</td>', page)
            self.assertIn("Floor row 3, column 6", page)
            self.assertFalse(list(game.rglob("*.html")))
            with self.assertRaises(FileExistsError):
                write_page(game, path, open_page=False)
            self.assertEqual(path.read_text(encoding="utf-8"), page)
            with self.assertRaisesRegex(ValueError, "outside the game folder"):
                write_page(game / "DATA", game / "wrong.html", open_page=False)

    def test_empty_or_incomplete_folder_explains_what_to_pick(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)
            with self.assertRaises(GameFolderError) as problem:
                write_page(folder, open_page=False)
            self.assertEqual(str(problem.exception), app.wrong_folder)
            make_my_game_fixture(folder)
            (folder / "DATA" / "L29.PAK").unlink()
            with self.assertRaises(GameFolderError) as problem:
                write_page(folder, open_page=False)
            self.assertEqual(str(problem.exception), app.wrong_folder)

    def test_selected_language_is_used_in_all_three_name_tables(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            game = root / "fixture"
            make_my_game_fixture(game)
            data = game / "DATA"
            german = data / "GER"
            german.mkdir()
            label = "Ein Testname"
            text = encode_string(label.encode("cp437")).decode("latin-1")
            placeholder = "[test placeholder]"
            hidden = encode_string(placeholder.encode("cp437")).decode("latin-1")
            (data / "LANDS.GER").write_bytes(write_strings(
                {"offsets": [4, 5 + len(text)], "strings": [text, hidden, ""]}, "<"))
            items = [*call(0x0E, 121, 0x4000, *([0] * 8)), *call(0x0E, 122, 0x4001, *([0] * 8))]
            (data / "ONETIME.INF").write_bytes(script(*items))
            path = write_page(german, root / "page.html", open_page=False)
            page = path.read_text(encoding="utf-8")
            self.assertIn("German text table", page)
            self.assertIn(f"<h3>{label}</h3>", page)
            self.assertIn(f"<td>{label}</td><td>121</td>", page)
            self.assertIn(f"<td>{label}</td><td>0</td>", page)
            self.assertNotIn(placeholder, page)

    def test_save_follows_equipment_handles_and_excludes_empty_party_slots(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            game = root / "game"
            make_my_game_fixture(game)
            slot = bytearray(0x1427F)
            slot[60:65] = b"CD04\0"
            character, state = 76, 0x254
            slot[character + 2:character + 6] = b"Hero"
            slot[character + 132:character + 138] = b"Former"
            pack_into("<H", slot, character, 1)
            pack_into("<H", slot, character + 0x50, 37)
            slot[state + 21] = 1
            pack_into("<H", slot, state + 528, 432)
            pack_into("<H", slot, state + 563 + 16 * 37 + 12, 121)
            source = root / "test.dat"
            source.write_bytes(slot)
            page = app.read_saved(source, game)
            self.assertIn(f"<td>Hero</td><td>{TRANSLATE_FROM}</td>", page)
            self.assertIn(f"{TRANSLATE_FROM} · Gold 432", page)
            self.assertNotIn("Former", page)
            self.assertEqual(source.read_bytes(), slot)


class MyGameDesktop(unittest.TestCase):
    def test_save_report_refuses_to_write_into_the_save_folder(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            saves = root / "saves"
            saves.mkdir()
            source = saves / "slot.dat"
            source.write_bytes(b"saved game")
            fixture = replace(app, read_saved=Mock(return_value="save report"))
            dialogs, messages = Mock(), Mock()
            dialogs.askopenfilename.return_value = str(source)
            dialogs.askdirectory.return_value = str(root / "game")
            with patch("my_game_ui.documents_folder", return_value=saves):
                fixture.open_saved_game(Mock(), dialogs, messages)
            fixture.read_saved.assert_called_once_with(source, root / "game")
            messages.showerror.assert_called_once()
            self.assertEqual(list(saves.iterdir()), [source])
            self.assertEqual(source.read_bytes(), b"saved game")

    def test_default_page_uses_documents_without_overwriting(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            documents = root / "Documents"
            game = root / "game"
            fixture = replace(app, read_page=Mock(return_value="test"))
            with patch("my_game_ui.documents_folder", return_value=documents):
                first = fixture.write_page(game, open_page=False)
                first.write_text("keep this page", encoding="utf-8")
                second = fixture.write_page(game, open_page=False)
                with self.assertRaisesRegex(ValueError, "outside the game folder"):
                    fixture.write_page(root, open_page=False)
            self.assertEqual(first.resolve(), (documents / "LoL1 My Game.html").resolve())
            self.assertEqual(first.read_text(encoding="utf-8"), "keep this page")
            self.assertEqual(second.resolve(), (documents / "LoL1 My Game 2.html").resolve())
            self.assertEqual(second.read_text(encoding="utf-8"), "test")

    def test_cancel_tells_the_player_no_page_was_written(self):
        tkinter = Mock()
        tkinter.TclError = RuntimeError
        tkinter.filedialog.askdirectory.return_value = ""
        with patch("my_game_ui.MyGame.write_page") as write:
            self.assertEqual(app.open_installation(tkinter.Tk.return_value, tkinter.filedialog, tkinter.messagebox), 0)
        write.assert_not_called()
        tkinter.messagebox.showinfo.assert_called_once_with(TITLE, CANCELLED, parent=tkinter.Tk.return_value)

    def test_saved_path_is_shown_with_or_without_browser(self):
        path = Path("Documents", "LoL1 My Game.html")
        for opened in (True, False):
            with self.subTest(opened=opened):
                tkinter = Mock()
                tkinter.TclError = RuntimeError
                tkinter.filedialog.askdirectory.return_value = "game"
                fixture = replace(app, language_options=None)
                with patch("my_game_ui.MyGame.write_page", return_value=path):
                    with patch("my_game_ui.open_report", return_value=opened):
                        self.assertEqual(fixture.open_installation(tkinter.Tk.return_value, tkinter.filedialog,
                                                                   tkinter.messagebox), 0)
                self.assertEqual(tkinter.messagebox.showinfo.call_count, 1)
                self.assertTrue(tkinter.messagebox.showinfo.call_args.args[1].endswith(str(path)))
