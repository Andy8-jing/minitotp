# sdk/python/wxtotp.py —— TOTP 后端 SDK（RFC6238），仅用标准库
import os
import hmac
import hashlib
import time
from urllib.parse import quote
from .base32 import b32decode, b32encode


def generate_secret(bits=160):
    """生成 base32 编码随机密钥（加密安全随机）。"""
    raw = os.urandom((bits + 7) // 8)
    return b32encode(raw)


def build_otpauth_uri(issuer, account, secret, period=30, digits=6):
    """构造 otpauth://totp URI。"""
    return (
        f"otpauth://totp/{quote(issuer)}:{quote(account)}"
        f"?secret={secret}&issuer={quote(issuer)}&period={period}"
        f"&digits={digits}&algorithm=SHA1"
    )


def generate_qr_svg(uri):
    """生成二维码 SVG 文本（可选依赖 qrcode 库）。"""
    try:
        import qrcode
        from io import BytesIO
    except ImportError:
        raise RuntimeError(
            "可选依赖 qrcode 未安装。请先 pip install qrcode[pil]，或用标准库版本跳过二维码。"
        )
    img = qrcode.make(uri)
    buf = BytesIO()
    img.save(buf, format="SVG")
    return buf.getvalue().decode("utf-8")


def calc_totp(secret_b32, ts=None, period=30, digits=6):
    """计算 TOTP 验证码。"""
    if ts is None:
        ts = time.time()
    key = b32decode(secret_b32)
    t_int = int(ts // period)
    t_bytes = t_int.to_bytes(8, byteorder="big")
    h = hmac.new(key, t_bytes, hashlib.sha1).digest()
    offset = h[19] & 0x0F
    bin_code = int.from_bytes(h[offset:offset + 4], byteorder="big") & 0x7FFFFFFF
    mod = 10 ** digits
    return f"{bin_code % mod:0{digits}d}"


def verify_code(input_code, secret_b32, window=1, period=30, digits=6, ts=None):
    """校验验证码，支持时间窗口容错。"""
    if ts is None:
        ts = time.time()
    for i in range(-window, window + 1):
        if calc_totp(secret_b32, ts + i * period, period, digits) == input_code:
            return True
    return False
