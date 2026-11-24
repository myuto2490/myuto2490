"""komarev の閲覧数を読み取り、オリジナルの数字画像 counter/views.svg を作り直す。
GitHub Actions から定期的に実行する。
komarev は GitHub の画像プロキシ経由の表示だけを数えるので、ここで直接読み取っても数は増えない。"""
import json, os, re, sys, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import render

HERE = os.path.dirname(os.path.abspath(__file__))
cfg = json.load(open(os.path.join(HERE, "config.json")))
url = f"https://komarev.com/ghpvc/?username={cfg['username']}&style=for-the-badge"
req = urllib.request.Request(url, headers={"User-Agent": "profile-counter-updater"})
svg = urllib.request.urlopen(req, timeout=30).read().decode()
m = re.search(r'aria-label="[^"]*?:\s*([\d,]+)"', svg)
if not m:
    sys.exit("閲覧数を読み取れませんでした")
total = int(m.group(1).replace(",", ""))
views = max(0, total - cfg.get("offset", 0))

out = os.path.join(HERE, "views.svg")
new = render(views)
old = open(out).read() if os.path.exists(out) else ""
if new != old:
    open(out, "w").write(new)
    print(f"updated: {views}")
else:
    print(f"unchanged: {views}")
