# sdk/python/base32.py —— RFC4648 Base32（纯标准库实现）
import re

_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
_ALPHABET_REVERSE = {c: i for i, c in enumerate(_ALPHABET)}


def b32decode(s):
    """Base32 解码，忽略大小写与非 base32 字符，返回 bytes。"""
    s = s.upper()
    s = re.sub(r"[^A-Z2-7]", "", s)
    bits = ""
    for c in s:
        bits += format(_ALPHABET_REVERSE[c], "05b")
    out = bytearray()
    for i in range(0, len(bits) - 7, 8):
        out.append(int(bits[i:i + 8], 2))
    return bytes(out)


def b32encode(buf):
    """Base32 编码（无填充），返回 str。"""
    bits = "".join(format(b, "08b") for b in buf)
    out = []
    for i in range(0, len(bits) - 4, 5):
        out.append(_ALPHABET[int(bits[i:i + 5], 2)])
    return "".join(out)
