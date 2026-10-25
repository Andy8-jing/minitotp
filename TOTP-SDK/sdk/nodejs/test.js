// sdk/nodejs/test.js —— RFC6238 官方测试向量
const assert = require("assert");
const totp = require("./wxtotp");
const base32 = require("./base32");

// RFC6238 附录 B 测试向量
// secret 字节 = "12345678901234567890"，标准 base32 = GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ
const SECRET_B32 = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ";
// 官方向量为 8 位输出：
const VECTORS = [
  [59, "94287082"],
  [1111111109, "07081804"],
  [2000000000, "69279037"]
];

for (const [t, expect] of VECTORS) {
  const got = totp.calcTOTP(SECRET_B32, t, 30, 8); // 注意 RFC 向量是 8 位
  const got6 = totp.calcTOTP(SECRET_B32, t, 30, 6);
  // RFC6238 向量为 8 位；本项目默认 6 位，取后 6 位
  assert.strictEqual(got, expect, `T=${t} 8位`);
  assert.strictEqual(got6, expect.slice(-6), `T=${t} 6位`);
  console.log(`PASS T=${t} → ${got}`);
}

// 校验窗口测试
assert.strictEqual(totp.verifyCode(totp.calcTOTP(SECRET_B32, 100, 30, 6), SECRET_B32, 3, 30, 6, 100), true);
assert.strictEqual(totp.verifyCode("000000", SECRET_B32, 1, 30, 6, 100), false);

// base32 roundtrip
const raw = Buffer.from("12345678901234567890");
assert.ok(Buffer.compare(base32.decode(base32.encode(raw)), raw) === 0);

console.log("\n✅ 全部 RFC6238 测试通过");
