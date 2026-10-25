<div align="center">

# minitotp

**标准 TOTP（RFC6238）二次验证 SDK · Python / Go / Node.js · 替代短信验证码**

[English](./README.md) · 简体中文

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![RFC6238](https://img.shields.io/badge/标准-RFC6238%2F4226-orange.svg)](https://datatracker.ietf.org/doc/html/rfc6238)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](./TOTP-SDK/sdk/python)
[![Go](https://img.shields.io/badge/Go-1.18+-00ADD8?logo=go&logoColor=white)](./TOTP-SDK/sdk/go)
[![Node.js](https://img.shields.io/badge/Node.js-16+-339933?logo=node.js&logoColor=white)](./TOTP-SDK/sdk/nodejs)

</div>

---

## 这是什么

**minitotp** 是面向**业务网站开发者**的标准 TOTP 二次验证 SDK：在你的注册/登录系统中生成密钥、生成 otpauth 二维码、校验 6 位动态验证码。多语言实现，算法与官方 RFC 测试向量完全对齐。

配套的 **WxTOTP 微信小程序验证器**由运营方提供（闭源）。业务方接入 minitotp 后，可引导用户使用该验证器；用户也可自由选用任意标准 TOTP 验证器（微软验证器 / Authy / Google Authenticator）。

## 目录结构

```
TOTP-SDK/                  # 本仓库
├── sdk/
│   ├── python/            # 纯标准库实现
│   ├── go/                # Go 实现 + 测试
│   └── nodejs/            # Node.js 实现 + 测试
├── demo-site/             # express 演示站点（绑定 + 校验闭环）
├── docs/
│   └── integrate.md       # 第三方业务接入文档
└── LICENSE                # MIT
```

## 特性

✅ **标准协议**：RFC4226(HOTP) / RFC6238(TOTP)、otpauth://，与所有标准验证器互通
✅ **多端一致**：三语言 SDK 算法对齐，全部通过 RFC6238 官方向量
✅ **加密安全**：密钥用操作系统 CSPRNG 生成，不存任何数据，存储交由业务方
✅ **轻量无依赖**：Python/Go 核心零三方依赖

## 快速开始（Node.js）

```bash
cd sdk/nodejs && npm install && node test.js
```

```js
const totp = require("minitotp");
const secret = totp.generateSecret(160);                       // 生成 base32 密钥
const uri = totp.buildOtpauthUri("MySite", "user@example.com", secret); // otpauth URI
const ok = totp.verifyCode(inputCode, secret, 1);              // 校验 6 位验证码
```

## 接入步骤

1. 用户开启 2FA：后端 `generateSecret()` 生成密钥 + `buildOtpauthUri()` 生成二维码
2. 用户用 WxTOTP 小程序（或任意标准验证器）扫码绑定
3. 登录时用户提交 6 位验证码，后端 `verifyCode()` 校验

> 完整接入见 [`TOTP-SDK/docs/integrate.md`](./TOTP-SDK/docs/integrate.md)

## 安全声明

> ⚠️ TOTP 存在钓鱼风险：仿站拿到 30s 内的 6 位验证码即可登录。
> 本项目**不是防钓鱼方案**，不能替代 FIDO2 / WebAuthn(Passkey)。高安全场景请使用 FIDO2。
> secret 是凭证根，业务方必须加密存储。

## 测试向量（RFC6238）

```
Secret: 12345678901234567890
T = 59           → "94287082"   (8位)
T = 1111111109   → "07081804"   (8位)
T = 2000000000   → "69279037"   (8位)
```

## 协议

[MIT License](./LICENSE)
