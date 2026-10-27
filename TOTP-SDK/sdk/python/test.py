# sdk/python/test.py —— RFC6238 官方测试向量
from minitotp.base32 import b32encode, b32decode
from minitotp import calc_totp, verify_code

# RFC6238 附录 B 测试向量
# secret 字节 = b"12345678901234567890"
SECRET_B32 = b32encode(b"12345678901234567890")  # => GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ
# 官方向量为 8 位输出：
VECTORS = [
    (59, "94287082"),
    (1111111109, "07081804"),
    (2000000000, "69279037"),
]

for t, expect in VECTORS:
    got = calc_totp(SECRET_B32, t, 30, 8)        # RFC 向量为 8 位
    got6 = calc_totp(SECRET_B32, t, 30, 6)       # 本项目默认 6 位
    assert got == expect, f"T={t} 8位失败: {got} != {expect}"
    assert got6 == expect[-6:], f"T={t} 6位失败"
    print(f"PASS T={t} -> {got}")

# 校验窗口
assert verify_code(calc_totp(SECRET_B32, 100, 30, 6), SECRET_B32, 3, 30, 6, 100)
assert not verify_code("000000", SECRET_B32, 1, 30, 6, 100)

# base32 roundtrip
raw = b"12345678901234567890"
assert b32decode(b32encode(raw)) == raw

# 二维码 SVG（回归：0.1.0 的 generate_qr_svg 用 PIL 工厂输出 SVG 会 KeyError）
from minitotp import build_otpauth_uri, generate_qr_svg
uri = build_otpauth_uri("minitotp", "demo", SECRET_B32)
svg = generate_qr_svg(uri)
assert isinstance(svg, str) and "<svg" in svg, "generate_qr_svg 应返回合法 SVG"
print("PASS generate_qr_svg ->", len(svg), "bytes")

print("\n✅ 全部 RFC6238 测试通过")
