---
name: pick-skills
description: "Show every skill of a plugin as a checklist, let me pick which to bring into ykit, and fork them all together. Use for /ykit:pick-skills <plugin>."
disable-model-invocation: true
---

Let me choose skills from one plugin, then fork all of them in one pass. Work from the ykit repository root. Do not run `git add`, `git commit`, or `git push`.

Argument: a plugin name such as `pstack` or `pstack@cursor-plugins`.

1. Find the plugin. Read `~/.claude/plugins/installed_plugins.json` and take the `installPath` of the matching plugin. If it is not installed, ask me for the source GitHub URL and stop using the installed copy.
2. Build the list. Run `python3 <this skill's folder>/checklist.py <installPath>/skills --plugin <name> --exclude <names> --json`, where `<names>` is the comma-separated list of folder names under ykit's `skills/` plus the last path segment of every key in `vendor.json`. Skills that are already in ykit come back with `excluded: true`; tell me how many were left out.
3. Let me choose. Count the entries with `excluded: false`.
   - 16 or fewer: ask with AskUserQuestion, up to 4 questions of up to 4 options each, all `multiSelect`. The option label is the skill name and the description is the skill's own description, cut at 200 characters.
   - 17 or more: run the same script with `--html <scratch dir>/pick-<name>.html` instead of `--json`, open the file with `open`, and tell me to check skills and press the copy button. I paste back one line shaped like `ykit-pick <plugin>: a, b, c`. Split it into names and stop if any name is not in the list.
4. Ask the confirmations once, for all chosen skills together.
   - The source repository and skill folder path: confirm once per plugin, not per skill. The installed copy can be a build output of another folder in the repo (pstack builds from `harness/pstack/claude-code`, while its source skills live under `pstack/skills/<name>`). Find the real folder from the repo tree and show me the `repo` and `path` pattern you found.
   - Dependencies: scan every chosen skill the way step 4 of `skills/fork-skill/SKILL.md` does, merge the results into one list grouped by what they are, and let me pick which to copy too, in a single question.
5. Fork. Pin one commit for the whole run: the latest commit that touched the plugin's skills folder in the source repo. For each chosen skill, follow steps 2, 3, 5, 6, and 7 of `skills/fork-skill/SKILL.md` using that single commit as `SHA`. Do not ask any question during this step. Skip a skill that already exists and say so at the end. Copy the dependencies I approved the same way.
6. Finish with the list of forked skills, the skipped ones, the changed files, and a suggested commit message. Stop there.
