# master_index.md
## 역할(한 줄): AI가 볼트 시스템을 부팅할 때 전체 구조와 폴더 위치를 한눈에 알아차리게 만드는 '마스터 구조 지도(Blueprint)'
## 위치: 전체 볼트(Vault)의 최상위 루트 

### 구체적인 역할과 기능
 - 필요할 때만 조회하는 온디맨드 메모리 아키텍처 구현 (Memory on Demand & Token Saving)
 - 각 폴더와 하위 파일들의 정체성이 1~2줄의 요약 문장과 불릿 리스트로 정확히 기입.
 - AI는 부팅 시 전체 하위 데이터 수천 개를 한 번에 전부 읽는 과부하를 범하지 않고, 오직 이 지도만 파악하고 있다가 Ji가 특정 지식이나 작업을 요구하는 그 순간에만 표적 폴더\파일을 선택적으로 로딩하여 처리하므로 토큰 낭비를 차단하고 처리 성능 상승
 - master_index에는 vault루트에 위치한 **메인 폴더 - .agents, .codex, .obsidian, .venv, .vscode 등 시스템 폴더 제외** 및 주요 파일만 표시 (.gitignore, .env, cookies.txt, requirements.txt 같은 시스템 파일 제외)
  > 각 폴더 별로 폴더명과 동일한 md파일이 존재한다. 그 파일이 각 폴더별 상세 index이다. 폴더 별 상세 목적은 거기서 확인한다.

---

### 이 지도를 쓰는 법

**master_index는 각 폴더의 index만 가리킨다.** 개별 작업 문서를 여기서 찾지 않는다.

```
1. 이 파일에서 "그 일이 어느 폴더 소관인지" 찾는다
        ↓
2. 그 폴더의 index(폴더명과 같은 .md)를 연다
        ↓
3. index가 가리키는 실제 문서를 연다
```

예: 코스 제작에 필요한 기술 스택을 알고 싶다 → 02_product 소관 → [`02_course_creation.md`](02_product/02_course_creation/02_course_creation.md)를 연다 → 거기서 [`course_tech_stack.md`](02_product/02_course_creation/course_tech_stack.md)를 가리키고 있으니 그걸 연다.

---

### 📁 Koreanwithji_vault 폴더 구조

```
📁 Koreanwithji_vault\
│
├─📁 _about\                        사업과 Ji에 대한 정보. 브랜드 정의와 사업 로드맵
│   └─📄 _about.md                  ← 폴더 index
│
├─📁 _vault_setup\                  vault를 만들고 운영하는 도구와 규칙서. 자료 .md 변환 파이프라인
│   └─📄 _vault_setup.md            ← 폴더 index
│
├─📁 00_daily_worklog\              날짜별 작업 로그. 과거 작업을 추적하는 색인. 본 프로젝트의 MEMORY 그 자체
│   └─📄 00_daily_worklog.md        ← 폴더 index (+ 날짜별 요약 표)
│
├─📁 01_inbox\                      Ji와 에이전트 사이의 완충 지대. 메모리 기록 시스템의 출발점
│   ├─📄 01_inbox.md                ← 폴더 index
│   └─📄 conversation_log\to_do.md  지금 할 일. worklog(과거)의 반대편
│
├─📁 02_product\                    판매할 상품을 실제로 만드는 곳. 현재 상품은 한국어 코스
│   ├─📄 02_product.md              ← 폴더 index
│   ├─📁 01_raw\                    강의 재료가 되는 원본 자료 저장소 (읽기 전용)
│   │   └─📄 01_raw.md              ← 폴더 index
│   └─📁 02_course_creation\        강의 제작 작업장. 절차와 도구, 산출물
│       ├─📄 02_course_creation.md  ← 폴더 index (지도만. 2026-09-04 재작성)
│       └─📄 course_plan.md         강의 제작 로드맵·계획의 유일한 출처 (실시/미실시 사항 포함)
│
├─📁 03_tech\                       tech 지식 자체를 모아두는 참고 서가
│   └─📄 03_tech.md                 ← 폴더 index
│
├─📁 04_marketing\                  유입부터 결제까지의 경로 설계. 추후 마케팅 자료 서가로 확장
│   └─📄 04_marketing.md            ← 폴더 index
│
├─📄 AGENTS.md                      Codex 에이전트 행동 규칙과 라우팅
└─📄 master_index.md                현재 파일. vault 전체 큰 그림 index
```

---

### 어떤 일을 할 때 어디로 가나

| 이런 작업이면 | 여기 index부터 |
|---|---|
| 브랜드 톤과 메시지, ICP, 사업 순서와 우선순위 판단 | [`_about/_about.md`](_about/_about.md) |
| vault 구조 손보기, 자료 .md 변환, 파이프라인 | [`_vault_setup/_vault_setup.md`](_vault_setup/_vault_setup.md) |
| 과거에 무슨 작업을 했는지 추적 | [`00_daily_worklog/00_daily_worklog.md`](00_daily_worklog/00_daily_worklog.md) |
| 대화 기록, 지금 할 일 확인, 새 자료 투입, 결과물 검토 | [`01_inbox/01_inbox.md`](01_inbox/01_inbox.md) |
| 강의 제작, 원본 자료 찾기, 코스 기술 스택 | [`02_product/02_product.md`](02_product/02_product.md) |
| AGENTS.md, Skill, Agent, 메모리 등 tech 학습 | [`03_tech/03_tech.md`](03_tech/03_tech.md) |
| 퍼널, 카피, 가격, 채널 전략 | [`04_marketing/04_marketing.md`](04_marketing/04_marketing.md) |

---

### 규칙

- **각 폴더의 index는 폴더명과 같은 이름의 .md다.** 새 메인 폴더를 만들면 같은 규칙으로 index를 만들고 이 지도에 한 줄 추가한다.
- **index는 지도이지 본문이 아니다.** 실제 내용은 별도 문서에 두고 index는 가리키기만 한다.
- **같은 사실은 한 곳에만 쓴다(Single Source of Truth).** 다른 문서에서는 그곳을 가리킨다.

