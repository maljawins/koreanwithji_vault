# Greg Isenberg | Become AI Native in less than 60 mins

## Metadata
- **채널:** Greg Isenberg
- **URL:** https://youtu.be/LztPaNmcWGU
- **Duration:** 56:44
- **Upload Date:** 2026-06-08
- **목적:** AI literacy (AI-native)
- **변환일:** 2026-08-31

---

## 핵심 요약
AI Native 조직은 단순히 AI 도구를 사용하는 것을 넘어, 사람이 Agent를 관리하고 Agent가 기업의 컨텍스트(Context)를 읽고 쓰며 시간이 흐를수록 시스템이 스스로 학습하는 구조를 갖춘 조직이다. 핵심은 명확한 목표(Goal), 기술(Skills), 도구(Tools), 그리고 공유된 컨텍스트(Shared Context)를 결합하여 Agent에게 자율성(Autonomy)을 부여하는 것이며, 이를 통해 제안서 작성이나 프로토타이핑 같은 복잡한 업무를 수 분 내에 완료하고 시장의 신호(Signal)를 즉각 반영하는 선순환 구조를 구축하는 것이다.

---

## 적용 지식

### AI Native 조직의 정의와 구성 요소 [05:53]
AI Native 조직은 단순히 ChatGPT를 사용하는 수준을 넘어선다. 이는 사람(People), Agent, 컨텍스트(Context)가 유기적으로 결합된 시스템이다.
- **People:** 전략, 취향(Taste), 판단력(Judgement), 신뢰를 담당한다. AI가 실행(Execution)의 중간 단계를 처리하므로, 사람은 업무의 시작(기획/전략)과 끝(검토/피드백)에 집중하는 매니저 역할을 수행한다.
- **Agents:** 도구를 루프(Loop) 내에서 사용하는 모델이다. `env = Environment()`, `tools = Tools(env)`, `system_prompt = "Goals, constraints, and how to act"`와 같은 구조로 작동하며, 사람을 대신해 컨텍스트와 상호작용한다.
- **Context:** 기업의 브레인(Company Brain) 역할을 하는 공유 컨텍스트 레이어다. 고객 인텔리전스, SOP, 회의록, KPI 등을 포함하며 Agent가 읽을 수 있는(Agent-readable) 형태여야 한다.

### Agent 자율성(Autonomy)을 위한 4가지 필수 조건 [14:04]
Agent가 사람의 개입 없이 독립적으로 업무를 수행하게 하려면 다음 요소가 반드시 갖춰져야 한다.
1. **명확한 목표(Clear Goal):** 성공의 기준과 측정 방법을 구체적으로 정의한다.
2. **기술(Skills):** 특정 작업을 수행하기 위한 지침 세트다. LCA에서는 이를 Markdown 파일 형태로 관리한다.
3. **도구(Tools):** 작업을 실행하는 데 필요한 환경과 수단이다.
4. **컨텍스트(Context):** 업무 수행에 필요한 배경 지식과 데이터다.

### Skillchains: 복잡한 업무 자동화를 위한 기술 체인 [18:26]
단일 Skill을 넘어 여러 Skill을 순차적으로 실행하는 `Skillchains`를 통해 고도의 결과물을 얻을 수 있다. 예를 들어, 제안서 작성 워크플로우는 다음과 같은 체인으로 구성된다.
- **Skill 1 (Proposal Microsite):** 데이터를 기반으로 웹 형태의 제안서 사이트 구축.
- **Skill 2 (Copy Skill):** 텍스트를 사용자의 톤앤매너에 맞춰 다듬음.
- **Skill 3 (QA Skill):** 제안 내용의 정확성을 검토하고 환각(Hallucination) 여부 확인.

### 재귀적 컨텍스트 레이어(The Recursive Context Layer) 구축 [22:38]
기업의 지식을 Agent가 활용하고 강화하는 5단계 프로세스다.
1. **CAPTURE:** Slack, 이메일, 회의록(Zoom/Meet), Linear 티켓 등에서 데이터를 수집한다. `personal-brain/_demos/spoti`와 같은 경로에 원시 데이터를 모은다.
2. **CURATE:** 수집된 데이터 중 가치 있는 것을 선별하고 정리한다. 불필요한 정보는 무시(Ignore)하고 중요한 정보는 트리거(Trigger)로 설정한다.
3. **STORE:** 정리된 데이터를 `knowledge/`, `frameworks/`, `decisions/` 등의 폴더 구조로 저장하여 Agent가 검색하기 쉽게 만든다. `glossary.md` 등을 통해 용어를 통일한다.
4. **EXECUTE:** 저장된 컨텍스트를 활용해 아티팩트(Artifact)를 생성하거나 프로토타입을 빌드한다.
5. **EXPERIENCE:** 결과물을 고객에게 전달하고 시장의 신호(Signal)를 다시 CAPTURE 단계로 피드백한다.

### 실전 워크플로우: Spotify Daily Blitz 프로토타이핑 [41:15]
LCA 시스템을 사용하여 10분 내에 기능적인 프로토타입을 제작하고 테스트하는 과정이다.
- **목표:** 리텐션 향상을 위한 'Daily Blitz' 기능(매일 3곡의 추천 플레이리스트) 구현.
- **실행:** `lca-labs-2.vercel.app/experiment/spotify-daily-blitz-2026` 경로에 프로토타입 배포.
- **테스트 및 신호 수집:** `lca-labs-2.vercel.app/t/fd5be223-1fde-4638-b567-2dea0e0aebc3`에서 사용자 테스트 수행. 사용자의 피드백(예: "곡 수가 너무 적다")은 즉시 `Synthesize Feedback` Skill을 통해 분석되어 V2 기획에 반영된다.

### 기술 자산 관리 (Skills = Markdown) [19:52]
모든 기술 지침은 Markdown 파일로 관리하며, `app.excalidraw.com/s/8BV4DSDZRXZ/5TJ1ORNzEjH`와 같은 설계도를 기반으로 구조화된다.
```markdown
# spotify-prototype
Build Spotify mobile prototypes. Output ships as three separate files: index.html, styles.css, script.js.

## RULES
1. Never output "Spotify" or the Spotify logo. App name is always "spotify" (lowercase).
2. Read references/kitchen-sink.html for every component.
3. Output three files in Build/vslug/.
4. Use data-screen-id and data-labs-screen-id for tracking.
```

---

## 주의사항
- **환각(Hallucination) 방지:** Agent는 신입 사원처럼 의욕이 앞서 거짓 정보를 만들 수 있다. 이를 방지하기 위해 반드시 QA Skill을 체인에 포함하고, `references/` 폴더의 근거 데이터만 사용하도록 강제해야 한다. [22:59]
- **인간의 개입(Human-in-the-loop):** 자율성이 높아지더라도 최종 판단과 신뢰 구축은 사람의 몫이다. 특히 고위험(High stakes) 작업에서는 `permissions` 설정을 통해 단계별 승인 절차를 거쳐야 한다. [33:57]
- **데이터 오염 방지:** Agent가 생성한 잘못된 결과물이 다시 컨텍스트 저장소(Brain)로 흘러 들어가지 않도록 큐레이션(Curation) 단계에서 엄격한 필터링이 필요하다. [40:00]
- **보안 및 권한:** 모든 데이터를 모든 Agent에게 공개해서는 안 된다. `DANGER ZONE` 설정이나 권한 관리를 통해 민감 정보 접근을 제어해야 한다. [46:29]