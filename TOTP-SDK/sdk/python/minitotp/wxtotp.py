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
    """生成二维码 SVG 文本（可选依赖 qrcode 库）。

    显式使用 qrcode 的 SVG 路径工厂（``qrcode.image.svg.SvgPathImage``）。
    不要用 ``qrcode.make(uri)`` 的默认工厂：当 PIL 已安装时默认工厂是
    ``PilImage``，其 ``save(format="SVG")`` 会抛 ``KeyError: 'SVG'``
    （PIL 不支持输出 SVG）—— 这是 0.1.0 的已知缺陷，已在 0.1.1 修复。
    """
    try:
        import qrcode
        import qrcode.image.svg
        from io import BytesIO
    except ImportError:
        raise RuntimeError(
            "可选依赖 qrcode 未安装。请先 pip install qrcode[pil]，或用标准库版本跳过二维码。"
        )
    img = qrcode.make(uri, image_factory=qrcode.image.svg.SvgPathImage)
    buf = BytesIO()
    img.save(buf)
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
