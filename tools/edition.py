#!/usr/bin/env python3
"""Compare your original LoL1 install with the measured edition fingerprints."""
from hashlib import sha256
import os
from pathlib import Path

from cli_errors import ReaderArgumentParser, run_cli


WITNESSES = {'English CD 1.02': {'HARDRIVE/MAIN.EXE': (356928, '10a9bdce8e234a917da36bbdfe5434add3d9ce01f0ea9b132a95b2fd1ef03e23'),
                'HARDRIVE/MAINW.EXE': (352656, '3fb3b4a92ff4c5d4dccdaa66a1e3b6309c7bc30491cbb5eed9c63ef1f27fe935'),
                'HARDRIVE/LOLCD.EXE': (19356, '80ea9411ca772d2c3d5ac2ae614f4a12f7f5b7b71a96938925469c815fc694c5'),
                'ENG/LANDS.EXE': (357509, '5c0c5478df61a421a04d86ef10548ab73e775ed15d79d35bfa88c4ef5a5ec21c'),
                'ENG/FINALE.EXE': (132328, '406c8460617d4553f17215fc1ea98d182c081a303296e83a037a1c0df1ac9550'),
                'FRE/LANDS.EXE': (359338, '0eab44f69a5e99f07969027c13425f04a96df58d5d9a33bd0cfd3da1d645f529'),
                'FRE/FINALE.EXE': (134122, '14522084432e13d045b17786a7e404b80de36e37ea18b80898a257303b8ec235'),
                'GER/LANDS.EXE': (359418, 'decc1cfce8adddd8aa880414ce569b97a9cb5bc4bfab45da5b0db805f65d204f'),
                'GER/FINALE.EXE': (134212, 'e2817d8e28040da8dd568c81bdc00a9aa68cfe34b6c83022fc8fd6a66a3b2384'),
                'GENERAL.PAK': (1225033, 'e6a3ef89f39c1679b8de3cbe343bdaf20e1d4612eb7778d5bf75ca3015eab265'),
                'STARTUP.PAK': (167273, '926e61c3c99a05c85a4820570345844de4fa0c99793191055071f787ab54d12d'),
                'L01.PAK': (68733, 'c52c240f093dafe405f6f318cbdc4bcaddbe05bea443e274bae18b75281ec2ac')},
 'English floppy 1.05': {'MAIN.EXE': (373872, '4077ab84d19db6e16015b6d7752b4757344397dfce61a9caefd9b74701cc5a10'),
                         'LANDS.EXE': (129490, '01152602d9e6e8945b19de41b221f2c7e5f5aa63788872e08269c40595197438'),
                         'FINALE.EXE': (162728, '859f67e5b36abf79e3af96e0fe2715861fe7d65bb19834acceef2b327646cf8f'),
                         'GENERAL.PAK': (1383453, '4248f0cea0489b804a15d68e70ce6afe5eb2dc7a6339ff7064b16b0125a92128'),
                         'CHAPTER1.PAK': (2287611, '237e44d218ad8f52fd4520bf083f3ee3c0307b65d43507b2230a508ff3a89398'),
                         'CHAPTER7.PAK': (325053, '928129c3117978dcb61fc4f70ba7fbb2ad8b7c377b2675daff3c88e49fc97234')}}
SUBFOLDER = "DATA"
DATA_ENV = "LOL1_DATA"


def locate(root, name):
    for part in name.split("/"):
        if not root.is_dir():
            return None
        root = next((entry for entry in root.iterdir() if entry.name.casefold() == part.casefold()), None)
        if root is None:
            return None
    return root if root.is_file() else None


def identify(root):
    names = dict.fromkeys(name for rows in WITNESSES.values() for name in rows)
    if SUBFOLDER == "DATA":
        root = next((p for p in root.iterdir() if p.is_dir() and p.name.upper() == SUBFOLDER), root)
    elif SUBFOLDER == "DAT" and root.name.upper() == "DAT":
        root = root.parent
    found = {}
    for name in names:
        path = locate(root, name)
        if path is not None:
            with path.open("rb") as stream:
                found[name] = (path.stat().st_size, sha256_stream(stream))
    return root, found


def sha256_stream(stream):
    digest = sha256()
    for block in iter(lambda: stream.read(1024 * 1024), b""):
        digest.update(block)
    return digest.hexdigest()


def status(expected, observed):
    if observed is None:
        return "missing"
    return "matches" if observed == expected else "differs"


def main(argv=None):
    parser = ReaderArgumentParser(description=__doc__)
    default = os.environ.get(DATA_ENV)
    parser.add_argument("--data", type=Path, default=default, required=default is None,
                        help=f"your game folder or its {SUBFOLDER} folder (default: ${DATA_ENV})")
    parser.add_argument("--check", action="store_true",
                        help="verify that all fingerprint files match a measured edition")
    args = parser.parse_args(argv)
    root, found = identify(args.data.resolve())
    if not found:
        parser.error(f"No edition files found in {root}. Give --data your original game installation or its data folder.")

    def score(edition):
        _, rows = edition
        return (all(found.get(name) == value for name, value in rows.items()),
                sum(found.get(name) == value for name, value in rows.items()),
                sum(name in found for name in rows))

    label, rows = max(WITNESSES.items(), key=score)
    statuses = {name: status(value, found.get(name)) for name, value in rows.items()}
    differences = [f"{name} {value}" for name, value in statuses.items() if value != "matches"]
    summary = f"{label}: all {len(rows)} fingerprint files match in {root}."
    if args.check:
        if differences:
            raise ValueError(f"The {label} fingerprint does not match in {root} ({', '.join(differences)}). "
                             "Check an unmodified copy or run without --check for sizes and checksums.")
        print(f"CHECK edition: {summary}")
        return 0

    print("File | Bytes | SHA-256 | Status")
    for name, result in statuses.items():
        size, checksum = found.get(name, ("—", "—"))
        print(f"{name} | {size} | {checksum} | {result}")
    if differences:
        print(f"No complete edition fingerprint matches in {root}. The table compares with {label}.")
        return 1
    print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
