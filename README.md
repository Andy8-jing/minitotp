<div align="center">

# WxTOTP

**微信小程序版标准 TOTP 验证器 + 多语言后端 SDK · 替代短信验证码**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![RFC6238](https://img.shields.io/badge/标准-RFC6238%2F4226-orange.svg)](https://datatracker.ietf.org/doc/html/rfc6238)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](./TOTP-SDK/sdk/python)
[![Go](https://img.shields.io/badge/Go-1.18+-00ADD8?logo=go&logoColor=white)](./TOTP-SDK/sdk/go)
[![Node.js](https://img.shields.io/badge/Node.js-16+-339933?logo=node.js&logoColor=white)](./TOTP-SDK/sdk/nodejs)
[![微信小程序](https://img.shields.io/badge/WeChat-MiniProgram-07C160?logo=wechat&logoColor=white)](./WxTOTP/miniprogram)

</div>

---

## 项目组成

| 目录 | 说明 |
|---|---|
| **`WxTOTP/`** | 原生微信小程序：扫码/手动添加、AES 本地加密、离线计算 6 位动态验证码、导入导出备份 |
| **`TOTP-SDK/`** | 多语言后端 SDK（Python / Go / Node.js）：生成密钥、otpauth URI、SVG 二维码、校验验证码 |
| **`TOTP-SDK/demo-site/`** | express 演示站点：绑定二维码 + 校验闭环（已端到端验证） |
| **`TOTP-SDK/docs/`** | 第三方业务接入文档 `integrate.md` |
| **`WxTOTP/docs/`** | 完整开发文档 `dev.md` |

## 特性

✅ **去中心化**：没有中心化服务，密钥只存业务数据库 + 用户小程序本地
✅ **标准协议**：otpauth://totp，与 Microsoft Authenticator / Authy / Google Authenticator 双向互通
✅ **离线计算**：小程序全程离线，密钥不上传任何服务器
✅ **多端一致**：三语言 SDK 与小程序算法对齐，全部通过 RFC6238 官方向量

## 快速开始（后端，Node.js 示例）

```js
const totp = require("wxtotp-sdk");
const secret = totp.generateSecret(160);            // 生成 base32 密钥
const uri = totp.buildOtpauthUri("MySite", "user@example.com", secret); // otpauth URI
const ok = totp.verifyCode(inputCode, secret, 1);  // 校验 6 位验证码
```

> 详见 [`TOTP-SDK/README.md`](./TOTP-SDK/README.md) 与 [`TOTP-SDK/docs/integrate.md`](./TOTP-SDK/docs/integrate.md)

## 小程序能力

- 扫码解析 otpauth:// 二维码（`wx.scanCode`）
- 手动录入 base32 密钥
- AES-256 本地加密存储，支持本地解锁密码（PBKDF2 派生）
- 倒计时进度条、一键复制验证码
- 单条 / 批量导入、导出密钥备份

## 安全声明

> ⚠️ TOTP 存在钓鱼风险：仿站拿到 30s 内的 6 位验证码即可登录。
> 本项目**不是防钓鱼方案**，不能替代 FIDO2 / WebAuthn(Passkey)。高安全场景请使用 FIDO2。

## 测试向量（RFC6238）

```
Secret: 12345678901234567890
T = 59           → "94287082"   (8位)
T = 1111111109   → "07081804"   (8位)
T = 2000000000   → "69279037"   (8位)
```

## 协议

[MIT License](./LICENSE)
