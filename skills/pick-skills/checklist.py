import argparse
import json
import re
import sys
from pathlib import Path

BLOCK_MARKERS = {">", "|", ">-", "|-", ">+", "|+"}
KEY_LINE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")


def frontmatter_fields(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    body = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        body.append(line)
    fields = {}
    index = 0
    while index < len(body):
        match = KEY_LINE.match(body[index])
        index += 1
        if not match:
            continue
        key, value = match.group(1), match.group(2).strip()
        continuation = []
        while index < len(body) and (body[index].startswith((" ", "\t")) or not body[index].strip()):
            continuation.append(body[index].strip())
            index += 1
        if value in BLOCK_MARKERS:
            value = " ".join(part for part in continuation if part)
        elif continuation:
            value = " ".join([value] + [part for part in continuation if part])
        fields[key] = unquote(value)
    return fields


def unquote(value):
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    return value


def collect(skills_dir, excluded):
    root = Path(skills_dir)
    entries = []
    for path in sorted(root.rglob("SKILL.md")):
        relative = path.parent.relative_to(root)
        if "node_modules" in relative.parts:
            continue
        fields = frontmatter_fields(path.read_text(encoding="utf-8"))
        name = fields.get("name") or path.parent.name
        description = re.sub(r"\s+", " ", fields.get("description", "")).strip()
        entries.append(
            {
                "name": name,
                "description": description,
                "dir": relative.as_posix(),
                "excluded": name in excluded,
            }
        )
    return entries


PAGE = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ykit pick-skills</title>
<style>
:root {
  --bg: #fafaf9;
  --panel: #ffffff;
  --text: #1c1917;
  --muted: #78716c;
  --line: #e7e5e4;
  --accent: #2563eb;
  --accent-text: #ffffff;
  --hover: #f5f5f4;
  --selected: #eff6ff;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #131211;
    --panel: #1c1a19;
    --text: #f5f5f4;
    --muted: #a8a29e;
    --line: #2e2b29;
    --accent: #60a5fa;
    --accent-text: #0b0a09;
    --hover: #262321;
    --selected: #172033;
  }
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font: 15px/1.5 -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Segoe UI", sans-serif;
}
header {
  position: sticky;
  top: 0;
  z-index: 1;
  background: var(--bg);
  border-bottom: 1px solid var(--line);
  padding: 16px 0;
}
.bar, main, footer {
  width: min(960px, calc(100% - 32px));
  margin: 0 auto;
}
.bar {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
}
h1 {
  margin: 0;
  font-size: 17px;
  flex: 1 1 100%;
}
h1 span { color: var(--muted); font-weight: 400; }
input[type="search"] {
  flex: 1 1 240px;
  min-width: 0;
  padding: 8px 12px;
  font: inherit;
  color: var(--text);
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 8px;
}
.count { color: var(--muted); white-space: nowrap; }
button {
  font: inherit;
  padding: 8px 14px;
  border-radius: 8px;
  border: 1px solid var(--line);
  background: var(--panel);
  color: var(--text);
  cursor: pointer;
}
button.primary {
  background: var(--accent);
  border-color: var(--accent);
  color: var(--accent-text);
  font-weight: 600;
}
button:disabled { opacity: 0.45; cursor: default; }
main { padding: 8px 0 32px; }
.row {
  display: grid;
  grid-template-columns: minmax(150px, 220px) 1fr;
  gap: 4px 16px;
  align-items: start;
  padding: 10px 12px;
  border-bottom: 1px solid var(--line);
  border-radius: 6px;
}
.row:hover { background: var(--hover); }
.row.checked { background: var(--selected); }
.row.done { opacity: 0.5; }
.row[hidden] { display: none; }
label.pick {
  display: flex;
  gap: 10px;
  align-items: baseline;
  cursor: pointer;
  min-width: 0;
}
.row.done label.pick { cursor: default; }
input[type="checkbox"] { accent-color: var(--accent); flex: none; }
.name {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 14px;
  font-weight: 600;
  overflow-wrap: anywhere;
}
.group { color: var(--muted); font-weight: 400; }
.tag { color: var(--muted); font-size: 12px; margin-left: 4px; font-weight: 400; }
.desc {
  color: var(--muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  cursor: pointer;
  min-width: 0;
}
.desc.open { white-space: normal; }
footer { padding: 0 0 48px; }
textarea {
  width: 100%;
  min-height: 72px;
  padding: 10px 12px;
  font: 13px/1.5 ui-monospace, SFMono-Regular, Menlo, monospace;
  color: var(--text);
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 8px;
  resize: vertical;
}
.hint { color: var(--muted); font-size: 13px; margin: 6px 0 0; }
@media (max-width: 640px) {
  .row { grid-template-columns: 1fr; }
}
</style>
</head>
<body>
<header>
  <div class="bar">
    <h1>가져올 스킬 고르기 <span id="plugin"></span></h1>
    <input type="search" id="search" placeholder="이름이나 설명으로 검색" autocomplete="off">
    <span class="count" id="count"></span>
    <button type="button" id="clear">선택 해제</button>
    <button type="button" id="copy" class="primary" disabled>복사</button>
  </div>
</header>
<main id="list"></main>
<footer>
  <textarea id="out" readonly placeholder="체크하면 여기에 결과 문자열이 만들어집니다"></textarea>
  <p class="hint" id="hint">복사한 문자열을 Claude Code 채팅에 붙여 넣으세요. 설명을 클릭하면 전체가 펼쳐집니다.</p>
</footer>
<script>
const DATA = __DATA__;
const PLUGIN = __PLUGIN__;
const list = document.getElementById("list");
const out = document.getElementById("out");
const count = document.getElementById("count");
const copy = document.getElementById("copy");
const hint = document.getElementById("hint");
const search = document.getElementById("search");
document.getElementById("plugin").textContent = PLUGIN + " · " + DATA.length + "개";

const rows = DATA.map((item, index) => {
  const row = document.createElement("div");
  row.className = "row" + (item.excluded ? " done" : "");
  row.dataset.text = (item.name + " " + item.description).toLowerCase();

  const label = document.createElement("label");
  label.className = "pick";
  const box = document.createElement("input");
  box.type = "checkbox";
  box.disabled = item.excluded;
  box.dataset.name = item.name;
  const name = document.createElement("span");
  name.className = "name";
  const parts = item.dir.split("/");
  if (parts.length > 1) {
    const group = document.createElement("span");
    group.className = "group";
    group.textContent = parts.slice(0, -1).join("/") + "/";
    name.appendChild(group);
  }
  name.appendChild(document.createTextNode(item.name));
  if (item.excluded) {
    const tag = document.createElement("span");
    tag.className = "tag";
    tag.textContent = "이미 있음";
    name.appendChild(tag);
  }
  label.append(box, name);

  const desc = document.createElement("div");
  desc.className = "desc";
  desc.textContent = item.description || "(설명 없음)";
  desc.addEventListener("click", () => desc.classList.toggle("open"));

  box.addEventListener("change", () => {
    row.classList.toggle("checked", box.checked);
    refresh();
  });
  row.append(label, desc);
  list.appendChild(row);
  return { row, box };
});

function selectedNames() {
  return rows.filter(r => r.box.checked).map(r => r.box.dataset.name);
}

function refresh() {
  const names = selectedNames();
  count.textContent = names.length + "개 선택";
  copy.disabled = names.length === 0;
  out.value = names.length ? "ykit-pick " + PLUGIN + ": " + names.join(", ") : "";
}

search.addEventListener("input", () => {
  const q = search.value.trim().toLowerCase();
  rows.forEach(r => { r.row.hidden = q !== "" && !r.row.dataset.text.includes(q); });
});

document.getElementById("clear").addEventListener("click", () => {
  rows.forEach(r => { r.box.checked = false; r.row.classList.remove("checked"); });
  refresh();
});

copy.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(out.value);
    hint.textContent = "복사했습니다. Claude Code 채팅에 붙여 넣으세요.";
  } catch (error) {
    out.focus();
    out.select();
    hint.textContent = "자동 복사에 실패했습니다. 선택된 문자열을 직접 복사하세요 (Cmd+C).";
  }
});

refresh();
</script>
</body>
</html>
"""


def render_html(entries, plugin):
    data = json.dumps(entries, ensure_ascii=False).replace("</", "<\\/")
    label = json.dumps(plugin, ensure_ascii=False).replace("</", "<\\/")
    return PAGE.replace("__DATA__", data).replace("__PLUGIN__", label)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("skills_dir")
    parser.add_argument("--plugin", default="")
    parser.add_argument("--exclude", default="")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--json", action="store_true")
    mode.add_argument("--html", metavar="OUT")
    args = parser.parse_args()

    excluded = {name.strip() for name in args.exclude.split(",") if name.strip()}
    entries = collect(args.skills_dir, excluded)
    if args.json:
        json.dump(entries, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        Path(args.html).write_text(render_html(entries, args.plugin or Path(args.skills_dir).parent.name), encoding="utf-8")
        print(f"{len(entries)} skills -> {args.html}")


main()
