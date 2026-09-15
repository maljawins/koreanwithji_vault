# Greg Isenberg | Why Graph Engineering will 10x your Claude/Codex

## Metadata
- **채널:** Greg Isenberg
- **URL:** https://youtu.be/JWhICz1QR8M
- **Duration:** 26:28
- **Upload Date:** 2026-08-03
- **목적:** Graph Engineering
- **변환일:** 2026-08-31

---

## 핵심 요약
- Graph Engineering은 복잡한 AI 작업을 단일 채팅이 아닌 설계된 워크플로우(Workflow)로 전환하여 품질과 신뢰성을 극대화하는 방법론이다.
- 작업을 기획자(Planner), 연구원(Researcher), 회의론자(Skeptic), 통합자(Merger) 등의 개별 역할로 분리하고 병렬 처리와 검증 단계를 도입함으로써 모델의 자기 객관화 부족 문제를 해결한다.
- 수동 실행(Level 1)에서 시작하여 파일 기반 기록(Level 2), 자동화 오케스트레이션(Level 3)으로 점진적으로 확장하는 것이 권장된다.

---

## 적용 지식

### AI 활용의 세 가지 계층 [01:41]
AI로부터 최상의 결과물을 얻기 위한 접근 방식은 세 가지 계층으로 나뉩니다.
1. **Prompt Engineering**: 단어 선택을 통해 AI에게 더 나은 질문을 하는 방법입니다.
2. **Context Engineering**: AI에게 더 나은 입력 정보와 데이터를 제공하는 방법입니다.
3. **Graph Engineering**: AI를 중심으로 업무 방식 자체를 설계하는 최상위 계층입니다. 단일 채팅창에서 모든 것을 해결하려 하지 않고, 관리되는 워크플로우를 구축하는 것이 핵심입니다.

### Graph Engineering의 핵심 개념과 용어 [03:41]
그래프(Graph)는 화살표로 연결된 작업들의 집합을 의미합니다.
- **Jobs (작업)**: 워크플로우의 각 단계입니다. 하나의 단계는 명확한 소유자(Owner)와 하나의 출력물(Output)을 가집니다.
- **Arrows (화살표)**: 작업 간의 순서와 의존성을 나타냅니다. 무엇이 먼저 실행되어야 하는지를 결정합니다.
- **State (상태)**: 시스템이 지금까지 파악한 정보를 담은 공유 기록입니다.
- **Sequential (순차적)**: 티켓 분류 후 계정 조회와 같이 순서대로 진행되는 방식입니다.
- **Parallel (병렬적)**: 고통 포인트, 경쟁사, 유통 채널 조사를 동시에 진행하는 방식입니다. 다음 단계에서 이전 단계의 결과가 반드시 필요할 때만 대기하도록 설계하여 효율을 높입니다.

### Knowledge Graph와 Agent Graph의 차이 [06:50]
Graph Engineering이라는 용어는 혼용되기도 하지만, 목적에 따라 두 가지로 구분됩니다.
- **Knowledge Graph**: 정보가 어떻게 연결되는지(How information connects)를 다룹니다. 고객, 회사, 제품 간의 복잡한 관계를 AI가 추론할 수 있게 돕습니다. 단순한 RAG(Retrieval-Augmented Generation)가 유사한 텍스트 덩어리만 가져오는 한계를 극복하게 해줍니다.
- **Agent Graph**: 업무가 어떻게 이동해야 하는지(How work should move)를 다룹니다. 기획자가 연구원에게 업무를 전달하고, 회의론자가 검증하며, 인간이 최종 승인하는 업무 흐름을 설계합니다. 본 영상은 주로 이 **Agent Graph**에 집중합니다.

### 그래프 적용 여부 판단 기준 (The Qualifying Test) [08:57]
모든 작업에 그래프가 필요한 것은 아닙니다. 다음 6가지 조건 중 해당 사항이 없다면 단순한 프롬프트 작성이 더 효율적입니다.
1. **Multiple Steps**: 작업이 한 번에 끝나지 않는 경우.
2. **Multiple Sources**: 증거 자료가 여러 곳에서 오는 경우.
3. **Parallel Paths**: 서로 기다릴 필요 없는 독립적인 단계들이 있는 경우.
4. **Checks**: 결과물에 대한 등급 매기기나 검증이 필요한 경우.
5. **Risk**: 잘못된 답변이 금전적 손실이나 신뢰 하락을 초래하는 경우.
6. **Approvals**: 인간의 최종 서명이 필요한 경우.

### 실전 사례: 스타트업 아이디어 검증 워크플로우 [10:16]
"Shopify 판매자를 위한 AI 회계 제품을 출시해야 할까?"라는 질문을 그래프 방식으로 처리하는 과정입니다.

1. **PLAN (기획)**: 질문을 연구 레인(Lane)으로 분할합니다.
2. **RESEARCH IN PARALLEL (병렬 연구)**:
   - **Customer Pain**: 판매자들이 현재 장부를 어떻게 관리하는지 조사.
   - **Competitors**: 누가 이미 판매 중이며 가격은 얼마인지 조사.
   - **Distribution**: 실제로 판매자에게 도달할 수 있는 경로 조사.
3. **SKEPTIC (회의론자)**: 증거를 공격합니다. 근거가 약한 주장은 생존시키지 않습니다. 답변을 쓴 모델이 스스로 채점하게 하지 않고 검증을 별도의 작업으로 분리하는 것이 핵심입니다.
4. **MERGE (통합)**: 살아남은 증거들을 한 페이지 분량의 권장안으로 만듭니다.
5. **HUMAN GATE (인간 게이트)**: 모델이 아닌 인간이 다음 행동(고객 인터뷰, 경쟁사 분석, 혹은 포기 등)을 결정합니다.

### 구현의 3단계 로드맵 (The On-Ramp) [15:16]
처음부터 복잡한 도구를 사용하기보다 단계별로 확장해야 합니다.

- **Level 1: Manual Lanes (No Code)**
  - 각 레인을 별도의 채팅창이나 문서로 실행합니다.
  - `Excalidraw`나 `tldraw`로 그래프를 먼저 그려봅니다.
  - 인간이 직접 상태(State)를 관리합니다.
- **Level 2: File Trails (Light Code)**
  - `Claude Code`, `Codex` 또는 Git 저장소(Repo)를 활용합니다.
  - 모든 단계가 각자의 파일(예: `plan.md`, `customer.md`, `review.md`)을 작성하게 합니다.
  - 비교와 재사용이 가능한 종이 기록(Paper trail)을 남깁니다.
- **Level 3: Orchestrated (Real Tooling)**
  - `LangGraph`: 상태 체크포인트, 지속성, Human-in-the-loop 승인이 필요할 때 사용합니다.
  - `AutoGen GraphFlow`: 조건부 분기 및 루프가 있는 워크플로우에 적합합니다.
  - `n8n`, `Make.com`: Slack, Email, Airtable 등 외부 비즈니스 시스템 연동 시 사용합니다.

### 즉시 적용 가능한 3가지 그래프 패턴 [17:38]

```markdown
1. SUPPORT (고객 지원)
   Classify (분류) -> Account context (계정 맥락 확인) -> Docs + policy (문서/정책 검색) 
   -> Draft reply (답변 초안) -> Checker (정확성, 톤, 리스크 검증) 
   -> Human (환불, 화난 고객 등 최종 승인)

2. CONTENT (콘텐츠 제작)
   Research (조사) -> Thesis (주제 설정) -> Examples (사례 발굴) -> Hook (후킹 문구) 
   -> Script (스크립트) -> Checker (구체성, 페이싱 검증) 
   -> Titles, thumbnails, captions (제목, 썸네일, 캡션 생성)

3. CODE (코딩)
   Plan (설계) -> Edit (코드 수정) -> Review the diff (차이점 리뷰) -> Run tests (테스트 실행) 
   -> Check the UI (UI 확인) -> Hunt edge cases (예외 케이스 탐색) 
   -> Human approves the PR (최종 PR 승인)
```

---

## 주의사항
- **에이전트 수의 함정**: 에이전트(Agent)가 많다고 무조건 결과가 좋아지는 것은 아닙니다. 오히려 노이즈가 늘어나거나, 5명의 AI 작업자가 똑같이 틀린 생각을 반복할 수 있습니다. 목표는 품질을 개선하는 '가장 작은 규모'의 그래프를 만드는 것입니다. [21:00]
- **가짜 대기(Fake Waiting) 제거**: 병렬로 처리할 수 있는 작업을 순차적으로 배치하여 속도를 늦추지 않도록 설계해야 합니다. [21:30]
- **검증자와 작성자의 분리**: 답변을 작성한 동일한 모델에게 검증을 맡기는 것은 "자신이 쓴 성과 보고서를 스스로 채점하게 하는 것"과 같습니다. 반드시 검증 단계를 독립적인 작업으로 분리하십시오. [11:50]
- **인간 게이트의 필수성**: 비용이 많이 들거나 생산 데이터에 영향을 주는 결정(환불, 코드 배포, 공개 포스팅 등)에는 반드시 엄격한 인간 승인 단계를 포함해야 합니다. [23:30]