from __future__ import annotations

import base64
import random
import secrets
import sys
from pathlib import Path

import _x21


def encrypt_file(key_tag: str, path: Path, seed: int | None = None) -> None:
    path = Path(path)
    assert path.suffix == ".py"

    with path.open() as f:
        source = f.read()

    sbytes = encrypt_string(key_tag, source, seed=seed)

    # write secrets
    spath = path.with_suffix(".dat")
    assert not spath.exists()
    with spath.open("wb") as f:
        f.write(sbytes)

    # override python file
    with path.open("w") as f:
        f.write("import x21\nx21.__dex_23c__(__file__,globals())\n")


def encrypt_string(key_tag: str, message: str, seed: int | None = None) -> bytes | str:
    if key_tag == "22c":
        iv = _get_random_bytes(16, seed)
        iv_smessage = _x21.encrypt_22c(message, iv)
        return base64.a85encode(iv_smessage).decode()

    if key_tag in ["23a", "23b", "23c"]:
        iv = _get_random_bytes(12, seed)
        iv_smessage_tag = _x21.encrypt_23a(message, iv)
        if key_tag == "23a":
            return base64.a85encode(iv_smessage_tag).decode()
        return iv_smessage_tag

    msg = f"Unknown key {key_tag}. Perhaps an earlier version of x21 is required."
    raise ValueError(msg)


def _get_random_bytes(nbytes: int, seed: int | None = None) -> bytes:
    if seed is not None:
        random.seed(seed)
        try:
            # Python 3.9+
            return random.randbytes(nbytes)
        except AttributeError:
            return random.getrandbits(nbytes * 8).to_bytes(nbytes, sys.byteorder)

    return secrets.token_bytes(nbytes)


def __dex_22b__(scope: dict, iv: bytes, smessage: bytes) -> None:
    _x21.decrypt_and_exec_22b(smessage, iv, scope)


def __dex_22c__(scope: dict, iv_smessage: str) -> None:
    data = base64.a85decode(iv_smessage)
    _x21.decrypt_and_exec_22c(data, scope)


def __dex_23a__(scope: dict, iv_smessage_tag: str) -> None:
    data = base64.a85decode(iv_smessage_tag)
    _x21.decrypt_and_exec_23a(data, scope)


def __dex_23b__(scope: dict, data: bytes) -> None:
    # 23b is just like 23a encryption except that byte-strings are exchanged
    _x21.decrypt_and_exec_23a(data, scope)


def __dex_23c__(file: str, scope: dict) -> None:
    # 23c is just like 23a encryption except that only __file__ is given
    file = Path(file).with_suffix(".dat")
    with file.open("rb") as f:
        data = f.read()
    _x21.decrypt_and_exec_23a(data, scope)
