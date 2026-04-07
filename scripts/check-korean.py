#!/usr/bin/env python3
"""
check-korean.py — Pure Korean verifier
Usage: echo "text" | python3 check-korean.py
   or: python3 check-korean.py "text"
   or: pipe any text through it

Exit codes:
  0 = PASS (0 non-Korean characters found)
  1 = FAIL (found Chinese/Hanja/Kana)
  2 = ERROR (no input)
"""
import sys
import re

# Unicode ranges for Chinese, Japanese, and Hanja
NON_KOREAN_RANGES = [
    (0x4E00, 0x9FFF),    # CJK Unified Ideographs (includes Hanja)
    (0x3400, 0x4DBF),    # CJK Extension A
    (0x20000, 0x2A6DF),  # CJK Extension B
    (0x3040, 0x309F),    # Hiragana (Japanese)
    (0x30A0, 0x30FF),    # Katakana (Japanese)
    (0x3400, 0x4DBF),    # Korean Hanja Extension
    (0xAC00, 0xD7AF),    # Korean Hangul (this is OK! but check context)
]

def check_text(text: str) -> tuple[list[str], list[tuple[int, str]]]:
    """Return (found_non_korean_chars, list_of_positions_and_chars)"""
    found = []
    positions = []
    for i, char in enumerate(text):
        cp = ord(char)
        # Skip Hangul (Korean) — range AC00-D7AF
        if 0xAC00 <= cp <= 0xD7AF:
            continue
        # Skip ASCII
        if cp < 128:
            continue
        # Check if it's in any non-Korean range
        for start, end in NON_KOREAN_RANGES:
            if start <= cp <= end:
                # Exception: some Hangul Compatibility Jamo (1100-11FF) is OK
                if 0x1100 <= cp <= 0x11FF:
                    continue
                # Exception: halfwidth Katakana (FF65-FF9F) — usually Japanese
                if 0xFF65 <= cp <= 0xFF9F:
                    found.append(char)
                    positions.append((i, char))
                    break
                # CJK/Hiragana/Katakana
                found.append(char)
                positions.append((i, char))
                break

    return found, positions

def main():
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = sys.stdin.read()

    if not text.strip():
        print("ERROR: No input text", file=sys.stderr)
        sys.exit(2)

    found, positions = check_text(text)
    unique_chars = sorted(set(found), key=lambda c: ord(c))

    if found:
        print(f"FAIL: {len(found)}개 발견")
        print(f"문자: {''.join(unique_chars)}")
        print()
        print("위치별:")
        for pos, char in positions:
            print(f"  [{pos}] '{char}' (U+{ord(char):04X})")
        print()
        print("대체어 참조:")
        replacements = {
            '歴史':'이야기', '歴史的':'이야기적', '歴史적':'이야기적',
            '經濟':'살림', '경제적':'살림적',
            '日本':'Japan', '日本的':'Japan식',
            '中國':'China', '중국적':'China式',
            '確認':'살피기', '確認해':'살피고',
            '結果':'결과', '結果적':'결과적',
            '環境':'주변', '환경적':'주변적',
            '管理':'보기', '관리적':'보기적',
            '問題':'걱정', '문제적':'걱정적',
            '必要':'꼭', '필요한':'꼭 필요한',
            '現在':'지금', '현재의':'지금의',
            '重要':'아주 중요', '중요한':'아주 중요한',
            '一般':'평소', '일반적':'평소적',
            '모든':'다', '매우':'아주',
            'システム':'시스템', 'システム的':'시스템적',
            'プログラム':'프로그램',
            'コンピュータ':'컴퓨터',
            'デザイン':'디자인',
            'ユーザー':'유저',
            'サービス':'서비스',
            '処理':'처리',
            '生成':'만들기',
            '機能':'기능',
            '状態':'상태',
            '作業':'일',
            '上の':'이거', '위의':'이거',
            '以下の':' 아래', '이하의':' 아래의',
        }
        for char in unique_chars:
            if char in replacements:
                print(f"  {char} → {replacements[char]}")
        print()
        sys.exit(1)
    else:
        print(f"PASS: 0개 (검증 통과)")
        sys.exit(0)

if __name__ == "__main__":
    main()
