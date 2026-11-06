---
name: sync-upstream
description: "Check forked skills for upstream changes and merge them into my customized copies. Use for /ykit:sync-upstream [skills/<name>]."
disable-model-invocation: true
---

Bring upstream changes into the skills I forked. Work from the ykit repository root. Do not run `git add`, `git commit`, or `git push`.

Argument: optional key from `vendor.json` (for example `skills/sharpen`). With no argument, handle every entry.

For each entry:

1. Read `repo`, `path`, `ref`, and `baseSha` from `vendor.json`. Decide whether the folder changed by comparing its tree SHA at `baseSha` and at `<ref>`: run `gh api "repos/<repo>/contents/<parent of path>?ref=<X>" --jq '.[] | select(.path=="<path>") | .sha'` once with `<X>` = `baseSha` and once with `<X>` = `<ref>`. If the two are equal, report "no upstream change" and go to the next entry. Do not compare commit SHAs here: a `baseSha` pinned for a whole plugin can be newer than the last commit that touched this folder. Otherwise get the latest upstream commit for the folder: `LATEST=$(gh api "repos/<repo>/commits?path=<path>&sha=<ref>&per_page=1" --jq '.[0].sha')`.
2. Show what changed upstream. List the commits between the two points that touched the folder (`gh api "repos/<repo>/commits?path=<path>&sha=<ref>"`, stop at `baseSha`) with date and first line, then the per-file changes from `gh api "repos/<repo>/compare/<baseSha>...$LATEST"` limited to files under `<path>/`. This is how upstream changed, not how my copy differs. Ask me whether to merge.
3. Merge file by file into a scratch directory outside the repo. For each file under `<path>/` that exists in my copy and upstream:
   - fetch the base: `gh api "repos/<repo>/contents/<path>/<file>?ref=<baseSha>" --jq .content | base64 -d > base`
   - fetch the latest the same way with `ref=$LATEST` into `theirs`
   - copy my file to `mine`, then run `git merge-file -L mine -L base -L upstream mine base theirs`
   - exit code 0 means a clean merge. A positive exit code is the number of conflicts and the file now holds conflict markers. A negative exit code means an error such as a binary file; skip that file and report it.
   Files that are new upstream or deleted upstream are not merged automatically; list them and ask me what to do. Only after all files are done, write the `mine` results over my files.
4. If any file has conflict markers, show me each conflict, leave the markers in the file, and do not change `baseSha`. Tell me to resolve the markers and run this skill again; when a re-run finds no markers it can set `baseSha`.
5. When every file merged cleanly or the conflicts are resolved, set `baseSha` to `$LATEST` and `syncedAt` to today in `vendor.json`. If upstream had no `LICENSES` change, leave the license file alone; if the upstream LICENSE changed, say so.
6. Finish with the list of changed files and a suggested commit message. Stop there.
