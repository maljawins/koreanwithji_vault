# 새로운 시작 (neosarchizo) | [Claude Code 입문 E15] Agentic Loop 작동 원리: 도구 실행 흐름과 컨텍스트 윈도우 관리

## Metadata
- **채널:** 새로운 시작 (neosarchizo)
- **URL:** https://youtu.be/6fiMMnrbfuY
- **Duration:** 13:09
- **Upload Date:** 2026-04-09
- **목적:** 04_agent_building
- **변환일:** 2026-09-02

---

## 핵심 요약
- Claude Code는 단순한 챗봇이 아니라 Gather Context(문맥 수집), Take Action(행동), Verify Results(결과 검증) 단계를 자율적으로 반복하는 Agentic Loop 메커니즘으로 동작한다.
- 컨텍스트 창(Context Window)의 효율적 관리를 위해 자동 압축(Auto-compaction) 기능을 제공하며, 사용자는 `/compact` 명령어나 Subagent를 활용해 토큰 소모를 최적화할 수 있다.
- 프로젝트의 고유 규칙은 `CLAUDE.md`에 작성하여 세션마다 자동으로 로드되게 하고, 학습된 패턴은 `MEMORY.md`를 통해 세션 간에 유지하여 일관된 작업 환경을 구축한다.

---

## 적용 지식

### Agentic Loop의 개념과 3단계 [00:11]

Claude Code를 단순한 챗봇이 아닌 Agent로 만들어주는 핵심은 자율 실행 사이클인 Agentic Loop이다. 일반적인 AI가 단발성 질문과 답변(Single turn interaction)으로 끝나는 것과 달리, Agentic AI는 요청을 받으면 스스로 생각(Think), 행동(Act), 검증(Verify)하는 과정을 반복하여 최종 응답을 도출한다. 이 루프는 크게 세 단계로 구분된다.

1.  **Gather Context**: 파일을 검색하고 읽어서 코드를 이해하는 단계이다.
2.  **Take Action**: 코드를 수정하거나 셸 명령어를 실행하는 실제 작업 단계이다.
3.  **Verify Results**: 테스트를 실행하거나 빌드 상태를 확인하여 작업 결과를 검증하는 단계이다.

작업의 성격에 따라 루프의 형태는 달라진다. 단순 코드 질문은 Gather Context 위주로 진행되지만, Bug Fix는 세 단계를 모두 여러 번 반복하며, Refactoring 작업은 Verify Results 단계에 더 많은 비중을 둔다.

### 핵심 구성 요소: Model과 Tools [01:54]

Agentic Loop를 가능하게 하는 Claude Code Harness는 Model과 Tools, 그리고 Context Management를 연결한다.
- **Model**: 코드를 이해하고 추론하며, 다음에 어떤 행동을 할지 결정하는 두뇌 역할을 한다.
- **Tools**: 실제로 파일을 읽고 수정하며 명령을 실행하는 손발 역할을 한다. Tools가 없다면 Claude는 텍스트만 생성할 수 있을 뿐, 실제 환경에 변화를 줄 수 없다.

### 도구 카테고리와 승인 프로세스 [02:36]

Claude Code의 내장 도구는 기능에 따라 5가지 카테고리로 분류된다.

| Category | What Claude Can Do | Tools |
| :--- | :--- | :--- |
| **File Ops** | 파일 읽기, 수정, 생성, 이동 | `Read`, `Edit`, `Write` |
| **Search** | 패턴으로 파일 찾기, 내용 검색 | `Glob`, `Grep` |
| **Execution** | 셸 명령, 테스트, Git 실행 | `Bash` |
| **Web** | 웹 검색, 문서 가져오기 | `WebFetch`, `WebSearch` |
| **Code Intel** | 타입 에러 확인, 정의로 이동 | `ide_executeCode`, `ide_getDiagnostics` |

도구는 실행 권한에 따라 두 종류로 나뉜다.
- **Auto-approved (Read-only)**: `Read`, `Glob`, `Grep` 등 읽기 전용 도구는 사용자 개입 없이 자동으로 실행된다.
- **Requires approval (Write/Execute)**: `Edit`, `Write`, `Bash`, `WebFetch`, `WebSearch` 등 시스템에 변경을 가하거나 외부 네트워크를 사용하는 도구는 사용자의 승인(`y`/`n`)이 반드시 필요하다.

### 자율적 도구 선택 및 실행 흐름 [04:21]

Claude는 사용자가 일일이 지시하지 않아도 어떤 도구를 사용할지 스스로 결정한다. 예를 들어 "로그인 버그를 수정해 줘"라는 요청을 받으면 다음과 같은 흐름으로 작동한다.
1.  **탐색**: `Glob`으로 로그인 관련 파일(`Login.tsx`, `auth.ts` 등)을 탐색한다.
2.  **분석**: `Read`로 파일을 읽어 버그 위치(예: `validatePassword` 함수)를 파악한다.
3.  **수정**: `Edit`으로 코드를 고친다 (사용자 승인 필요).
4.  **검증**: `Bash`로 `npm test`를 실행하여 모든 테스트가 통과하는지 확인한다.

만약 빌드 중 `TypeScript type mismatch` 같은 에러가 발생하면, Claude는 자동으로 에러를 분석하고 `Edit` 도구로 타입을 수정한 뒤 다시 빌드를 시도하는 자율 복구 능력을 보여준다. 해결할 수 없는 경우(예: 환경 변수 누락)에만 사용자에게 도움을 요청한다.

### 병렬 도구 실행(Parallel Tool Execution) [05:50]

독립적인 작업은 동시에 처리하여 시간을 절약한다.
- **Sequential (순차 실행)**: 의존성이 있는 경우이다. 파일을 수정(`Edit`)하기 위해서는 반드시 먼저 읽기(`Read`)가 선행되어야 한다.
- **Parallel (병렬 실행)**: 의존성이 없는 경우이다. 여러 컴포넌트 파일(`compA.tsx`, `compB.tsx`, `compC.tsx`)을 동시에 읽는 작업 등이 이에 해당한다.

### 사용자 제어 옵션(Control Options) [06:21]

사용자는 루프가 진행되는 동안 실시간으로 개입하여 방향을 조정할 수 있다.
- **Interrupt**: 작업 중 `Enter`를 눌러 중단하고 새로운 지시를 내릴 수 있다.
- **Redirect**: "그게 아니라 세션 처리 쪽을 확인해 봐"와 같이 대화하듯이 방향을 전환한다.
- **Approve/Deny**: 파일 수정이나 명령 실행 시 `y`(yes) 또는 `n`(no)으로 승인 여부를 결정한다.

### 컨텍스트 창(Context Window) 구성 및 관리 [06:53]

Context Window는 Claude가 한 번에 참조할 수 있는 정보의 총량이다. 세션 시작 시 자동으로 로드되는 항목들은 이미 상당한 토큰을 차지한다.

**자동 로드 항목 (v2.1.96 기준 예시):**
- **System Prompt**: 핵심 지시사항 (~4,200 tokens)
- **MEMORY.md**: 학습된 패턴 (~680 tokens)
- **Environment**: OS, shell, git status 등 환경 정보 (~280 tokens)
- **MCP Tools**: 도구 이름 정보 (~120 tokens)
- **Skills**: 한 줄 기능 설명 (~450 tokens)
- **CLAUDE.md**: 프로젝트 규칙 (~1,800 tokens)

전체 컨텍스트 사용량 중 파일 읽기가 가장 큰 비중을 차지하므로, 프롬프트를 구체적으로 작성하여 Claude가 필요한 파일만 읽도록 유도하는 것이 효율적이다. 현재 컨텍스트 상태는 `/context` 명령어로 확인할 수 있다.

```bash
# 컨텍스트 사용량 확인 예시 (TERMINAL 출력)
/context
Context Usage Opus 4.6
15.9k/200k tokens (8%)
Estimated usage by category
- System prompt: 6.4k tokens (3.2%)
- System tools: 8.7k tokens (4.4%)
- Memory files: 277 tokens (0.1%)
- Skills: 514 tokens (0.3%)
- Messages: 8 tokens (0.0%)
- Free space: 163.1k (81.6%)
- Autocompact buffer: 21k tokens (10.5%)
```

### 압축(Compaction) 및 컨텍스트 최적화 전략 [08:14]

컨텍스트가 한계에 도달하면 Claude Code는 **Auto Compaction**을 수행한다. 오래된 도구 출력(파일 내용, 명령 결과)을 제거하고 이전 대화를 요약한다. 이때 사용자의 요청과 핵심 코드는 보존되지만 초반의 상세 지시사항은 유실될 수 있다.

**최적화 전략:**
1.  **수동 압축**: `/compact` 명령어를 사용한다. 특정 주제를 지정하여 압축할 수도 있다.
    ```bash
    /compact Focus on API changes
    ```
2.  **CLAUDE.md 활용**: 대화 기록에 의존하지 않고 반복되는 규칙은 `CLAUDE.md`에 작성한다. 압축 후에도 유지되므로 안정적이다.
    ```markdown
    ## Compact Instructions
    - Always remember API endpoint changes
    - Keep current branch info
    ```
3.  **Subagent 활용**: 독립적인 컨텍스트 창을 가진 Subagent에게 무거운 작업(예: 20개 파일 분석)을 맡긴다. Subagent는 분석 후 요약본(~500 tokens)만 메인 에이전트에게 반환하여 메인 컨텍스트를 깨끗하게 유지한다.

### 세션 간 지식 유지(Persistence) [12:20]

각 세션은 독립적이며 이전 대화 기록을 공유하지 않는다. 지식을 유지하기 위해 다음 방법을 사용한다.
- **Auto Memory**: Claude가 학습한 패턴이나 선호도를 `MEMORY.md`에 자동으로 저장하고 다음 세션에서 불러온다.
- **CLAUDE.md**: 사용자가 직접 프로젝트 규칙과 컨벤션을 작성하여 매 세션마다 로드되게 한다.
- **세션 재개**: `claude -c` 명령어를 사용하여 이전 세션을 이어서 작업한다.

---

## 주의사항

- **정보 손실**: 자동 압축(Auto Compaction) 과정에서 대화 초반의 상세한 지시사항이 손실될 수 있다. 반드시 유지되어야 하는 프로젝트 규칙은 `CLAUDE.md`에 명시해야 한다.
- **세션 독립성**: 새로운 세션은 이전 세션의 대화 기록을 갖지 않는다. 연속적인 작업이 필요한 경우 반드시 `claude -c` 옵션을 사용해야 한다.
- **승인 대기**: `Edit`, `Bash` 등 쓰기/실행 권한이 필요한 도구는 사용자의 승인이 있을 때까지 루프가 멈추므로 실시간 모니터링이 필요하다.
- **경로 주의**: `CLAUDE.md`는 프로젝트의 루트 디렉토리에 위치해야 Claude Code가 시작 시 자동으로 인식한다. (예: `~/GitProjects/hello-claude/CLAUDE.md`)