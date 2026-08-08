# Reddit post — C++ audit (krótki)

Sub: r/cpp  (lub r/Cplusplus, r/learncpp)
Tytuł: Built a static C++ analyzer — ran it on a 10-line snippet, caught 4 issues

Treść:
I made Project Doctor — a static audit tool for C++ repos (no compile needed,
no deps installed, no code run). Just structure + risk patterns → prioritized report.

Tested it on a deliberately ugly 10-liner:

    char* buf = new char[256];   // raw new
    strcpy(buf, "hello");        // unsafe
    printf("val=%d\n", 42);      // printf family
    int* p = (int*)buf;          // C-style cast
    goto cleanup;                 // goto

Flags: strcpy (HIGH), raw new (MED), C-cast (LOW), goto (LOW). Score 16/100.

Not a clang-tidy replacement — it's the "pre-flight check" before you set up a
pipeline or hand off to a client.

If useful, full tool here (from 29 EUR for C++): https://ctoai-funnel.fly.dev/
Sample Python audit: https://github.com/famatyyk/project-doctor-samples
