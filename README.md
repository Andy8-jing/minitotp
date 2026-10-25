<div align="center">

# minitotp

**Standard TOTP (RFC6238) 2FA SDK · Python / Go / Node.js · Replace SMS verification codes**

English · [简体中文](./README.zh-CN.md)

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![RFC6238](https://img.shields.io/badge/Standard-RFC6238%2F4226-orange.svg)](https://datatracker.ietf.org/doc/html/rfc6238)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](./TOTP-SDK/sdk/python)
[![Go](https://img.shields.io/badge/Go-1.18+-00ADD8?logo=go&logoColor=white)](./TOTP-SDK/sdk/go)
[![Node.js](https://img.shields.io/badge/Node.js-16+-339933?logo=node.js&logoColor=white)](./TOTP-SDK/sdk/nodejs)

</div>

---

## What is this?

**minitotp** is a standard TOTP two-factor authentication SDK for **web service developers**: generate secrets, build otpauth QR codes, and verify 6-digit dynamic codes in your sign-up/login system. Multi-language implementations, with algorithms fully aligned to the official RFC test vectors.

A companion **WxTOTP WeChat Mini Program authenticator** is provided by the operator (closed source). After integrating minitotp, you can guide users to use this authenticator; users are also free to use any standard TOTP authenticator (Microsoft Authenticator / Authy / Google Authenticator).

## 🚀 Live Demo

**Try it online — pure front-end, no server needed:** generate a binding QR code, watch the real-time 6-digit code, and verify it, all in your browser.

👉 **[Open the Live Demo](https://Andy8-jing.github.io/minitotp/)**

Scan the demo QR with the **Mina令牌 (WxTOTP) Mini Program** to bind & verify. Your own project can also use this Mini Program for 2FA — scan, bind, and it works offline.

## Directory structure

```
TOTP-SDK/                  # This repository
├── sdk/
│   ├── python/            # Pure standard-library implementation
│   ├── go/                # Go implementation + tests
│   └── nodejs/            # Node.js implementation + tests
├── demo-site/             # Express demo site (bind + verify flow)
├── docs/
│   └── integrate.md       # Third-party integration guide
└── LICENSE                # MIT
```

## Features

✅ **Standard protocol**: RFC4226 (HOTP) / RFC6238 (TOTP), otpauth:// — interoperable with all standard authenticators
✅ **Cross-language consistency**: all three SDK implementations are aligned and pass the RFC6238 official vectors
✅ **Cryptographically secure**: secrets generated with OS CSPRNG; SDK stores nothing — storage is the business party's responsibility
✅ **Lightweight & dependency-free**: Python/Go core has zero third-party dependencies

## Quick start (Node.js)

```bash
cd sdk/nodejs && npm install && node test.js
```

```js
const totp = require("minitotp");
const secret = totp.generateSecret(160);                       // generate a base32 secret
const uri = totp.buildOtpauthUri("MySite", "user@example.com", secret); // build otpauth URI
const ok = totp.verifyCode(inputCode, secret, 1);              // verify the 6-digit code
```

## Integration steps

1. User enables 2FA: backend calls `generateSecret()` + `buildOtpauthUri()` to create the QR code
2. User scans it with the WxTOTP Mini Program (or any standard authenticator) to bind
3. At login, user submits a 6-digit code and the backend verifies it with `verifyCode()`

> Full integration guide: [`TOTP-SDK/docs/integrate.md`](./TOTP-SDK/docs/integrate.md)

## Security notice

> ⚠️ TOTP is vulnerable to phishing: an attacker can log in with a 6-digit code captured within 30 seconds.
> This project is **not an anti-phishing solution** and cannot replace FIDO2 / WebAuthn (Passkey). Use FIDO2 for high-security scenarios.
> The secret is the root of the credential — the business party must store it encrypted.

## Test vectors (RFC6238)

```
Secret: 12345678901234567890
T = 59           → "94287082"   (8 digits)
T = 1111111109   → "07081804"   (8 digits)
T = 2000000000   → "69279037"   (8 digits)
```

## License

[MIT License](./LICENSE)
