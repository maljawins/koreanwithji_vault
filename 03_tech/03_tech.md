# 03_tech 인덱스

> 이 폴더는 **tech 지식 자체를 모아두는 참고 서가**다. 사업 계획도, 작업 지시서도 아니다.
> Ji가 무언가를 새로 만들 때 에이전트가 여기서 근거와 방법을 꺼내 쓴다.
> **여기에 사업 결정 사항이나 도구 선택 결과를 쓰지 않는다.** 그건 기획서와 각 작업 폴더의 몫이다.
> 최종 갱신: 2026-09-02

---

## 이 폴더를 여는 상황

| 이럴 때 | 여기서 찾는다 |
|---|---|
| CLAUDE.md를 쓰거나 고칠 때 | `01_CLAUDE.md/` |
| 에이전트 메모리 구조를 손볼 때 | `02_claude_memory/` |
| Skill을 만들거나 고칠 때 | `03_claude skills/` |
| Agent나 워크플로우를 설계할 때 | `04_agent_building/` |
| AI를 업무에 어떻게 붙일지 큰 그림이 필요할 때 | `05_ai_native/` |

**여기서 찾으면 안 되는 것**: 우리가 실제로 쓰기로 정한 도구(기획서 v6 §3), 코스 제작 전용 스택([`02_product/02_course_creation/course_tech_stack.md`](../02_product/02_course_creation/course_tech_stack.md)).

**단, vault 관리를 위해 참조할 자료는 `_vault_setup/02_vault_ops` 폴더에서 찾는다.** Obsidian 구조 설계, Claude Code 연동, LLM Wiki 패턴처럼 **이 vault를 굴리는 방법**에 관한 자료는 여기가 아니라 그쪽에 있다. 이 폴더는 일반 tech 지식이고, 그쪽은 vault 운영 지식이다.

---

## 폴더 구조

```
03_tech\
├─ 03_tech.md                ← 이 파일. 폴더 인덱스
├─ 01_CLAUDE.md\             ← CLAUDE.md 작성법 (문서 6개)
├─ 02_claude_memory\         ← Claude Code 메모리 시스템 (문서 1개)
├─ 03_claude skills\         ← Skill 작성법 (문서 3개)
├─ 04_agent_building\        ← Agent와 워크플로우 설계 (문서 2개)
└─ 05_ai_native\             ← AI Native 업무 구조 (문서 1개)
```

---

## 01_CLAUDE.md — CLAUDE.md 작성법

| 문서 | 핵심 |
|---|---|
| `tech_bri_CLAUDE.md Complete Guide` | CLAUDE.md, Skills, Commands, Hooks의 4단계 계층 구조. CLAUDE.md는 200줄 이내 브리핑 문서로 유지하고 상세는 분리. 파일 끝에 "스스로 개선하라" 지침을 넣어 에이전트가 문서를 유지보수하게 만든다. 권장 섹션 6개(Project Identity / Key Commands / Conventions / Hard Stops / Known Gotchas / Links) 예시 포함 |
| `tech_camelCase_Stop Writing Bad CLAUDE.md Files` | 300줄 이하(권장 150~200줄). 모델이 일관되게 따르는 지침은 150~200개가 한계이고 Claude Code 시스템 프롬프트가 이미 50개를 쓴다. `/init` 자동 생성은 장황해서 비권장. 중요한 지침은 맨 위에. Progressive Disclosure로 분리 |
| `tech_Jay E_The Karpathy CLAUDE.md File` | Karpathy 4원칙: Think Before Coding(가정을 밝히고 불확실하면 질문), Simplicity First(최소 코드), Surgical Changes(요청받은 것만 수정), Goal-Driven Execution(How 대신 Done 정의) |
| `tech_GritAI Studio_How to Use CLAUDE.md v1` | CLAUDE.md는 프로젝트 메모리 시스템. `/memory` 명령으로 실시간 갱신해 복리 효과를 낸다. 대규모면 `.claude/rules/`로 모듈화하고 경로별 적용 범위 제한 |
| `tech_GritAI Studio_How to Use CLAUDE.md v2` | v1과 같은 영상의 다른 정리본. 메모리 계층 구조(Managed policy > Project memory > Project rules > User memory > Project local) 설명이 추가돼 있다 |
| `tech_짐코딩_CLAUDE.md 하나로 AI 코딩 품질이 3배` | CLAUDE.md는 시스템 프롬프트가 아니라 사용자 메시지로 전달된다. 그래서 모호한 지시는 무시되고 **검증 가능한 구체적 규칙**만 지켜진다. 200줄 이하 권장. 도메인 용어 정의를 넣으면 품질이 크게 오른다 |

**6개 문서의 공통 결론**: 짧게(200줄), 구체적으로(검증 가능하게), 중요한 것은 위에, 나머지는 별도 파일로 분리.

---

## 02_claude_memory — 메모리 시스템

| 문서 | 핵심 |
|---|---|
| `tech_새로운 시작 E22 메모리 시스템` | 사용자가 쓰는 CLAUDE.md와 Claude가 스스로 기록하는 Auto memory가 병행된다. Auto memory는 로컬에만 저장되고 Git으로 공유되지 않으므로 공통 규칙은 반드시 CLAUDE.md에 쓴다. `/compact`로 압축해도 CLAUDE.md와 Auto memory는 자동 재주입된다 |

---

## 03_claude skills — Skill 작성법

| 문서 | 핵심 |
|---|---|
| `tech_새로운 시작 E25 커스텀 스킬 작성` | SKILL.md가 스킬의 진입점이고 `description` 필드가 에이전트의 사용 판단 트리거다. 본문에는 에이전트가 이미 아는 일반 지식을 빼고 프로젝트 전용 관례와 실행 절차만 쓴다 |
| `tech_새로운 시작 E26 실전 스킬 만들기` | SKILL.md는 빌트인 기능이 모르는 프로젝트 고유 관례와 함정을 정의한다. `context: fork`와 `agent: Explore` 조합으로 메인 컨텍스트 오염을 막고, Plan-validate-execute 패턴과 `assets/` 분리로 안전성과 토큰 효율을 확보한다. PR 리뷰·테스트 생성·문서 생성 예제 포함 |
| `tech_Greg Isenberg_How AI agents & Claude skills work` | CLAUDE.md 같은 전체 컨텍스트 파일은 토큰 낭비가 크므로 워크플로우 단위 Skill로 쪼갠다. Skill은 이름과 설명만 상주하다 필요할 때 전체를 불러오는 progressive disclosure 방식. **처음부터 문서를 쓰지 말고, 에이전트와 대화하며 워크플로우를 성공시킨 뒤 그 과정을 요약해 SKILL.md로 만든다** |

---

## 04_agent_building — Agent와 워크플로우 설계

| 문서 | 핵심 |
|---|---|
| `tech_Greg Isenberg_Building AI Agents that actually work` | Agent는 목표 설정부터 결과 도출까지 스스로 수행하는 시스템이다. 성패는 정교한 프롬프트가 아니라 CLAUDE.md와 MEMORY.md를 활용한 **Context Engineering**에 달렸다. MCP로 외부 도구를 붙이고 반복 업무는 skill로 자산화한다 |
| `tech_Greg Isenberg_Why Graph Engineering will 10x your Claude Codex` | 복잡한 작업을 단일 채팅이 아니라 설계된 워크플로우로 전환한다. 기획자·연구원·회의론자·통합자로 역할을 나누고 병렬 처리와 검증 단계를 넣어 모델의 자기 객관화 부족을 보완한다. 수동 실행(L1) → 파일 기반 기록(L2) → 자동화 오케스트레이션(L3)으로 점진 확장 |

---

## 05_ai_native — AI Native 업무 구조

| 문서 | 핵심 |
|---|---|
| `tech_Greg Isenberg_Become AI Native in less than 60 mins` | AI Native는 도구를 쓰는 수준을 넘어, 사람이 Agent를 관리하고 Agent가 조직의 컨텍스트를 읽고 쓰며 시간이 갈수록 시스템이 스스로 학습하는 구조다. 목표(Goal) + 기술(Skills) + 도구(Tools) + 공유 컨텍스트(Shared Context)를 결합해 자율성을 부여한다 |

---

## 자료 추가 규칙

- 새 tech 자료는 주제별 하위 폴더에 넣고, **이 파일의 해당 표에 한 줄 요약을 추가한다.** 표에 없으면 에이전트는 그 문서의 존재를 모른다.
- 파일명 규칙은 변환 파이프라인이 정한다. [`_vault_setup/01_md_convert/tech_yt_md_guide.md`](../_vault_setup/01_md_convert/tech_yt_md_guide.md) 참조.
- 새 주제가 생기면 하위 폴더를 만들고 위 "이 폴더를 여는 상황" 표에도 행을 추가한다.
