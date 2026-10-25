// sdk/nodejs/wxtotp.js —— TOTP 后端 SDK（RFC6238）
const crypto = require("crypto");
const base32 = require("./base32");

// qrcode-svg 是可选依赖：用于生成 SVG 二维码
let QRCodeSvg = null;
try {
  QRCodeSvg = require("qrcode-svg");
} catch (e) {
  /* 可选，未安装则 generateQrSvg 不可用 */
}

/**
 * 生成 base32 编码随机密钥（加密安全随机）。
 * @param {number} bits 默认 160
 * @returns {string}
 */
function generateSecret(bits = 160) {
  const buf = crypto.randomBytes(Math.ceil(bits / 8));
  return base32.encode(buf).replace(/=+$/, "");
}

/**
 * 构造 otpauth://totp URI。
 */
function buildOtpauthUri(issuer, account, secret, period = 30, digits = 6) {
  return (
    "otpauth://totp/" +
    encodeURIComponent(issuer) +
    ":" +
    encodeURIComponent(account) +
    "?secret=" +
    secret +
    "&issuer=" +
    encodeURIComponent(issuer) +
    "&period=" +
    period +
    "&digits=" +
    digits +
    "&algorithm=SHA1"
  );
}

/**
 * 生成二维码 SVG 文本（可选依赖 qrcode-svg）。
 */
function generateQrSvg(uri) {
  if (!QRCodeSvg) {
    throw new Error("缺少可选依赖 qrcode-svg，请执行 npm install");
  }
  return new QRCodeSvg({ content: uri, padding: 2, width: 220, height: 220 }).svg();
}

/**
 * 计算 TOTP 验证码。
 * @param {string} secretB32
 * @param {number} ts      unix 秒
 * @param {number} period  默认 30
 * @param {number} digits  默认 6
 * @returns {string}
 */
function calcTOTP(secretB32, ts = Date.now() / 1000, period = 30, digits = 6) {
  const keyBuf = base32.decode(secretB32);
  const T = BigInt(Math.floor(ts / period));

  const tBuf = Buffer.alloc(8);
  tBuf.writeBigUInt64BE(T, 0);

  const hmac = crypto.createHmac("sha1", keyBuf);
  hmac.update(tBuf);
  const hash = hmac.digest();

  const offset = hash[19] & 0x0f;
  const bin = hash.readUInt32BE(offset) & 0x7fffffff;

  const mod = Math.pow(10, digits);
  return (bin % mod).toString().padStart(digits, "0");
}

/**
 * 校验验证码，支持时间窗口容错。
 * @param {string} inputCode
 * @param {string} secretB32
 * @param {number} window  默认 1
 * @param {number} period
 * @param {number} digits
 * @param {number} now     unix 秒（默认当前）
 * @returns {boolean}
 */
function verifyCode(inputCode, secretB32, window = 1, period = 30, digits = 6, now = Date.now() / 1000) {
  for (let i = -window; i <= window; i++) {
    const c = calcTOTP(secretB32, now + i * period, period, digits);
    if (c === inputCode) return true;
  }
  return false;
}

module.exports = { generateSecret, buildOtpauthUri, generateQrSvg, calcTOTP, verifyCode };
