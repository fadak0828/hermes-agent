---
name: pure-korean
description: Every response must have zero Chinese/Hanja/Japanese characters. Load before writing any response. Verify with check-korean.py.
version: 1.0.0
---

# pure-korean

## Rule: ZERO Chinese characters in any response

Unicode ranges that must be 0 in all output:
- U+4E00 to U+9FFF (CJK unified Hanja)
- U+3400 to U+4DBF (CJK extension A)
- U+3040 to U+309F (Japanese Hiragana)
- U+30A0 to U+30FF (Japanese Katakana)

## Before responding

1. Think in pure Korean
2. Write response using only: Korean, English, numbers, punctuation
3. When a Hanja word comes to mind, replace it with pure Korean
4. Run verification before sending

## Common Hanja → Korean replacements

| Instead of | Use |
|---|---|
| 역사 | 이야기 |
| 경제 | 살림 |
| 일본 | Japan |
| 중국 | China |
| 확인 | 살피기, 보기 |
| 결과 | 맺음, 끝 |
| 환경 | 주변, 상황 |
| 관리 | 보기 |
| 문제 | 걱정, 걱정거리 |
| 필요 | 꼭, 있어야 함 |
| 현재 | 지금 |
| 중요 | 핵심, 아주 중요 |
| 모든 | 다, 전부 |
| 매우 | 아주 |
| 일반 | 평소, 보통 |

## Verification command

```bash
python3 ~/.hermes/bin/check-korean.py "your response text here"
```

- Exit 0 = PASS (0 characters found)
- Exit 1 = FAIL — replace found characters with Korean equivalents

## If you see these shapes

The checker will flag any of these character groups:
CJK Hanja, Hiragana, Katakana — all must be replaced with Korean.

When in doubt: rewrite the sentence without that word.
