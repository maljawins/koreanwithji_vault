# 코스 제작 용어 사전

> **코스 제작 용어의 단일 출처다.** 비전공자가 읽을 수 있게 쓴다.
> 브랜드 용어(Language Core, Translation Trap, Rule of Three, TSV, STLOHV)는 [`_about/01_brand.md`](../../_about/01_brand.md)가 단일 출처다.
> vault 전반 용어와 도메인 용어 요약은 [`AGENTS.md`](../../AGENTS.md) §9에 있다.
> 최종 갱신: 2026-09-15

---

## 1. 산출물

| 용어 | 쉬운 뜻 |
|---|---|
| lesson_spec | 레슨 한 개가 무엇을 가르치는지 정형화해 적은 명세서. 4층 구조(raw / spec / outline / draft)의 층 2 |
| OUTLINE | DRAFT 전에 레슨 뼈대를 잡는 단계 |
| DRAFT | outline에 살을 붙인 영상 설계서(BEAT 묶음). 사람도 읽고 AI도 읽는다 |
| BEAT | 영상의 한 컷. Draft의 최소 조립 단위 |
| CHECK | 학생이 멈춰 회상·예측하게 하는 이해확인 컷 |

## 2. lesson_spec 안의 필드

| 용어 | 쉬운 뜻 |
|---|---|
| GOAL | 이 레슨이 끝나면 학생이 할 수 있게 되는 것. 한 문장 |
| SKELETON | 이 레슨의 뼈대 한 줄 |
| TEACHING_POINTS | 가르칠 항목을 순서대로 편 목록 |
| NEW | 이 레슨에서 처음 가르치는 것 |
| PREREQ | 이 레슨이 딛고 서는, 앞 레슨에서 이미 가르친 것 |
| BUDGET | 그 레슨의 예문에 쓸 수 있는 문법의 상한선. 직전 레슨까지 가르친 NEW의 누적 |
| THROUGH_LINE | 그 레슨을 관통하는 개념 (예: Rule of Three) |
| OUT_OF_SCOPE | 일부러 안 다루는 것과 어느 레슨으로 미루는지 |
| SOURCES | 그 레슨이 근거로 쓰는 raw 파일의 **경로** 목록. 링크가 아니라 경로다 |
| RAW_DIGEST | raw에서 이 레슨 주제에 해당하는 대목만 뽑아 붙인 발췌. 출처를 함께 적는다 |
| OPEN | Ji 결정 대기 항목. 에이전트가 막혔을 때 멈추지 않고 적어두는 자리 |

## 3. 작업

| 용어 | 쉬운 뜻 |
|---|---|
| 조준점 | "이 레슨에서는 이것만 본다"는 한 줄. 발췌할 때 무엇을 뽑을지 정하는 기준 |
| 조준 발췌 | raw 전체를 합치지 않고 조준점에 해당하는 대목만 골라 뽑는 것 |
| status (4단계) | spec 한 장이 자라는 단계. `topic_copy`(V7 복사) → `topic_raw`(발췌 붙임) → `topic_shaped`(대조해 확정) → `spec_done`(필드 다 채움) |
| concept_index | 개념 이름을 하나로 통일해 관리하는 xlsx. 개념마다 표준명·별칭·등장 레슨을 적는다 |
| Ref_No | index xlsx가 자료마다 붙인 번호. 파일 ID가 아니라 **(레슨 × 자료) 짝의 ID**다. 같은 영상도 레슨이 다르면 번호가 다르다. 2026-09-15부터 `01_Ji_Draft_index.xlsx`에도 이 번호가 있다 |
| 트랙 | 레슨 폴더 안의 자료 출처별 하위 폴더 (`01_Ji_draft`, `02_yt_md`, `03_Amira`, `04_HTSK`, `05_Reddit`) |
| batch | 여러 개를 한 번에 묶어 처리 |

## 4. vault와 도구

| 용어 | 쉬운 뜻 |
|---|---|
| Vault | Obsidian이 관리하는 폴더 하나. 그 안의 모든 노트가 한 묶음 |
| Wiki | AI가 원본을 읽고 정리해 쌓는 노트 모음. 사람이 안 쓰고 AI가 씀 |
| 규칙서(AGENTS.md) | Codex에게 "이 창고는 이렇고 자료는 이렇게 처리하라"를 알려주는 설명서 |
| 작업지시서 | 각 STEP의 상세 작업 방법을 담은 별도 파일 |
| Agent (AI 작업자) | 정해진 일을 반복 수행하는 AI |
| 털뭉치 | 문서 간 링크가 너무 많아 Obsidian 그래프가 엉킨 실뭉치처럼 되는 것. 이전 vault의 실패 상태 |

## 5. 관리와 설계

| 용어 | 쉬운 뜻 |
|---|---|
| DP | Decision Point: 결정해야 다음으로 넘어가는 지점 |
| PoC | Proof of Concept: 진짜 되는지 작게 한 번 끝까지 해보는 검증 |
| MOE | Measure of Effectiveness: 잘 되고 있는지 재는 지표 |
| LOE (작업 줄기) | Lines of Effort: 시간 순서가 아니라 분야별로 쭉 이어지는 작업 흐름 |
| Linear Scaffolding | 쉬운 것부터 한 칸씩 쌓아 올리는 학습 설계 |
| VSL | Video Sales Letter. 랜딩 페이지에 넣는 영상. 커리큘럼의 첫 항목 |
