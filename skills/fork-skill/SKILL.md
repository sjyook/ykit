---
name: fork-skill
description: "Copy a skill from an open GitHub repo into ykit and record where it came from. Use for /ykit:fork-skill <GitHub URL | plugin:skill>."
disable-model-invocation: true
---

Fork one skill into this repository (the ykit plugin root) so I can customize it. Work from the ykit repository root. Do not run `git add`, `git commit`, or `git push`.

Argument: a GitHub URL to the skill's `SKILL.md` or its folder, or `plugin:skill` for an installed plugin.

1. Resolve the source.
   - For a GitHub URL, split it into `repo`, `ref`, and `path`, where `path` is the skill's folder.
   - For `plugin:skill`, read `~/.claude/plugins/installed_plugins.json` to find the plugin's marketplace, then read that marketplace's git remote under `~/.claude/plugins/marketplaces/<marketplace>`. The installed copy can be a build output of another folder in the repo, so find the skill's real folder in the repo (`gh api repos/<repo>/git/trees/<ref>?recursive=1`, filter by the skill name) and show me the `repo` and `path` you found. Wait for my confirmation before continuing.
2. Stop if `skills/<name>/` already exists or `vendor.json` already has the key `skills/<name>`. Never overwrite.
3. Pin the source. `SHA=$(gh api "repos/<repo>/commits?path=<path>&sha=<ref>&per_page=1" --jq '.[0].sha')`. Every file below is fetched at this `SHA`, never at the branch name.
4. Scan for dependencies in the source folder. Report, as a list, each of these that you find:
   - names of other skills in the same plugin
   - `plugin:skill` references
   - agent names or `subagent_type` values
   - relative paths that leave the skill folder (`../`)
   - scripts the skill runs
   For each one, ask me whether to copy it too. Agents go to `agents/<name>.md`, other skills to `skills/<name>/`, and each copied item gets its own `vendor.json` entry. Hooks and MCP servers are not copied; list them for me instead.
5. Copy the folder. List files with `gh api "repos/<repo>/git/trees/$SHA?recursive=1"`, keep the entries under `<path>/`, and write each one to `skills/<name>/` with `gh api "repos/<repo>/contents/<path>/<file>?ref=$SHA" --jq .content | base64 -d`. Do not edit the copied files.
6. Save the license. Look for a LICENSE file at `<path>`'s parent folders up to the repo root at `$SHA`. If `LICENSES/<repo-slug>` does not exist, write it there and tell me which file you used. If you find none, tell me and leave the license field empty.
7. Add the entry to `vendor.json`: `repo`, `path`, `ref`, `baseSha` (the `SHA`), `syncedAt` (today), and `license`.
8. Finish with the list of changed files and a suggested commit message. Stop there.
