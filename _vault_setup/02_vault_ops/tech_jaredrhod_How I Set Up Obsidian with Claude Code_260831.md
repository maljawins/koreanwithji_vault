# jaredrhod | How I Set Up Obsidian with Claude Code

## Metadata
- **채널:** jaredrhod
- **URL:** https://youtu.be/lTd3DwajYks
- **Duration:** 16:45
- **Upload Date:** 2026-07-23
- **목적:** Vault 세팅
- **변환일:** 2026-08-31

---

## 핵심 요약
Obsidian Vault를 AI Agent의 외부 메모리로 활용하여 컨텍스트 창(context window)의 한계를 극복하고 지능을 극대화한다. 모든 폴더와 노트 상단에 요약된 Index를 배치하는 구조를 통해 Agent가 필요한 정보만 선택적으로 로드하는 'Memory on Demand' 시스템을 구축한다. `CLAUDE.md`와 `MEMORY.md` 설정을 통해 Anthropic의 기본 메모리 시스템을 우회하고 Vault를 유일한 진실의 원천(Source of Truth)으로 정의한다.

---

## 적용 지식

### Obsidian Vault와 AI Agent의 상호작용 [00:09]
Obsidian은 컴퓨터에 저장된 Markdown 파일들을 시각적으로 보여주는 인터페이스이며, Obsidian Vault는 단순히 이러한 파일들이 담긴 폴더다. AI Agent는 이 Vault 내의 모든 Markdown 파일을 읽고, 수정하고, 새로 생성하거나 삭제할 수 있는 전체 제어권을 가진다. 이를 통해 Agent에게 무한한 메모리를 제공할 수 있으며, 시스템을 구현하는 즉시 Agent의 작업 효율이 비약적으로 상승한다.

### Vault 구조 및 폴더 레이아웃 [01:37]
효율적인 메모리 관리를 위해 Vault는 엄격한 구조로 조직되어야 한다. 각 폴더는 명확한 목적을 가지며, 관련 데이터는 반드시 지정된 위치에 저장해야 한다.

- `00Inbox`: 사용자와 Agent 사이의 이양 데스크(two-way handoff desk) 역할을 한다. Agent에게 읽히고 싶은 노트나 Agent가 작업 후 검토를 위해 생성한 결과물을 임시로 보관하는 곳이다.
- `01 Daily Notes`: 공유 세션 로그다. 모든 Agent는 작업 내용을 `## <Agent>:<topic>` 형식으로 기록하여 다른 Agent들이 수행된 작업을 파악할 수 있게 한다.
- `02 Company A (Info Product)` / `03 Company B (Landscape Company)`: 개별 비즈니스 전용 폴더다. 각 비즈니스의 자산, 제품 정보, 운영 매뉴얼이 담긴다.
- `04 Dev`: `web-app` Agent 등을 위한 엔지니어링 메모리다.
- `05 Marketing`: 모든 비즈니스가 공유하는 마케팅 원칙, 카피라이팅 기술, 광고 전략 등이 담긴 중앙 허브다.
- `06 Personal`: 개인적인 프로젝트나 가족 정보가 담기며, 오직 `Assistant` 권한을 가진 Agent만 접근한다.
- `07 Archive`: 삭제 대신 Markdown 파일을 보관하는 장소다.

### 효율적인 검색을 위한 인덱싱 시스템 [04:15]
Agent가 수많은 노트를 일일이 읽어 토큰(token)을 낭비하는 것을 방지하기 위해 모든 노트와 폴더에 Index를 생성한다.

Daily Note의 경우, 노트 최상단에 해당 날짜에 수행된 작업을 한두 문장으로 요약한 불릿 리스트 형태의 Index를 작성한다. Agent는 `grep` 명령어나 키워드 검색을 통해 이 Index만 먼저 훑어본 뒤, 필요한 정보가 있다고 판단될 때만 전체 내용을 읽는다.

폴더의 경우, 폴더명과 동일한 이름의 노트를 해당 폴더 내에 생성하여 인덱스 노트로 사용한다(예: `Jobs/Jobs.md`). 이 `same-named` 인덱스 노트는 해당 폴더의 용도와 포함된 파일들의 위치를 Agent에게 안내하는 "문(door)" 역할을 한다.

### AI Priming과 작업(Jobs) 수행 방식 [07:02]
`Operations/Jobs` 폴더에는 Agent가 수행할 특정 작업에 대한 단계별 지침이 포함된다. 예를 들어 `Drafting Emails` 작업의 경우, 단순히 이메일을 쓰라고 명령하는 대신 다음과 같은 순서로 관련 노트를 먼저 읽도록 유도한다.

1. `marketing-email` 전략 노트 읽기
2. `marketing-copywriting` 기술 노트 읽기
3. `customer-questions` (고객의 실제 질문 모음) 분석
4. `Customer Avatar` 정보 확인

이러한 과정을 AI Priming이라고 하며, Agent가 작업의 맥락(context)을 충분히 학습한 뒤 결과물을 내놓게 하여 출력 품질을 100배 이상 향상시킨다. 특히 `customer-questions` 노트에는 고객이 사용하는 정확한 단어를 기록하여 카피라이팅의 설득력을 높인다.

### Vault Index와 마스터 맵 [10:55]
Vault의 루트 디렉토리에는 유일하게 폴더에 속하지 않은 `Vault Index.md` 파일이 존재한다. 이는 전체 Vault의 마스터 맵이다. Agent가 부팅될 때 가장 먼저 읽는 유일한 파일로, Vault의 전체 구조와 각 폴더의 위치 및 용도를 한두 문장으로 설명한다. Agent는 이 맵을 통해 필요한 정보가 어디에 있는지 파악하고, 실제로 필요할 때만 해당 경로로 이동하여 데이터를 로드하는 'Memory on Demand' 방식을 구현한다.

### Claude Code 설정 및 메모리 우회 [13:02]
`jarvis-demo`와 같은 프로젝트 폴더 내의 `CLAUDE.md` 파일은 Agent의 페르소나, 규칙, 그리고 부팅 시 `Vault Index.md`를 읽으라는 명령을 담고 있다. 또한 Anthropic의 기본 `auto-memory` 시스템인 `MEMORY.md`를 우회하여 Obsidian Vault를 유일한 저장소로 사용하도록 설정한다.

`~/.claude/projects/` 경로 내의 해당 프로젝트 폴더에 위치한 `MEMORY.md` 파일의 내용을 다음과 같은 포인터 구조로 교체한다.

```markdown
<!-- Starter template for the AI Memory Vault tutorial. -->
Replacing this file's contents with the pointer below makes Claude Code's native
memory redirect into your vault, so you never end up with two memory layers that
drift apart. Migrate anything already in it into your vault FIRST, then paste this.

There is no separate memory layer here. The single source of truth is the Obsidian
vault, located at:

[FILL IN: your vault's full path - e.g. /Users/you/Documents/Brain on Mac]

Read the vault from there at the start of every session. Sources of truth, in load order:
1. CLAUDE.md (in the working folder) - boot config: startup sequence + the rules that can't lapse.
2. VAULT-INDEX.md (at the vault root) - profile, full rules, the system map.

Everything else lives in its contextual home in the vault.
To remember something, write it to its place in the vault, never here.
```

---

## 주의사항

- **폴더 및 파일 명명 규칙:** 모든 폴더에는 폴더명과 정확히 일치하는 이름의 인덱스 노트가 있어야 한다. Agent는 이 `same-named` 노드를 해당 폴더의 진입점으로 인식한다.
- **메모리 파편화 방지:** `MEMORY.md`를 포인터로 교체하기 전에 기존에 저장된 메모리가 있다면 반드시 Vault로 먼저 이관(Migrate)해야 정보 유실을 막을 수 있다.
- **Agent의 행동 규칙:** 모든 Agent는 작업을 시작하기 전 관련 노트를 먼저 읽어야 하며, 절대 기억에 의존하여 추측해서는 안 된다. 모든 세션 로그는 `01 Daily Notes`에 기록해야 한다.
- **경로 설정:** `MEMORY.md` 내의 Vault 경로는 사용자의 운영체제에 맞는 절대 경로(예: macOS의 경우 `/Users/jaredrhodenizer/Documents/vault-demo`)로 정확히 기입해야 한다.
- **파일 형식:** 모든 지식은 `.md` 확장자를 가진 Markdown 파일로 관리되어야 하며, `.ma`와 같은 오타가 발생하지 않도록 주의한다.
- **시간 기록:** Daily Note의 각 엔트리는 `10:05 AM EDT` 또는 `4:30 PM EDT`와 같이 정확한 시간과 타임존을 포함하여 기록한다.
- **작업 시간 준수:** `9am`부터 시작되는 `deep-work` 블록과 같은 일정 관리는 `Schedule and Routine` 노트를 통해 Agent가 인지하도록 세팅해야 한다.