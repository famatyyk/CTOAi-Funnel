import os, re, json, urllib.request

FUN = r"C:\Users\zycie\CTOAi-Funnel"
token = open(os.path.join(FUN, ".devto_token"), encoding="utf-8").read().strip()
md = open(os.path.join(FUN, "CXX_DEVTO_ARTICLE.md"), encoding="utf-8").read()

# frontmatter: ---\ntitle: ...\npublished: false\ntags: ...\n---
m = re.match(r"^---\n(.*?)\n---\n(.*)$", md, re.S)
if not m:
    print("BLAD: brak frontmatter"); raise SystemExit
fm, body = m.group(1), m.group(2).strip()

def get(key):
    line = re.search(rf"^{key}:\s*(.+)$", fm, re.M)
    return line.group(1).strip() if line else ""

title = get("title")
tags_raw = get("tags")
tags = [t.strip() for t in tags_raw.split(",")] if tags_raw else ["cpp"]

# Dev.to API: POST /api/articles
# body_markdown zawiera caly MD (z frontmatter tez jest ok, ale lepiej bez)
payload = {
    "article": {
        "title": title,
        "body_markdown": body,
        "tags": tags,
        "published": True,  # publikuj od razu
    }
}
req = urllib.request.Request(
    "https://dev.to/api/articles",
    data=json.dumps(payload).encode(),
    headers={
        "api-key": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    },
    method="POST",
)
try:
    r = urllib.request.urlopen(req, timeout=30)
    resp = json.loads(r.read().decode())
    print("OPUBLIKOWANO:", r.status)
    print("URL:", resp.get("url"))
    print("ID:", resp.get("id"))
except urllib.error.HTTPError as e:
    print("BLAD HTTP:", e.code, e.read().decode()[:300])
