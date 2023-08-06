from __future__ import annotations

import base64
import random
import secrets
import sys

import _x21


def encrypt_string(key_tag: str, message: str, seed: int | None = None) -> bytes | str:
    if key_tag == "22c":
        iv = _get_random_bytes(16, seed)
        iv_smessage = _x21.encrypt_22c(message, iv)
        return base64.a85encode(iv_smessage).decode()

    if key_tag == "23a":
        iv = _get_random_bytes(12, seed)
        iv_smessage_tag = _x21.encrypt_23a(message, iv)
        return base64.a85encode(iv_smessage_tag).decode()

    if key_tag == "23b":
        iv = _get_random_bytes(12, seed)
        # 23b is just like 23a encryption except that byte-strings are
        # exchanged
        iv_smessage_tag = _x21.encrypt_23a(message, iv)
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


def __dex_22b__(glob: dict, iv: bytes, smessage: bytes) -> None:
    _x21.decrypt_and_exec_22b(smessage, iv, glob)


def __dex_22c__(glob: dict, iv_smessage: str) -> None:
    data = base64.a85decode(iv_smessage)
    _x21.decrypt_and_exec_22c(data, glob)


def __dex_23a__(glob: dict, iv_smessage_tag: str) -> None:
    data = base64.a85decode(iv_smessage_tag)
    _x21.decrypt_and_exec_23a(data, glob)


def __dex_23b__(glob: dict, data: bytes) -> None:
    # 23b is just like 23a encryption except that byte-strings are exchanged
    _x21.decrypt_and_exec_23a(data, glob)
