"""Check the one-page guide with invented maps and names."""
from importlib.util import find_spec
import re
from pathlib import Path
from struct import pack_into
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import Mock, patch

from tests.test_level_tools import TOOLS
from tests.kit_fixture import make_fixture, TRANSLATE_FROM

from my_game import CANCELLED, GameFolderError, TITLE, WRONG_FOLDER, desktop, game_page, write_page


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
                game_page(folder)
            self.assertEqual(str(problem.exception), WRONG_FOLDER)
            make_my_game_fixture(folder)
            (folder / "DATA" / "L29.PAK").unlink()
            with self.assertRaises(GameFolderError) as problem:
                game_page(folder)
            self.assertEqual(str(problem.exception), WRONG_FOLDER)


class MyGameDesktop(unittest.TestCase):
    def test_default_page_uses_documents_without_overwriting(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            documents = root / "Documents"
            game = root / "game"
            with patch("my_game.documents_folder", return_value=documents), patch("my_game.game_page", return_value="test"):
                first = write_page(game, open_page=False)
                first.write_text("keep this page", encoding="utf-8")
                second = write_page(game, open_page=False)
                with self.assertRaisesRegex(ValueError, "outside the game folder"):
                    write_page(root, open_page=False)
            self.assertEqual(first.resolve(), (documents / "LoL1 My Game.html").resolve())
            self.assertEqual(first.read_text(encoding="utf-8"), "keep this page")
            self.assertEqual(second.resolve(), (documents / "LoL1 My Game 2.html").resolve())
            self.assertEqual(second.read_text(encoding="utf-8"), "test")

    def test_cancel_tells_the_player_no_page_was_written(self):
        tkinter = Mock()
        tkinter.TclError = RuntimeError
        tkinter.filedialog.askdirectory.return_value = ""
        with patch.dict("sys.modules", tkinter=tkinter), patch("my_game.write_page") as write:
            self.assertEqual(desktop(), 0)
        write.assert_not_called()
        tkinter.messagebox.showinfo.assert_called_once_with(TITLE, CANCELLED, parent=tkinter.Tk.return_value)

    def test_saved_path_is_shown_with_or_without_browser(self):
        path = Path("Documents", "LoL1 My Game.html")
        for opened in (True, False):
            with self.subTest(opened=opened):
                tkinter = Mock()
                tkinter.TclError = RuntimeError
                tkinter.filedialog.askdirectory.return_value = "game"
                with patch.dict("sys.modules", tkinter=tkinter), patch("my_game.write_page", return_value=path):
                    with patch("my_game.open_report", return_value=opened):
                        self.assertEqual(desktop(), 0)
                self.assertEqual(tkinter.messagebox.showinfo.call_count, 1)
                self.assertTrue(tkinter.messagebox.showinfo.call_args.args[1].endswith(str(path)))
