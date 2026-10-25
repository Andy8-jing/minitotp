# WxTOTP 第三方业务接入文档

> 面向业务网站开发者：如何在你的注册/登录系统中接入 WxTOTP（标准 TOTP 二次验证）。
> 用户端可用 WxTOTP 微信小程序，也可用任意标准 TOTP 验证器（微软验证器 / Authy / Google Authenticator）。

## 1. 接入前提

- 你的业务后端支持运行 Python / Go / Node.js 之一
- secret 需落库并**加密存储**（secret 是二次验证的凭证根）
- 登录服务是 HTTPS（保护传输的验证码）

## 2. 三步接入流程

```
① 用户开启2FA  →  后端: generateSecret() 生成密钥 + buildOtpauthUri() 生成二维码
② 用户扫码绑定 →  用户用 WxTOTP 小程序扫描二维码，本地保存密钥
③ 登录校验     →  后端: 用户提交6位验证码 → verifyCode() 校验
```

## 3. 接入示例

### 3.1 用户表新增字段

```sql
-- 以 MySQL 为例
ALTER TABLE users
  ADD COLUMN totp_secret     VARCHAR(128) NULL,   -- base32，需加密存储
  ADD COLUMN totp_enabled    TINYINT(1)  DEFAULT 0,
  ADD COLUMN totp_created_at DATETIME    NULL;
```

### 3.2 开启二次验证（后端生成密钥 + 二维码）

**Node.js**
```js
const totp = require("wxtotp-sdk");

// 1. 生成密钥
const secret = totp.generateSecret(160);

// 2. 生成 otpauth URI（给二维码/手动录入用）
const uri = totp.buildOtpauthUri("MySite", "user@example.com", secret);

// 3. 生成 SVG 二维码（前端渲染展示给用户）
const svg = totp.generateQrSvg(uri);

// 4. 加密后落库
await db.users.update({ totp_secret: encrypt(secret) });
```

**Python**
```python
from wxtotp import generate_secret, build_otpauth_uri

secret = generate_secret(160)
uri = build_otpauth_uri("MySite", "user@example.com", secret)
```

**Go**
```go
secret, _ := GenerateSecret(160)
uri := BuildOtpauthUri("MySite", "user@example.com", secret)
```

### 3.3 绑定校验（用户首次回填验证码，确认绑定）

拿到用户首次输入的 6 位验证码，校验通过才标记 `totp_enabled = 1`。

```js
const ok = totp.verifyCode(inputCode, secret, 1, 30, 6);
if (ok) { await db.users.update({ totp_enabled: 1 }); }
```

### 3.4 登录时校验

```js
// 账号密码校验通过后，再校验 TOTP
const user = await db.users.findByLogin(login);
if (user.totp_enabled) {
  const ok = totp.verifyCode(inputCode, decrypt(user.totp_secret), 1, 30, 6);
  if (!ok) return { error: "验证码错误或已过期" };
}
```

## 4. 接口返回码建议

```json
{ "success": true,  "msg": "校验成功" }
{ "success": false, "msg": "验证码错误或已过期" }
```

## 5. 安全建议（必读）

1. **secret 必须加密存储**：泄露 secret 等于泄露二次验证权限。
2. **校验接口限流**：同一用户 1 分钟内最多 5 次尝试，防暴力枚举。
3. **window 不推荐大于 2**：增大容错会放大重放窗口。
4. **提示用户备份**：绑定页展示明文 base32 密钥，引导用户离线备份。
5. **重置流程**：提供【重置二次验证】，需人工核验身份（如邮箱验证）。
6. **日志**：记录登录 IP / UA，异常登录告警。

## 6. 用户端提示文案（建议）

> 绑定二维码页：
> 「请使用 **WxTOTP 小程序**（或微软验证器 / Authy）扫描二维码完成绑定。绑定后每次登录需输入 6 位动态验证码。」

> 登录验证页：
> 「打开 WxTOTP 小程序，查看对应账号的 6 位动态验证码并输入。」

## 7. 兼容性说明

- 本项目为标准 TOTP（RFC6238），与所有支持 `otpauth://` 的验证器互通。
- **不是防钓鱼方案**：TOTP 无法防御钓鱼网站骗取验证码；高安全场景请改用 FIDO2 / Passkey。
