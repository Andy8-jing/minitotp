// Package wxtotp 提供 TOTP (RFC6238) 后端 SDK：生成密钥、otpauth URI、校验验证码。
package wxtotp

import (
	"crypto/hmac"
	"crypto/rand"
	"crypto/sha1"
	"encoding/base32"
	"fmt"
	"strings"
	"time"
)

// GenerateSecret 生成 base32 编码随机密钥（加密安全随机）。
func GenerateSecret(bits int) (string, error) {
	if bits <= 0 {
		bits = 160
	}
	l := (bits + 7) / 8
	buf := make([]byte, l)
	if _, err := rand.Read(buf); err != nil {
		return "", err
	}
	return base32.StdEncoding.WithPadding(base32.NoPadding).EncodeToString(buf), nil
}

// BuildOtpauthUri 构造 otpauth://totp URI。
func BuildOtpauthUri(issuer, account, secret string, period, digits int) string {
	return fmt.Sprintf(
		"otpauth://totp/%s:%s?secret=%s&issuer=%s&period=%d&digits=%d&algorithm=SHA1",
		issuer, account, secret, issuer, period, digits,
	)
}

// CalcTOTP 计算 TOTP 验证码。
// ts: unix 秒；period: 步长（默认 30）；digits: 位数（默认 6）。
func CalcTOTP(secretB32 string, ts float64, period, digits int) (string, error) {
	if period <= 0 {
		period = 30
	}
	if digits <= 0 {
		digits = 6
	}
	key, err := base32.StdEncoding.WithPadding(base32.NoPadding).DecodeString(strings.ToUpper(secretB32))
	if err != nil {
		return "", err
	}

	T := uint64(ts / float64(period))
	tBuf := make([]byte, 8)
	for i := 7; i >= 0; i-- {
		tBuf[i] = byte(T & 0xff)
		T >>= 8
	}

	mac := hmac.New(sha1.New, key)
	mac.Write(tBuf)
	hash := mac.Sum(nil)

	offset := hash[19] & 0x0f
	bin := int64(hash[offset]&0x7f)<<24 |
		int64(hash[offset+1])<<16 |
		int64(hash[offset+2])<<8 |
		int64(hash[offset+3])

	mod := int64(1)
	for i := 0; i < digits; i++ {
		mod *= 10
	}
	code := bin % mod
	return fmt.Sprintf("%0*d", digits, code), nil
}

// VerifyCode 校验验证码，支持时间窗口容错（window=1 校验 ±1 时间片）。
// ts==0 时使用当前时间。
func VerifyCode(inputCode, secretB32 string, window, period, digits int, ts float64) (bool, error) {
	if ts == 0 {
		ts = float64(time.Now().Unix())
	}
	for i := -window; i <= window; i++ {
		c, err := CalcTOTP(secretB32, ts+float64(i*period), period, digits)
		if err != nil {
			return false, err
		}
		if c == inputCode {
			return true, nil
		}
	}
	return false, nil
}
