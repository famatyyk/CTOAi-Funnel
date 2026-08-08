---
title: "I ran a static analyzer on a tiny C++ file — it caught 4 real issues in 10 lines"
published: false
description: "What a static C++ audit flags, why it matters even for small code, and how to get one for your repo."
tags: cpp, cplusplus, security, codereview, showdev
---

# I ran a static analyzer on a tiny C++ file — it caught 4 real issues in 10 lines

I build **Project Doctor** — a static audit tool for repos (Python, C++, Lua, JS/TS). It doesn't run your code, doesn't install deps, doesn't read secrets. It just inventories structure, scans for risk patterns, and gives you a prioritized report.

To sanity-check the C++ analyzer, I threw a deliberately ugly 10-line snippet at it:

```cpp
#include <cstdio>
#include <cstring>

int main() {
    char* buf = new char[256];      // raw new
    strcpy(buf, "hello");           // unsafe function
    printf("val=%d\n", 42);         // printf family
    int* p = (int*)buf;             // C-style cast
    goto cleanup;                    // goto
    cleanup:
    return 0;
}
```

## What it flagged

| Severity | Issue | Why it matters |
| --- | --- | --- |
| **HIGH** | `strcpy` (unsafe C function) | Buffer overflow risk — use `std::string` / `snprintf` |
| **MEDIUM** | Raw `new` without ownership | Leak risk — use `std::unique_ptr` / `std::shared_ptr` |
| **LOW** | C-style cast | Prefer `static_cast` / `const_cast` for type safety |
| **LOW** | `goto` | Hurts readability — use loops/functions/`std::expected` |

Result: **16/100**. (Yes, a 10-line toy file scores 16. Real projects with tests/CI/clean structure score much higher.)

## Why this isn't "just use clang-tidy"

`clang-tidy` is great. But it requires you to set up the build, compile flags, and a working toolchain. Project Doctor is for the moment **before** that — when you want to know *what to fix* without configuring a pipeline. It's the "pre-flight check" for a client handoff or open-source release.

## Try it

- **From 19 EUR** (Python/Lua/JS/TS) · **29 EUR** (C++)
- Report in Markdown + JSON, 24–48h
- 100% static — no code execution, no dependency install

👉 https://ctoai-funnel.fly.dev/

*Sample audit of `requests` (Python) here: https://github.com/famatyyk/project-doctor-samples*

---

*Found something wrong in this post? Comment — I'll fix it. (I audit my own tool's repo too.)*
