// sdk/nodejs/base32.js —— RFC4648 Base32 编解码
const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";

/**
 * Base32 编码（无填充）。
 * @param {Buffer} buf
 * @returns {string}
 */
function encode(buf) {
  let bits = "";
  for (const b of buf) bits += b.toString(2).padStart(8, "0");
  let out = "";
  for (let i = 0; i + 5 <= bits.length; i += 5) {
    out += alphabet[parseInt(bits.slice(i, i + 5), 2)];
  }
  return out;
}

/**
 * Base32 解码。
 * @param {string} s
 * @returns {Buffer}
 */
function decode(s) {
  s = s.toUpperCase().replace(/[^A-Z2-7]/g, "");
  let bits = "";
  for (const c of s) bits += alphabet.indexOf(c).toString(2).padStart(5, "0");
  const arr = [];
  for (let i = 0; i + 8 <= bits.length; i += 8) {
    arr.push(parseInt(bits.slice(i, i + 8), 2));
  }
  return Buffer.from(arr);
}

module.exports = { encode, decode };
