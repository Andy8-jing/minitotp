// wxtotp_test.go —— RFC6238 官方测试向量
package wxtotp

import "testing"

// RFC6238 附录 B 测试向量（secret 字节 = "12345678901234567890"）
// 标准 base32 编码 = GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ
const secretB32 = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ"

func TestRFC6238Vectors(t *testing.T) {
	cases := []struct {
		ts   float64
		want string
	}{
		{59, "94287082"},
		{1111111109, "07081804"},
		{2000000000, "69279037"},
	}
	for _, c := range cases {
		got, err := CalcTOTP(secretB32, c.ts, 30, 8) // RFC 向量为 8 位
		if err != nil {
			t.Fatalf("T=%v err=%v", c.ts, err)
		}
		if got != c.want {
			t.Errorf("T=%v got=%s want=%s", c.ts, got, c.want)
		}
		// 本项目默认 6 位，取后 6 位
		got6, _ := CalcTOTP(secretB32, c.ts, 30, 6)
		if got6 != c.want[len(c.want)-6:] {
			t.Errorf("T=%v 6位 got=%s want=%s", c.ts, got6, c.want[len(c.want)-6:])
		}
	}
}

func TestVerifyCode(t *testing.T) {
	now := float64(100)
	code, _ := CalcTOTP(secretB32, now, 30, 6)
	ok, err := VerifyCode(code, secretB32, 3, 30, 6, now)
	if err != nil || !ok {
		t.Errorf("窗口内校验应通过: ok=%v err=%v", ok, err)
	}
	bad, err := VerifyCode("000000", secretB32, 1, 30, 6, now)
	if err != nil || bad {
		t.Errorf("错误验证码不应通过: bad=%v err=%v", bad, err)
	}
}

func TestGenerateSecret(t *testing.T) {
	s1, _ := GenerateSecret(160)
	s2, _ := GenerateSecret(160)
	if s1 == s2 {
		t.Errorf("两次生成的密钥不应相同")
	}
	if len(s1) < 20 {
		t.Errorf("160bit base32 编码长度过短: %d", len(s1))
	}
}
