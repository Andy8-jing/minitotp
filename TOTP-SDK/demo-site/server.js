// demo-site/server.js —— WxTOTP 演示后端（Node.js + express）
// 仅作接入演示，不可直接用于生产。
const express = require("express");
const totp = require("../sdk/nodejs/wxtotp");

const app = express();
app.use(express.json());
app.use(express.static("public"));

// 演示：单用户内存存储（真实场景应存业务数据库，secret 需加密）
let userSecret = null;

// 1. 开始绑定：生成密钥 + otpauth URI + SVG 二维码
app.get("/api/bind-start", (req, res) => {
  const secret = totp.generateSecret(160);
  userSecret = secret; // 演示用；生产环境请落库
  const uri = totp.buildOtpauthUri("WxTOTP-Demo", "demo@test.local", secret);
  const svg = totp.generateQrSvg(uri);
  res.json({ secret, uri, svg });
});

// 2. 校验验证码
app.post("/api/verify", (req, res) => {
  const { code } = req.body || {};
  if (!userSecret) {
    return res.json({ success: false, msg: "请先发起绑定" });
  }
  const ok = totp.verifyCode(String(code || "").trim(), userSecret, 1, 30, 6);
  res.json({ success: ok, msg: ok ? "校验成功" : "验证码错误或已过期" });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`WxTOTP demo running: http://127.0.0.1:${PORT}`);
});
