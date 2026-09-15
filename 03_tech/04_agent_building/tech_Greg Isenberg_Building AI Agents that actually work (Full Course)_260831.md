# Greg Isenberg | Building AI Agents that actually work (Full Course)

## Metadata
- **채널:** Greg Isenberg
- **URL:** https://youtu.be/eA9Zf2-qYYM
- **Duration:** 58:55
- **Upload Date:** 2026-03-17
- **목적:** AI Agent 만들기
- **변환일:** 2026-08-31

---

## 핵심 요약
- AI Agent는 단순한 질문-답변(Chat)을 넘어 목표 설정부터 결과 도출(Goal to Result)까지 스스로 수행하는 시스템이다.
- 성공적인 Agent 구축의 핵심은 정교한 프롬프트가 아니라, `CLAUDE.md`와 `MEMORY.md`를 활용한 컨텍스트 엔지니어링(Context Engineering)에 있다.
- MCP(Model Context Protocol)를 통해 외부 도구(Gmail, Notion, Stripe 등)를 연결하고, 반복되는 업무 프로세스를 `.skill` 파일로 자산화하여 자동화 효율을 극대화한다.

---

## 적용 지식

### Chat 모델과 AI Agent의 근본적 차이 [01:35]
Chat 모델은 사용자가 질문하면 AI가 답변하고 다시 사용자가 작업을 수행하는 '질문-답변(Question to Answer)' 방식이다. 반면 Agent는 사용자가 목표를 주면 AI가 계획을 세우고 실행하여 결과를 전달하는 '목표-결과(Goal to Result)' 방식으로 작동한다. Agent 내부에는 관찰(Observe), 사고(Think), 행동(Act)의 과정을 반복하는 Agent Loop가 존재한다. 예를 들어 웹사이트 제작 요청을 받으면, Agent는 먼저 대상에 대해 조사(Observe)하고, 제작 계획을 수립(Think)한 뒤, 코드를 작성(Act)하며, 결과물이 목표에 부합할 때까지 이 루프를 반복한다.

### Agent 구동을 위한 4가지 구성 요소와 Harness [08:40]
Agent는 뇌 역할을 하는 LLM(Claude, GPT 등), 중단 없이 작업을 수행하는 Loop, 외부 기능을 수행하는 Tools, 그리고 배경 지식인 Context로 구성된다. 이러한 요소들이 원활하게 작동하도록 돕는 애플리케이션 플랫폼을 Agent Harness라고 부른다. 대표적인 도구로는 `Claude Code`, `Codex`, `Antigravity`, `Manus`, `OpenClaw` 등이 있으며, 사용자는 로컬 폴더를 연결하여 Agent가 해당 디렉토리 내의 파일을 읽고 쓰게 할 수 있다.

### 컨텍스트 엔지니어링: CLAUDE.md 설정 [12:52]
Agent에게는 신입 사원을 온보딩하듯 비즈니스 배경과 선호도를 알려줘야 한다. 이를 위해 프로젝트 루트 폴더에 설정 파일을 생성한다. 도구에 따라 파일명이 다르지만 개념은 동일하다.
- `Claude Code`: `CLAUDE.md`
- `Codex`, `OpenClaw`: `agents.md`
- `Gemini`: `Gemini.md`

이 파일에는 Agent의 역할, 비즈니스 컨텍스트, 작업 선호도, 사용하는 도구 목록 등을 상세히 기술한다. Agent는 매 세션 시작 시 이 파일을 가장 먼저 읽어(Observe step) 사용자의 의도를 정확히 파악한다.

### 지속적인 학습을 위한 MEMORY.md 구축 [34:52]
Agent는 기본적으로 세션 간 기억을 공유하지 않으므로, 사용자의 피드백이나 새로운 선호도를 저장할 `MEMORY.md` 파일이 필요하다. `CLAUDE.md` 상단에 다음과 같은 지침을 추가하여 Agent가 스스로 기억을 관리하게 한다.

```markdown
# CLAUDE.md (또는 agents.md) 상단 추가 예시
- 모든 컨텍스트 파일을 읽으십시오.
- MEMORY.md를 읽어 과거에 학습한 내용을 파악하십시오.
- 사용자가 수정을 요청하거나 새로운 사실을 알려주면 MEMORY.md의 관련 섹션을 업데이트하십시오.
- MEMORY.md를 항상 최신 상태로 유지하고 오래된 정보는 교체하십시오.
```

이를 통해 "이메일 서명에 'Cheers' 대신 'Warm regards'를 사용해줘"와 같은 교정 사항이 다음 세션에도 유지되도록 할 수 있다. `CLAUDE.md`는 성능 유지를 위해 200줄 이내로 관리하는 것이 권장된다.

### MCP를 활용한 도구 연결 및 워크플로우 자동화 [39:07]
MCP(Model Context Protocol)는 LLM과 외부 도구 사이의 번역기 역할을 하여 복잡한 개발 없이도 다양한 앱을 연결한다. `Claude Code`나 `Manus` 등의 설정에서 `Gmail`, `Google Calendar`, `Notion`, `Stripe`, `Granola` 등을 연결할 수 있다.
- **실제 활용 사례:** "오늘 받은 이메일을 요약하고, `Granola`의 미팅 노트를 참조해서 제안서 이메일 초안을 작성해줘. `Stripe` 결제 링크를 포함하고 `Notion`에 프로젝트 페이지도 만들어줘."라고 명령하면 Agent가 모든 도구를 순차적으로 호출하여 작업을 완료한다.

### Skill: AI를 위한 표준 운영 절차(SOP) 자산화 [40:13]
Skill은 특정 작업을 수행하는 정확한 프로세스를 `.skill` 파일로 패키징한 것이다. 한 번 성공한 작업 흐름을 Skill로 만들면 이후에는 동일한 퀄리티의 결과물을 즉시 얻을 수 있다.
- **Skill 생성 방법:**
  1. 직접 작성: 특정 주제(예: Viral Hooks)에 대한 강의 스크립트나 자료를 업로드하고 "이 내용을 바탕으로 `viral-hooks` Skill을 만들어줘"라고 요청한다.
  2. 실행 후 생성: 특정 작업을 수동으로 완료한 뒤 "방금 수행한 과정을 Skill로 저장해줘"라고 명령한다.
- **구조:** `.claude/skills/` 폴더 내에 `SKILL.md`와 필요한 `references` 폴더가 생성된다.

### 실전 사례: Meta Ads 분석 Agent 구축 [48:05]
마케팅 에이전시 업무를 자동화하기 위해 구축된 `content-team` 폴더 구조와 `CONTENT-TEAM` Agent의 설정 예시는 다음과 같다.

```text
# 폴더 구조 예시
ai-with-remy/
└── content-team/
    ├── .claude/
    │   ├── agents/
    │   └── skills/
    │       └── meta-ads-analysis/
    ├── output/
    │   └── meta-ads/
    │       └── the-oodie/
    │           ├── assets/ (스크린샷 저장)
    │           ├── deep-dives/ (개별 광고 분석 리포트)
    │           └── MASTER-REPORT.md (전체 전략 요약)
    └── CLAUDE.md
```

`CLAUDE.md`에는 `Main Claude`가 직접 콘텐츠를 작성하지 않고 `brand-writer`, `content-researcher`, `visual-designer` 등 서브에이전트(subagent)에게 업무를 위임(Delegate)하도록 규칙을 정의한다. `meta-ads-analysis` Skill을 실행하면 Agent는 광고 라이브러리 URL을 탐색하고, `the-oodie-video-61.mp4`와 같은 에셋을 분석하며, `ad-01-pokemon-bulbasaur-blanket.md`와 같은 상세 분석 파일을 생성한다.

### 고급 자동화: 스케줄링 및 OpenClaw [53:50]
`Cowork`나 `Claude Code`에서는 `cron` 작업과 같은 스케줄링 기능을 제공한다. "매일 아침 9시에 `morning-brief` Skill을 실행해줘"라고 설정하면 Agent가 스스로 도구들을 확인하여 하루 일과를 준비한다. 더 높은 자율성이 필요한 경우 `OpenClaw`를 사용하며, 여기에는 Agent의 성격(Soul)과 정체성(Identity)을 정의하는 추가 Markdown 파일이 사용된다.

---

## 주의사항
- **보안 및 권한:** Agent에게 예산 관리나 광고 집행 권한을 줄 때는 도구별 권한(Permissions) 설정을 통해 읽기 전용(Read-only) 접근이나 승인 후 실행 모드를 적절히 활용해야 한다. [08:46]
- **파일 형식:** Agent가 정보를 가장 잘 소화할 수 있는 형식은 Markdown(.md)이다. PDF나 Doc 파일보다 Markdown 형식을 우선적으로 사용하라. [34:52]
- **Skill 관리:** 모든 Skill을 전역(Global)으로 설정하면 컨텍스트가 오염될 수 있다. 특정 프로젝트에만 필요한 Skill(예: 특정 지인 참조)은 프로젝트 레벨 폴더에 두어 관리한다. [53:50]
- **학습 곡선:** `OpenClaw`는 설정 난이도가 가장 높으므로, 입문자는 `Cowork`나 `Claude Code`에서 먼저 프로세스를 구축하고 Skill을 완성한 뒤 마이그레이션하는 것이 권장된다. [53:50]