# Repository notes

`.gitignore` tells Git which **untracked** local files to leave out of ordinary `git add` operations. The ignore file itself is committed so each clone starts with the same guardrails.

The first group excludes operating-system and editor debris. The Python group excludes caches, virtual environments, and build products while leaving `.py` source, tests, JSON fixtures, and published Markdown reports trackable. The local-settings group excludes environment files and common credential/key formats. The temporary-output group excludes logs, packet captures, and scratch output. The final group excludes raw reports, transcripts, résumés, and local source-evidence directories.

Configuration examples (`.cfg`, `.conf`, `.zone`), diagrams, scripts, tests, and synthetic `.json` files remain publishable. A real configuration still needs a manual privacy review before staging; an allowlisted extension is not a safety check.

Before intentionally adding an ignored file, inspect it and its history with `git status --ignored`, `git check-ignore -v path/to/file`, and a content review. Then stage that exact file with `git add -f path/to/file` only if publication is appropriate. Avoid `git add -f .`.

Ignore rules do not remove a file already tracked by Git. Use `git ls-files` to find tracked files, and review the index with `git diff --cached --name-only` before committing.
