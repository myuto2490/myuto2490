"""オリジナルの数字画像（7 セグメント風 SVG）で閲覧数を描く。
外部の画像やフォントは使わず、線だけで数字を描く。
見る人の GitHub がダーク/ライトのどちらでも見えるよう、SVG 内の CSS で色を切り替える。"""
import sys

SEG = {  # 各数字で点灯するセグメント
    "0": "abcdef", "1": "bc", "2": "abdeg", "3": "abcdg", "4": "bcfg",
    "5": "acdfg", "6": "acdefg", "7": "abc", "8": "abcdefg", "9": "abcdfg",
}
TILE_W, TILE_H, GAP, PAD = 44, 68, 8, 2
X0, X1, Y0, YM, Y1 = 12, 32, 12, 34, 56  # タイル内の数字の骨格
S = 3.5  # 線の端の余白

def segments():
    return {
        "a": (X0 + S, Y0, X1 - S, Y0), "g": (X0 + S, YM, X1 - S, YM), "d": (X0 + S, Y1, X1 - S, Y1),
        "f": (X0, Y0 + S, X0, YM - S), "b": (X1, Y0 + S, X1, YM - S),
        "e": (X0, YM + S, X0, Y1 - S), "c": (X1, YM + S, X1, Y1 - S),
    }

def render(n: int, digits: int = 7, label: str = "PROFILE VIEWS") -> str:
    s = str(max(0, int(n))).rjust(digits, "0")
    w = PAD * 2 + len(s) * TILE_W + (len(s) - 1) * GAP
    h = PAD * 2 + TILE_H + 22
    parts = []
    for i, ch in enumerate(s):
        tx = PAD + i * (TILE_W + GAP)
        parts.append(f'<g transform="translate({tx},{PAD})"><rect class="tile" width="{TILE_W}" height="{TILE_H}" rx="9"/>')
        for name, (x1, y1, x2, y2) in segments().items():
            cls = "on" if name in SEG[ch] else "off"
            parts.append(f'<line class="{cls}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')
        parts.append("</g>")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}: {int(n)}">
<title>{label}: {int(n)}</title>
<style>
.tile{{fill:#111111}} .on{{stroke:#ffffff}} .off{{stroke:#ffffff;opacity:.08}}
line{{stroke-width:5;stroke-linecap:round}}
.label{{fill:#57606a;font:600 11px -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;letter-spacing:3px}}
@media (prefers-color-scheme: dark){{
  .tile{{fill:#f0f0f0}} .on{{stroke:#111111}} .off{{stroke:#111111;opacity:.08}} .label{{fill:#8b949e}}
}}
</style>
{"".join(parts)}
<text class="label" x="{w/2}" y="{h-4}" text-anchor="middle">{label}</text>
</svg>
'''

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    out = sys.argv[2] if len(sys.argv) > 2 else "counter.svg"
    open(out, "w").write(render(n))
    print("wrote", out)
