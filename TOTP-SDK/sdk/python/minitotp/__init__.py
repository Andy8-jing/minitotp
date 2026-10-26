# minitotp —— 标准 TOTP（RFC6238）二次验证 SDK（纯标准库）
"""Standard TOTP (RFC6238) two-factor authentication SDK.

Pure standard-library implementation. Provides secret generation, otpauth
URI building, optional QR SVG, TOTP calculation and verification.
"""

from .wxtotp import (
    generate_secret,
    build_otpauth_uri,
    generate_qr_svg,
    calc_totp,
    verify_code,
)

__version__ = "0.1.0"
__all__ = [
    "generate_secret",
    "build_otpauth_uri",
    "generate_qr_svg",
    "calc_totp",
    "verify_code",
]
