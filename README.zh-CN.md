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

**比手机短信验证码更优的替代方案。** 不用为短信 OTP 付费、等待，minitotp 在**用户设备本地**生成同样的 6 位验证码——无需短信网关、离线可用、更安全：

| 短信验证码 | minitotp (TOTP) |
|---|---|
| ❌ 每条短信计费，需短信网关 | ✅ **零成本**，本地生成 |
| ❌ 依赖运营商/信号/网络，有延迟 | ✅ **离线可用**，30s 即时出码 |
| ❌ 可被 SIM 卡劫持 / 短信拦截 | ✅ **不经过短信通道**，更安全 |
| ❌ 需要收集手机号 | ✅ **无需手机号**，保护隐私 |

配套的 **微信小程序：Mina令牌**（标准 TOTP 验证器）由运营方提供（闭源）。业务方接入 minitotp 后，可引导用户使用该小程序；用户也可自由选用任意标准 TOTP 验证器（微软验证器 / Authy / Google Authenticator）。

![Mina令牌 小程序码](docs/mina-miniprogram-qr.png)

## 🚀 在线体验（Live Demo）

**无需部署、纯前端运行**：生成绑定二维码 → 实时查看 6 位动态验证码 → 输入校验，全在浏览器完成。

👉 **[打开在线体验](https://Andy8-jing.github.io/minitotp/)**

用 **微信小程序：Mina令牌** 扫码绑定即可体验（扫码绑定、离线出码）；你自己的项目接入本 SDK 后，同样可让用户用这个小程序完成二次验证。

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

## 快速开始（Python）

从 PyPI 安装——纯标准库，无三方依赖：

```bash
pip install minitotp
```

```python
from minitotp import generate_secret, build_otpauth_uri, verify_code
secret = generate_secret()                                     # 生成 base32 密钥
uri = build_otpauth_uri("MySite", "user@example.com", secret)  # 生成 otpauth URI
ok = verify_code(input_code, secret, 1)                        # 校验 6 位验证码
```

### 端到端示例（复制即可运行）

一个覆盖 **后端 → 验证器/前端 → 后端** 全链路的自包含流程。复制保存为 `demo.py`，`pip install minitotp` 后直接运行：

```python
from minitotp import generate_secret, build_otpauth_uri, calc_totp, verify_code

# ① 后端：为用户开启 2FA → 生成密钥 + otpauth URI（把 URI 转成二维码给用户扫）
secret = generate_secret()
uri = build_otpauth_uri("MySite", "user@example.com", secret)
print("绑定 URI:", uri)

# ② 验证器 / 前端：用户扫码绑定后，用同一 secret 计算当前 6 位动态码
code = calc_totp(secret)
print("验证器显示:", code)

# ③ 后端：登录时校验用户提交的 6 位码
print("后端校验:", "通过 ✓" if verify_code(code, secret) else "失败 ✗")
```

## 接入步骤

1. 用户开启 2FA：后端 `generateSecret()` 生成密钥 + `buildOtpauthUri()` 生成二维码
2. 用户用 微信小程序：Mina令牌（或任意标准验证器）扫码绑定
3. 登录时用户提交 6 位验证码，后端 `verifyCode()` 校验

> 完整接入见 [`TOTP-SDK/docs/integrate.md`](./TOTP-SDK/docs/integrate.md)

## 安全声明

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
