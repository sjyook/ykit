# ykit

자주 쓰는 스킬을 모아 직접 관리하는 Claude Code 플러그인입니다.

## 스킬

- [**pick-skills**](skills/pick-skills/SKILL.md): 설치된 플러그인의 스킬 목록에서 가져올 것을 골라 한 번에 포크합니다.
- [**fork-skill**](skills/fork-skill/SKILL.md): GitHub 저장소나 플러그인의 스킬 하나를 출처와 함께 복사합니다.
- [**sync-upstream**](skills/sync-upstream/SKILL.md): 포크한 스킬의 원본 변경을 내 수정 위에 합칩니다.
- [**frame-problem**](skills/frame-problem/SKILL.md): 아이디어를 해결책 중립적인 문제 진술로 다듬습니다.
- [**unslop**](skills/unslop/SKILL.md): writing-clarity, humanize-korean, humanizer를 차례로 돌려 글을 후처리합니다.
- [**sharpen**](skills/sharpen/SKILL.md): 작업 범위를 넓히지 않고 깊게 만든 뒤 프롬프트를 다시 씁니다. pstack에서 포크했습니다.

모두 `/ykit:<이름>`으로 직접 호출합니다.

## 설치

```bash
claude plugin marketplace add sjyook/ykit
claude plugin install ykit@ykit
```
