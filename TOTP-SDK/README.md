# minitotp — TOTP 二次验证 SDK

> **minitotp** 标准 TOTP 后端 SDK：多语言实现（Python / Go / Node.js）+ Demo 站点
> MIT License | RFC4226 / RFC6238 | 兼容 otpauth:// 协议

供业务网站集成：生成密钥、生成 otpauth 二维码、校验 6 位动态验证码。用户端配套使用微信小程序：Mina令牌（也可用任意标准 TOTP 验证器）。

![Mina令牌 小程序码](../docs/mina-miniprogram-qr.png)

## 在线体验（Live Demo）

纯前端运行，**无需部署服务器**，密钥在浏览器本地生成、不上传任何数据：

- 生成绑定二维码（otpauth:// 标准协议）
- 实时查看 6 位动态验证码（RFC 6238，30s 刷新）
- 输入验证码即时校验（±1 时间片容错）

👉 **点击体验**：`https://<你的用户名>.github.io/<仓库名>/`（GitHub Pages 免费托管）

![Mina令牌 TOTP 在线体验演示](docs/demo-screenshot.png)

> 演示页源码：`demo-site/public/index.html`（单文件，无外部依赖，可放到任意静态托管）。

## 目录结构

```
TOTP-SDK/
├── README.md
├── sdk/
│   ├── nodejs/
│   │   ├── wxtotp.js       # 主逻辑
│   │   ├── base32.js
│   │   ├── package.json
│   │   └── test.js         # RFC6238 测试向量
│   ├── python/
│   │   ├── wxtotp.py
│   │   ├── base32.py       # 纯 Python base32（无三方依赖）
│   │   └── test.py
│   └── go/
│       ├── wxtotp.go
│       ├── wxtotp_test.go
│       └── go.mod
└── demo-site/
    ├── server.js           # Node.js 演示后端
    └── public/
        └── index.html      # 演示页面（生成二维码 + 校验）
└── docs/
    └── integrate.md        # 第三方业务接入文档（数据库字段/示例/安全建议）
```

## 核心 API（三语言一致）

| 函数 | 作用 |
|---|---|
| `generateSecret(bits=160)` | 生成 base32 编码随机密钥 |
| `buildOtpauthUri(issuer, account, secret, ...)` | 生成 otpauth://totp URI |
| `generateQrSvg(uri)` | 生成二维码 SVG 文本 |
| `calcTOTP(secret, ts, period, digits)` | 计算动态验证码（内部） |
| `verifyCode(code, secret, window=1, ...)` | 校验验证码（容错 ±window 时间片） |

## 快速接入（后端）

### Node.js
```bash
cd sdk/nodejs
npm install            # 安装 qrcode-svg（可选，仅二维码需要）
node test.js           # 跑测试向量
```
> 依赖需安装在 `sdk/nodejs`（SDK 文件所在目录），不要在 `demo-site` 下单独装，否则 `require` 找不到。
```js
const totp = require("./sdk/nodejs/wxtotp");
const secret = totp.generateSecret();
const uri = totp.buildOtpauthUri("MySite", "user@test.com", secret);
const svg = totp.generateQrSvg(uri);
const ok = totp.verifyCode("123456", secret);
```

### Python
```bash
pip install minitotp        # 发布 PyPI 后可直接安装
# 本地开发模式：cd sdk/python && pip install -e .
```
```python
from minitotp import generate_secret, build_otpauth_uri, verify_code
secret = generate_secret()
uri = build_otpauth_uri("MySite", "user@test.com", secret)
ok = verify_code("123456", secret)
```
> 注：`generate_qr_svg` 需要可选依赖 `qrcode[pil]`（`pip install minitotp[qr]`）；核心算法只用标准库。测试：`cd sdk/python && python3 test.py`

#### 端到端示例（后端 → 前端 → 后端，复制即用）

覆盖「后端生成绑定 → 验证器/前端计算动态码 → 后端校验」全链路，`pip install minitotp` 后直接运行：

```python
from minitotp import generate_secret, build_otpauth_uri, calc_totp, verify_code

# ① 后端：开启 2FA，生成密钥 + otpauth URI（转二维码给用户扫）
secret = generate_secret()
uri = build_otpauth_uri("MySite", "user@example.com", secret)
print("绑定 URI:", uri)

# ② 验证器 / 前端：扫码绑定后用同一 secret 计算当前 6 位码
code = calc_totp(secret)
print("验证器显示:", code)

# ③ 后端：登录时校验用户提交的 6 位码
print("后端校验:", "通过 ✓" if verify_code(code, secret) else "失败 ✗")
```

### Go
```bash
cd sdk/go
go test ./...
```
```go
secret, _ := GenerateSecret(160)
uri := BuildOtpauthUri("MySite", "user@test.com", secret)
ok, _ := VerifyCode("123456", secret, 1, 30, 6, 0)
```

## 校验窗口说明

`window=1` 代表校验当前时间片及其前后各 1 个（共 3 个，容错 ±30s）。业务方可按需调整，但**不推荐大于 2**（增加重放风险）。

## 安全约束

1. 密钥必须使用加密安全随机数（`crypto.randomBytes` / `os.urandom` / `crypto/rand`）
2. SDK 本身不存储数据；secret 由业务方数据库保管，**必须加密存储**
3. 校验接口建议限流：同一用户 1 分钟内最多 5 次尝试，防暴力枚举

## 测试向量（RFC6238）

```
Secret: 12345678901234567890
T = 59   → "287082"
T = 1111111109 → "081804"
T = 2000000000 → "692790"
```

## 协议

MIT License
