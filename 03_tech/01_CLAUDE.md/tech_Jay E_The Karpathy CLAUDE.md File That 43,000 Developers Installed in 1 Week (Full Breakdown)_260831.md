# Jay E | 43,000명의 개발자가 일주일 만에 설치한 Karpathy의 CLAUDE.md 파일 분석

## Metadata
- **채널:** Jay E
- **URL:** https://youtu.be/d8BGxfW3Vj4
- **Duration:** 11:14
- **Upload Date:** 2026-04-16
- **목적:** CLAUDE.md 작성
- **변환일:** 2026-08-31

---

## 핵심 요약
- `CLAUDE.md`는 AI Agent의 고질적인 문제인 잘못된 가정, 코드 비대화, 불필요한 수정, 명령 위주의 실행을 해결하는 핵심 가이드라인 파일이다.
- Andrej Karpathy의 관찰을 바탕으로 한 4가지 원칙(Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution)을 적용하여 Agent의 성능을 극대화한다.
- 이 가이드를 적용하면 Agent가 코드를 작성하기 전 질문을 통해 의도를 명확히 하고, 최소한의 코드로 정확한 변경 사항만 반영하게 된다.

---

## 적용 지식

### Karpathy Skills와 CLAUDE.md의 개요 [00:39]

Tesla의 AI 책임자이자 OpenAI 창립 멤버인 Andrej Karpathy는 AI Agent가 흔히 저지르는 실수들을 분석하여 공유했습니다. 개발자 Forrest는 이 관찰 결과를 바탕으로 `Claude Code`의 행동을 개선하기 위한 단일 설정 파일인 `CLAUDE.md`를 제작했습니다. 이 파일은 공개된 지 일주일 만에 GitHub에서 43,000개 이상의 Star를 기록하며 폭발적인 인기를 얻었습니다. `CLAUDE.md`는 Agent가 프로젝트의 규칙, 빌드 명령, 테스트 방법 등을 이해하도록 돕는 컨텍스트(context) 역할을 수행하며, 특히 Karpathy가 강조한 4가지 핵심 원칙을 Agent의 행동 양식에 주입합니다.

### 설치 및 통합 방법 [01:11]

`Claude Code`를 처음 사용하는 경우 GitHub 저장소의 원본 파일을 직접 참조하도록 명령할 수 있습니다. 하지만 이미 기존의 `CLAUDE.md` 파일을 사용 중이라면, 기존 내용을 덮어쓰지 않고 새로운 원칙들을 병합(merge)하는 방식이 권장됩니다. 다음은 Agent에게 가이드라인을 설치하고 최적의 통합 방안을 제안하도록 요청하는 프롬프트 예시입니다.

```text
I'm giving you a set of coding guidelines called Karpathy Skills. Get the file from: https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md 
— this is a CLAUDE.md file with four principles (Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution) that improve how you handle coding tasks. 
Do NOT overwrite any existing CLAUDE.md file. If one already exists, merge these four principles into it — add them as a new section without removing or changing anything that's already there. 
If no CLAUDE.md exists, save the file as the project root. After installing, read the file back and confirm which principles are now active. 
Suggest to me how we can best integrate it to our setup.
```

### 원칙 1: 코딩 전 사고 (Think Before Coding) [02:08]

AI Agent의 가장 흔한 실수는 사용자의 의도를 멋대로 가정하고 확인 절차 없이 코드를 작성하는 것입니다. 이 원칙은 Agent가 혼란스러운 부분이 있다면 즉시 질문하고, 결정을 내리기 전에 모든 가정을 명시적으로 밝히게 만듭니다. `C-0310-karpathy-slides.md`에 정의된 이 원칙의 차이는 다음과 같습니다.

| 구분 | 일반적인 Agent (Without) | Karpathy 원칙 적용 (With) |
| :--- | :--- | :--- |
| **결정 방식** | 즉각적으로 해결책 선택 | 가정을 명시적으로 진술 |
| **소통** | 질문이나 명확화 과정 없음 | 불확실할 때 질문함 |
| **투명성** | 가정을 숨기고 임의로 결정 | 결정 전 모든 선택지를 사용자에게 노출 |
| **결과** | 작동은 하지만 의도와 다를 수 있음 | 정확히 설명한 대로 빌드됨 |

실제 테스트에서 `localhost:10001` 포트의 `RUBRIC` Console 앱에 라이트 모드 토글을 추가하라고 요청했을 때, 이 원칙이 적용된 Agent는 `window.THEME` 객체와 `localStorage`(`rubric-theme`) 사용 계획을 먼저 세우고 실행하여 완벽한 결과를 도출했습니다.

### 원칙 2: 단순성 우선 (Simplicity First) [04:58]

Agent는 기본적으로 방대한 프로덕션 코드 베이스로 학습되었기 때문에, 간단한 기능 추가에도 불필요하게 복잡하고 비대한 코드를 작성하는 경향이 있습니다. 이 원칙은 문제 해결을 위한 최소한의 코드만 작성하도록 강제합니다.

- **문제:** Agent가 7줄이면 충분한 필터 기능을 위해 외부 라이브러리를 임포트하거나 `Debounce` 유틸리티를 만드는 등 147줄의 코드를 작성함.
- **해결:** "시니어 엔지니어가 보기에 과하게 복잡한가?"라는 테스트를 스스로 수행하게 하여 코드를 간결하게 유지함.
- **사례:** `RUBRIC` 앱의 탭 리스트 필터링 기능을 구현할 때, 원칙이 적용된 Agent는 복잡한 로직 없이 `nav-filter` 클래스의 `input`과 간단한 `JS` 리스너만 사용하여 20줄 내외로 구현을 마쳤습니다.

### 원칙 3: 정밀한 변경 (Surgical Changes) [06:18]

Agent는 요청받지 않은 부분의 주석을 삭제하거나 코드 스타일을 임의로 변경하는 등 '생산성을 위한 생산성' 활동을 벌여 토큰(token)을 낭비하곤 합니다. `Surgical Changes` 원칙은 오직 요청받은 라인만 수정하도록 제한합니다.

- **Orthogonal edits 방지:** 작업과 직접적인 관련이 없는 코드 구조 재편성이나 포맷팅 수정을 금지합니다.
- **효율성:** 폰트를 `Outfit`에서 `Inter`로 변경할 때, 원칙이 적용된 Agent는 `replace_all`을 사용하여 필요한 부분만 정확히 교체했습니다. 반면 일반 Agent는 변경 사항이 제대로 반영되지 않아 오류를 수정하느라 불필요한 토큰을 계속 소모하는 모습을 보였습니다.

### 원칙 4: 목표 중심 실행 (Goal-Driven Execution) [08:51]

이 원칙은 Agent에게 "어떻게(How)" 할지 일일이 명령하는 명령형(Imperative) 방식에서 벗어나, "무엇(What)"이 완료된 상태인지 정의하는 선언형(Declarative) 방식으로 전환하는 것을 의미합니다.

- **성공 기준 정의:** Agent는 특정 목표를 달성할 때까지 루프를 도는 능력이 탁월하므로, 명확한 `Definition of Done`을 제공하는 것이 효율적입니다.
- **실행 사례:** `Skill Trees` 뷰에서 각 Agent의 아이콘을 선택할 수 있는 기능을 만들 때, 구체적인 UI 디자인을 지시하는 대신 "사용자가 아이콘을 선택할 수 있는 방법을 고안하라"는 목표만 제시했습니다. Agent는 스스로 `data.iconLibrary`에서 그리드를 생성하고 `selectAgentIcon` 함수를 통해 UI를 갱신하며 `api/prefs`에 저장하는 로직까지 스스로 설계하여 구현했습니다.

---

## 주의사항

- **기존 파일 보호:** 설치 시 `Do NOT overwrite any existing CLAUDE.md file` 지침을 명시하지 않으면 기존에 설정된 프로젝트 규칙이 유실될 수 있습니다. 반드시 병합(merge) 명령을 포함해야 합니다. [01:11]
- **토큰 소모 관리:** 원칙이 적용되지 않은 Agent는 오류 수정 과정에서 무의미한 `Bash` 명령(예: `grep`, `curl`)을 반복하며 토큰을 과다하게 소모할 수 있으므로 실행 과정을 모니터링해야 합니다. [07:21]
- **환경 의존성:** 영상의 예시는 `localhost:10000` 및 `10001` 포트에서 실행되는 `RoboLabs`의 `RUBRIC` Console 환경을 기준으로 하며, `Claude Code` Agent가 파일 시스템 및 네트워크 권한(`Bypass permissions`)을 가진 상태에서 수행되었습니다. [03:50]