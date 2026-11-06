# ykit

자주 쓰는 스킬을 모아서 직접 관리하는 Claude Code 플러그인입니다. 새 PC에서는 이 저장소 하나만 설치하면 됩니다.

## 새 PC에 설치

저장소를 GitHub에 올린 뒤 실행합니다.

```
claude plugin marketplace add <GitHub 계정>/ykit
claude plugin install ykit@ykit
```

로컬 저장소에서 바로 설치하려면 첫 줄의 인자를 저장소 경로(`~/personal/ykit`)로 바꿉니다. 비공개 저장소라면 먼저 `gh auth login`이 필요합니다.

### 다른 플러그인에 의존하게 될 때

의존성은 `.claude-plugin/plugin.json`의 `dependencies`에 `"이름@마켓플레이스"` 형식으로 적고, `.claude-plugin/marketplace.json`의 `allowCrossMarketplaceDependenciesOn`에 그 마켓플레이스 이름을 넣습니다. 현재는 의존성이 없습니다.

플러그인은 다른 마켓플레이스를 스스로 등록하지 못합니다. 의존하는 마켓플레이스를 먼저 추가한 다음 ykit을 설치해야 하고, 순서를 어기면 설치는 성공으로 표시되지만 ykit이 `failed to load` 상태가 됩니다(`claude plugin list`로 확인). 의존성을 추가하면 이 절의 설치 순서에 `claude plugin marketplace add`를 마켓플레이스마다 한 줄씩 먼저 적어 둡니다.

## 구조

| 경로 | 내용 |
|---|---|
| `skills/<name>/` | 포크해서 내가 고쳐 쓰는 스킬 |
| `agents/<name>.md` | 스킬이 의존하는 agent |
| `vendor.json` | 포크한 항목의 출처(저장소, 경로, 마지막으로 맞춘 원본 커밋). 스킬 폴더 밖이라 컨텍스트에 로드되지 않음 |
| `LICENSES/` | 원본 저장소의 LICENSE |

## 스킬 가져오기와 원본 변경 반영

- `/ykit:fork-skill <GitHub URL 또는 plugin:skill>`: 스킬 폴더를 원본의 특정 커밋 기준으로 복사하고 `vendor.json`에 출처를 기록합니다. 스킬이 의존하는 다른 스킬, agent, 상대 경로를 찾아 함께 가져올지 묻습니다.
- `/ykit:sync-upstream [skills/<name>]`: 마지막으로 맞춘 커밋 이후 원본이 바뀌었는지 확인합니다. 바뀌었다면 `git merge-file`로 그 변화를 내 수정 위에 합칩니다. 충돌이 남아 있는 동안에는 `vendor.json`의 기준 커밋을 바꾸지 않습니다.

두 스킬 모두 커밋과 push는 하지 않습니다.
