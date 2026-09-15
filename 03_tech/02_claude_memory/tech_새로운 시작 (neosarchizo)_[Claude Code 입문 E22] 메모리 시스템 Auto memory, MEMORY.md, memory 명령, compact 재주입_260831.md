# 새로운 시작 (neosarchizo) | [Claude Code 입문 E22] 메모리 시스템: Auto memory, MEMORY.md, /memory 명령, /compact 재주입

## Metadata
- **채널:** 새로운 시작 (neosarchizo)
- **URL:** https://youtu.be/2RJWSWcomQU
- **Duration:** 14:05
- **Upload Date:** 2026-04-27
- **목적:** MEMORY 관리
- **변환일:** 2026-08-31

---

## 핵심 요약
- Claude Code는 사용자가 정의하는 `CLAUDE.md`와 Claude가 스스로 학습하여 기록하는 Auto memory 시스템을 병행하여 사용한다.
- Auto memory는 로컬 머신에만 저장되며 Git으로 공유되지 않으므로, 팀 공통 규칙은 반드시 `CLAUDE.md`에 작성해야 한다.
- `/compact` 명령으로 컨텍스트를 압축하더라도 `CLAUDE.md`와 Auto memory의 내용은 자동으로 재주입(Re-injected)되어 유지된다.
- Subagent는 별도의 `memory` 필드 설정을 통해 프로젝트 스코프의 공유 가능한 메모리를 가질 수 있다.

---

## 적용 지식

### CLAUDE.md와 Auto memory의 비교 [00:11]
Claude Code는 두 가지 방식의 메모리를 사용하여 프로젝트의 컨텍스트를 유지한다. 이 둘은 서로 대체하는 것이 아니라 상호 보완적인 관계이다.

| 항목 | CLAUDE.md | Auto memory |
| :--- | :--- | :--- |
| **작성 주체** | 사용자(User) | Claude |
| **내용** | 규칙(Rules) 및 지시 사항 | 학습된 패턴(Learned patterns) |
| **적용 범위** | Project / User / Org 단위 | Working tree 단위 |
| **로드 방식** | 전체 로드(Full) | 첫 200줄 또는 25KB까지만 로드 |
| **용도** | 표준 정의(Standards) | 인사이트 및 사용자 선호도 파악 |
| **공유 방식** | GitHub 등 Git을 통한 팀 공유 | 로컬 머신 전용(Machine-local) |

### Auto memory의 작동 원리와 저장 내용 [01:28]
Auto memory는 Claude가 사용자의 작업 방식, 수정 사항, 선호도를 바탕으로 스스로 노트를 남기는 시스템이다. Claude는 미래의 대화에 유용하다고 판단되는 가치 있는 정보만을 선택적으로 저장한다. 주요 저장 대상은 빌드 명령(Build commands), 디버깅 인사이트(Debugging insights), 아키텍처 노트(Architecture notes), 코드 스타일 선호도(Code style preferences), 반복되는 워크플로우 습관 등이다.

세션 도중 Claude가 메모리를 조작할 때 다음과 같은 메시지가 표시된다:
- `Writing memory`: Claude가 메모리 파일에 내용을 쓰는 중임을 의미한다.
- `Recalled memory`: 저장된 메모리 파일을 읽어와 컨텍스트에 반영했음을 의미한다.

### 메모리 저장 구조 및 로드 제한 [02:09]
각 프로젝트는 별도의 메모리 디렉토리를 가지며, Git 저장소 정보를 기반으로 경로가 생성된다. 따라서 동일한 저장소의 모든 워크트리(worktrees)는 하나의 메모리 디렉토리를 공유한다.

**기본 저장 경로:**
`~/.claude/projects/<project>/memory/`

**디렉토리 내부 구성:**
- `MEMORY.md`: 어떤 토픽 파일이 있는지 요약하는 간결한 인덱스(Concise index) 파일이다.
- **Topic Files**: 상세한 내용이 담긴 개별 파일들이다 (예: `debugging.md`, `api-conventions.md`).

**로드 한계(Load limit):**
`MEMORY.md` 파일은 세션 시작 시 **앞 200줄(Lines)** 또는 **25KB** 중 먼저 도달하는 조건까지만 자동으로 로드된다. 이 한계를 넘는 상세 내용은 토픽 파일로 분리되어야 하며, Claude는 세션 도중 필요할 때만 `read` 도구를 사용하여 해당 토픽 파일을 온디맨드(on-demand) 방식으로 불러온다. 반면 `CLAUDE.md`는 크기와 상관없이 항상 전체가 로드된다.

### Auto memory 활성화 및 비활성화 방법 [04:23]
Auto memory는 기본적으로 활성화(`on`) 상태이며, 세 가지 방법으로 끌 수 있다.

1. **명령어 사용**: `/memory` 명령어를 입력한 후 엔터(Enter)를 눌러 `Auto-memory: on/off` 상태를 토글한다.
2. **설정 파일 수정**: `~/.claude/settings.json` 파일에서 `autoMemoryEnabled` 값을 수정한다.
   ```json
   {
     "autoMemoryEnabled": false
   }
   ```
3. **환경 변수 설정**: 터미널에서 환경 변수를 내보낸다.
   ```bash
   export CLAUDE_CODE_DISABLE_AUTO_MEMORY=1
   ```

### 저장 위치 변경 및 설정 레이어 [05:17]
메모리 저장 경로를 기본값 외의 장소로 변경하려면 `autoMemoryDirectory` 설정을 사용한다. 이 설정은 보안상의 이유로 프로젝트 루트의 `.claude/settings.json`에서는 거부되며, `user`, `local`, `policy` 레이어에서만 허용된다.

- **사용자 전체 적용**: `~/.claude/settings.json`
- **특정 프로젝트 로컬 적용**: 프로젝트 내 `.claude/settings.local.json`

```json
{
  "autoMemoryEnabled": true,
  "autoMemoryDirectory": "~/my-memory-dir"
}
```

### /memory 명령어의 기능 [06:25]
`/memory` 명령어는 다음 네 가지 핵심 기능을 제공한다.
1. **목록 표시**: 현재 세션에 로드된 `./CLAUDE.md`, `CLAUDE.local.md`, `.rules` 파일 목록을 보여준다.
2. **토글**: Auto memory의 활성 상태를 전환한다.
3. **폴더 링크**: Auto memory가 저장된 로컬 폴더를 즉시 열 수 있는 링크를 제공한다.
4. **에디터 연결**: 목록에서 파일을 선택하여 에디터(Editor)로 즉시 열고 수정할 수 있다.

### 영속적 기억을 위한 지시 방법 [07:22]
대화 중 특정 정보를 영구적으로 남기고 싶을 때, 목적에 따라 지시어를 구분해야 한다.
- **Auto memory에 저장**: "앞으로 이 프로젝트에서는 항상 pnpm을 사용해줘" 또는 "API 테스트에 local Redis가 필요하다는 걸 기억해줘"라고 말하면 Claude가 스스로 메모리에 기록한다.
- **CLAUDE.md에 저장 (팀 공유)**: "이 내용을 CLAUDE.md에 추가해줘"라고 명시적으로 지시하거나 사용자가 직접 파일을 편집한다.

### /compact 명령 후의 컨텍스트 유지 [08:32]
`/compact` 명령을 사용하여 대화 이력을 압축할 때, 항목별 유지 상태는 다음과 같다.

| 항목 | 압축 후 상태 |
| :--- | :--- |
| System prompt / output style | 유지(Preserved) |
| Project root CLAUDE.md | 디스크에서 다시 읽어 재주입(Re-injected) |
| Auto memory | 재주입(Re-injected) |
| paths: scoped rules | 해당 파일 재매칭 전까지 유실(Lost) |
| Nested subdirectory CLAUDE.md | 해당 폴더 파일 재판독 전까지 유실(Lost) |
| Executed skill bodies | 토큰 한도 내에서 재주입(Re-injected) |
| Hooks | 코드로 실행되므로 컨텍스트와 무관하게 작동 |

### Subagent Memory 설정 및 스코프 [09:42]
Subagent(서브 에이전트)도 자신만의 메모리를 가질 수 있어 도메인 지식을 축적하기에 용이하다. 에이전트 정의 파일에 `memory` 필드를 추가하여 활성화한다.

**에이전트 정의 예시:**
```yaml
name: code-reviewer
description: Code quality review
memory: project
---
You are a code reviewer. Update agent memory with patterns and recurring issues.
```

**메모리 스코프(Scopes):**
- **user**: `~/.claude/agent-memory/<agent>/` (모든 프로젝트 공통 지식)
- **project**: `.claude/agent-memory/<agent>/` (Git을 통해 팀과 공유 가능)
- **local**: `.claude/agent-memory-local/<agent>/` (프로젝트 전용이나 Git 제외)

Subagent의 메모리가 활성화되면 시스템 프롬프트에 메모리 관리 지침이 자동 포함되며, `read`, `write`, `edit` 도구가 활성화된다. `MEMORY.md` 200줄/25KB 제한 규칙은 동일하게 적용된다.

---

## 주의사항

- **보안 및 개인정보**: Auto memory는 일반 Markdown 파일이므로 로컬 DB 자격 증명이나 API 키와 같은 민감한 정보가 실수로 저장될 수 있다. 정기적으로 `/memory` 명령을 통해 폴더를 열어 내용을 점검해야 한다.
- **공유 한계**: Auto memory는 머신 로컬 기반이므로 `git push`를 통해 팀원과 공유할 수 없다. 팀 전체가 공유해야 할 빌드 명령이나 규칙은 반드시 `CLAUDE.md`에 작성하거나 Subagent의 `project` 스코프 메모리를 활용해야 한다.
- **지식 충돌**: `CLAUDE.md`와 Auto memory 사이에 충돌하는 지시가 있을 경우 Claude가 임의로 선택할 수 있다. 정기적으로 두 메모리를 검토하여 일관성을 유지해야 한다.
- **설정 거부**: 프로젝트 루트의 `.claude/settings.json`에 `autoMemoryDirectory`를 설정하면 보안 정책상 무시된다. 반드시 사용자 홈 디렉토리의 설정이나 `settings.local.json`을 사용해야 한다.
- **Auto memory 미작동 시 점검 순서**:
  1. `/memory` 명령어에서 토글이 `on`인지 확인한다.
  2. 환경 변수 `CLAUDE_CODE_DISABLE_AUTO_MEMORY`가 `1`로 설정되어 있는지 확인한다.
  3. `settings.json`의 `autoMemoryEnabled`가 `false`인지 확인한다.
  4. 해당 메모리 폴더에 쓰기 권한이 있는지 확인한다.