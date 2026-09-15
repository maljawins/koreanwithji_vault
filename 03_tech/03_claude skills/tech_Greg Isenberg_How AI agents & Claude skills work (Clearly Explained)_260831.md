# Greg Isenberg | How AI agents & Claude skills work (Clearly Explained)

## Metadata
- **채널:** Greg Isenberg
- **URL:** https://youtu.be/S_oN3vlzpMw
- **Duration:** 35:25
- **Upload Date:** 2026-04-08
- **목적:** AI Agent 만들기 Claude Skills
- **변환일:** 2026-08-31

---

## 핵심 요약
---
- `agent.md`나 `CLAUDE.md`와 같은 전체 컨텍스트 파일은 토큰 낭비가 심하므로, 특정 워크플로우에만 작동하는 `Skill` 단위로 기능을 분리해야 한다.
- `Skill`은 이름과 설명만 컨텍스트에 상주하다가 필요할 때만 전체 내용을 불러오는 점진적 공개(progressive disclosure) 방식을 사용하여 효율성을 극대화한다.
- 완벽한 `Skill`을 만들려면 처음부터 문서를 작성하지 말고, Agent와 직접 대화하며 워크플로우를 성공시킨 후 그 과정을 요약하여 `skill.md`로 변환해야 한다.

---

## 적용 지식

### AI Agent의 컨텍스트 구성 요소와 효율성 [00:32]
---
AI Agent가 동작할 때 컨텍스트 창(context window)은 여러 요소로 채워진다. 기본적으로 모델 제공자가 설정한 `System Prompt`가 있으며, 사용자가 추가하는 `agent.md` 또는 `CLAUDE.md`, 그리고 특정 기능을 수행하는 `Skills`, 도구 모음인 `Tools`, 전체 `Codebase`, 마지막으로 `User Convo`(사용자 대화 내역)가 포함된다.

많은 사용자가 모든 규칙을 `agent.md`에 넣으려 하지만, 이는 매 대화마다 수천 토큰을 소모하게 만든다. 예를 들어 1,000줄짜리 `agent.md`는 약 7,000 토큰을 매 턴마다 소비한다. 반면 `Skill` 방식을 사용하면 Agent는 `Skill`의 이름과 설명(약 50~100 토큰)만 기억하고 있다가, 실제로 해당 기능이 필요할 때만 전체 내용을 컨텍스트에 로드한다. 이를 통해 컨텍스트 창이 가득 차서 모델이 지능이 떨어지는 현상을 방지하고 비용을 절감할 수 있다.

### 효율적인 Skill 생성을 위한 점진적 워크플로우 [12:12]
---
새로운 `Skill`을 만들 때 가장 큰 실수는 처음부터 완벽한 `skill.md` 파일을 작성하려고 시도하는 것이다. Agent는 실제 성공 사례에 대한 컨텍스트가 없으면 복잡한 지시사항을 잘못 해석할 가능성이 높다. 대신 다음과 같은 단계를 권장한다.

1. **워크플로우 식별:** 자동화가 필요한 반복적인 작업을 정한다.
2. **단계별 직접 교육:** Agent에게 한 단계씩 명령을 내리며 작업을 수행한다. 예를 들어 "스폰서 이메일을 확인해", "그 회사의 Twitter와 YouTube를 조사해", "투자 유치 여부를 확인해"와 같이 구체적으로 지시한다.
3. **피드백 및 수정:** Agent가 실수하거나(예: Trust Pilot 확인 누락) API 호출에 실패하면 즉시 교정한다. "왜 실패했지?"라고 물어 `505 Error`나 `insufficient credits` 같은 구체적인 원인을 파악하게 한 뒤 수정하도록 한다.
4. **성공 사례의 코드화:** 워크플로우가 완벽하게 실행되면, Agent에게 "방금 우리가 수행한 성공적인 과정을 검토하고 이를 `skill.md` 파일로 만들어줘"라고 명령한다.

### Skill 파일의 구조와 토큰 최적화 [29:37]
---
잘 설계된 `Skill`은 Agent가 필요성을 판단할 수 있는 명확한 이름과 설명을 포함해야 한다. 다음은 약 944 토큰 분량의 로직을 `Skill`로 관리할 때의 예시 구조다.

```markdown
# Code Structure Skill
## Description
이 스킬은 여러 워크플로우가 동일한 운영 로직을 중복해서 생성할 때, 이를 서비스 레이어로 추출하고 구조화하기 위해 사용합니다.

## Mental Model
- 새로운 기능인가? -> 먼저 Action에 작성
- 반복되는 작업인가? -> Service로 추출
- 반복되지 않는가? -> Action에 유지

## Architecture Principle
"Actions orchestrate domain rules, while the service layer centralizes reusable operational mechanics with a composable, explicit-input API."

## Implementation Example
```typescript
// adminInvite.ts - orchestration
await sendWelcomeEmail({ to: invitee.email, name: invitee.name });
```
```

이러한 `Skill`은 `GitHub` 저장소 등에 저장하여 관리할 수 있으며, `Michael Shimeles`(`@rasmic`)의 `agent-toolkit`과 같은 프로젝트를 참고하여 `MCP`(Model Context Protocol) 서버용 `Skill`로 변환할 수도 있다.

### Agent 성능 유지를 위한 컨텍스트 관리 [30:52]
---
LLM은 컨텍스트 창이 가득 찰수록(80~90% 이상) 성능이 저하되고 지시사항을 무시하는 경향이 있다. 따라서 `less is more`(적을수록 좋다) 원칙을 지켜야 한다.
- **불필요한 정보 제거:** 모델이 이미 학습 데이터로 알고 있는 일반적인 지식(예: "React를 사용해라", "달러 기호를 사용해라")은 `agent.md`에 넣지 않는다.
- **고유 정보 집중:** 해당 회사만의 고유한 방법론, 특정 워크플로우, 전략적 취향 등 모델이 스스로 알 수 없는 정보만 `Skill`이나 `agent.md`에 포함한다.
- **재귀적 업데이트:** `Skill`을 사용하다가 Agent가 실수하면, 그 실수를 수정한 뒤 다시 `Skill` 파일을 업데이트하게 하여 지속적으로 성능을 개선한다.

---

## 주의사항
- **외부 Skill 다운로드 주의:** `Skills` 마켓플레이스 등에서 검증되지 않은 `Skill`을 다운로드하는 것은 보안 공격 벡터가 될 수 있으므로 주의해야 한다.
- **모델의 한계 인식:** LLM은 실제로 '생각'하는 것이 아니라 토큰을 예측하는 것이므로, 인간의 워크플로우와 취향을 명시적으로 교육하지 않으면 기대한 결과를 얻기 어렵다.
- **Claude Code 및 rate limits:** `Claude Code`와 같은 도구를 사용할 때는 `rate limits`(속도 제한)와 토큰 소모량을 항상 모니터링해야 하며, `ANTHROPIC`의 최신 업데이트(`Reducing Limits on Claude Max Plans` 등)를 확인해야 한다.
- **기술적 환경:** 본 방법론은 `TypeScript`, `Next.js`, `Convex` 등의 현대적인 스택과 `Claude Code`, `Cursor` 등의 Agent 환경에서 가장 효과적이다.