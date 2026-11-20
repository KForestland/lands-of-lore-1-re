"""Edition comparison tests using synthetic bytes only."""
from contextlib import redirect_stdout
from hashlib import sha256
from io import StringIO
import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import edition


class EditionCheck(unittest.TestCase):
    def test_statuses_and_check_from_environment(self):
        with TemporaryDirectory(prefix="edition test ") as folder:
            install = Path(folder)
            data = install / edition.SUBFOLDER
            data.mkdir()
            base = data if edition.SUBFOLDER == "DATA" else install
            expected = (len(b"original"), sha256(b"original").hexdigest())
            witness = {"Example edition": {name: expected for name in
                                          ("ENGINE.DAT", "COPIED.DAT", "ABSENT.DAT")}}
            (base / "ENGINE.DAT").write_bytes(b"original")
            (base / "COPIED.DAT").write_bytes(b"altered!")
            with patch.object(edition, "WITNESSES", witness), patch.dict(os.environ, {edition.DATA_ENV: str(data)}):
                output = StringIO()
                with redirect_stdout(output):
                    self.assertEqual(edition.main([]), 1)
                text = output.getvalue()
                self.assertRegex(text, r"(?m)^ENGINE\.DAT .* \| matches$")
                self.assertRegex(text, r"(?m)^COPIED\.DAT .* \| differs$")
                self.assertRegex(text, r"(?m)^ABSENT\.DAT .* \| missing$")
                with self.assertRaisesRegex(ValueError, "COPIED.DAT differs, ABSENT.DAT missing"):
                    edition.main(["--check"])
                for name in witness["Example edition"]:
                    (base / name).write_bytes(b"original")
                output = StringIO()
                with redirect_stdout(output):
                    self.assertEqual(edition.main(["--check"]), 0)
                self.assertEqual(len(output.getvalue().splitlines()), 1)
                self.assertIn("CHECK edition: Example edition: all 3", output.getvalue())
