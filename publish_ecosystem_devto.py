import os, re, json, urllib.request

FUN = r"C:\Users\zycie\CTOAi-Funnel"
token = open(os.path.join(FUN, ".devto_token"), encoding="utf-8").read().strip()
md = open(os.path.join(FUN, "DEVTO_ECOSYSTEM_ARTICLE.md"), encoding="utf-8").read()

# rozdziel front matter (--- ... ---) od tresci
m = re.match(r"^---\n(.*?)\n---\n(.*)$", md, re.S)
fm = m.group(1); body = m.group(2)
title = re.search(r'title:\s*"(.*?)"', fm).group(1)
tags = re.search(r'tags:\s*(.*)', fm).group(1)
tags = [t.strip() for t in tags.split(",")][:4]  # Dev.to max 4 tagi

payload = {
    "article": {
        "title": title,
        "body_markdown": body,
        "published": True,
        "tags": tags,
    }
}
req = urllib.request.Request(
    "https://dev.to/api/articles",
    data=json.dumps(payload).encode(),
    headers={"api-key": token, "Content-Type": "application/json",
             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
    method="POST",
)
r = urllib.request.urlopen(req, timeout=30)
print("STATUS:", r.status)
print("URL:", r.read().decode())
