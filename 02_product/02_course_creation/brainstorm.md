# STEP 1 작업 문서

> **여기는 두 가지만 담는다. STEP 1을 어떻게 실행하는가, 그리고 아직 정하는 중인 것.**
> 이미 확정된 계획(3층 구조, 결정 기록, STEP 정의, 현황 수치)은 [`course_plan.md`](course_plan.md).
> 용어는 [`glossary.md`](glossary.md), 교수법은 [`lesson_design_method.md`](lesson_design_method.md).
> 최종 갱신: 2026-09-07

---

## 지금 Ji가 정할 것

현재 없음. 2026-09-04에 올라온 Q1~Q3은 2026-09-07 Ji가 전부 결정해 반영했다 (§2-2, §5 참조).

---

## 1. 범위: 파일럿 44개 레슨

Hangul 6 + Numbers 7 + Level 1 21 + Level 2 10 = **44개**. 선정 이유는 [`course_plan.md`](course_plan.md) §7.

작업이 한 종류가 아니라 **두 갈래**다. V7 4번 컬럼의 분량이 레슨마다 다르기 때문이다 ([`course_plan.md`](course_plan.md) §3).

| 갈래 | 레슨 | 무엇이 기준인가 |
|---|---|---|
| 두꺼운 쪽 (121자 이상, 전체 43개) | V7에 teaching point가 이미 있다 | **Ji가 쓴 것이 기준.** 발췌는 보강 재료 |
| 얇은 쪽 (30자 이하 + 빈칸, 전체 74개) | V7에 키워드뿐이거나 비어 있다 | **발췌가 기준.** 여기서 사실상 새로 쓴다 |

얇은 쪽이 곧 어려운 쪽은 아니다. Level 12는 raw도 레슨당 1개 4~7KB라 양쪽 다 얇아 빨리 끝난다.

---

## 2. 작업 4단계

각 단계가 spec frontmatter의 `status` 값과 1:1로 대응한다.

### 2-1. V7 복사 (`topic_copy`)

V7 4번 컬럼을 레슨당 spec 1장으로 편다. **스크립트 일괄. 판단이 안 들어가므로 검수 불필요.**

- 슬래시로 뭉친 것을 불릿으로 편다
- 빈칸 레슨은 "raw에서 채워야 함"으로 표시한다. **빈 파일로 두지 않는다**

**이 단계를 왜 먼저 하는가.** 여기서 나오는 게 조준점이다. "2-10은 만/밖에/뿐만 본다"는 한 줄이 있어야 다음 단계에서 raw를 골라 읽을 수 있다. 이건 raw 없이 만들 수 있어서 비용이 0이다.

### 2-2. 조준 발췌 (`topic_raw`)

조준점을 들고 레슨 폴더의 raw를 읽어 **해당 주제 대목만** 뽑아 spec의 `RAW_DIGEST` 섹션에 넣는다.

**raw를 한 장으로 합치지 않는 이유 (DP-7).** 폴더가 이미 취합본이다. 다중 매핑 자료는 레슨 폴더마다 사본이 따로 있다(Miss Vicky `6 Essential Particles`는 7개 폴더에 7개 사본). 합치면 Level 2-02가 588KB 한 장이 되는데, 한국어 md 588KB는 대략 20만 토큰이라 에이전트가 한 번에 못 읽는다. 26개 파일일 때는 골라 읽을 수 있었으니 **합치면 지금보다 나빠진다.**

**Ji가 정확도를 최우선으로 지정했다. 규칙 5개다.**

| 규칙 | 이유 |
|---|---|
| 원문 그대로 인용. 요약 금지 | 요약하면 뉘앙스가 날아간다. 예문은 특히 그렇다 |
| 출처 3종 표기: Ref_No + 파일명 + 섹션 제목 | 어느 자료 어디서 왔는지 되짚을 수 있어야 한다 |
| 발췌문이 원문에 실제로 있는지 문자열 대조 | 에이전트가 지어내는 것을 사람 눈이 아니라 기계로 막는다 |
| 버릴지 애매하면 남긴다 | 원본은 폴더에 그대로 있다. 발췌는 버리는 게 아니라 골라내는 작업이다 |
| `02_yt_md`의 `## Transcript` 섹션(영상 원문 대사)은 가져오지 않는다 | 원본에 이미 있어 필요하면 SOURCES 경로로 되짚을 수 있다. `## Teaching Points`가 이미 구조화된 핵심이다 |

**Ref_No 사용법**

- Ref_No가 무엇인지는 [`glossary.md`](glossary.md) §3. 실무상 중요한 건 **레슨마다 번호가 다르다**는 점이다. 같은 Miss Vicky 영상이 `YT-2-10-3`, `YT-3-11-9`, `YT-4-14-8`로 각각 잡힌다. 다중 매핑 혼선 방지에 정확히 맞는 도구다
- **raw .md 1,727개 안에 Ref_No가 적힌 파일은 0개다.** 에이전트가 index xlsx를 열어 파일명으로 매칭해야 한다
- **`01_Ji_draft` 트랙은 Ref_No를 쓰지 않는다 (DP-10).** Ji가 직접 쓴 자료라 레슨당 1개씩이고 다중 매핑이 아니다. 경로로만 표기한다. 나중에 필요해지면 `Ji-01-01` 형식으로 넘버링할 수 있다

### 2-3. 대조와 확정 (`topic_shaped`)

V7 복사본과 발췌를 대조해 `TEACHING_POINTS`의 **순서와 범위**를 확정한다.

**여기가 Ji의 검수 지점이다.** 두 갈래(§1)에 따라 무엇을 기준으로 삼을지 달라진다.

### 2-4. 개념 indexing (`spec_done`)

`concept_index.xlsx`를 만들고 spec의 나머지 필드를 표준명으로 채운다. 컬럼은 §4-2.

---

## 3. 파일명 규칙 (DP-9 확정)

`레벨-레슨_lesson_spec_레슨제목.md` 형태. 예: `02-02_lesson_spec_The Rule of Three.md`

| 항목 | 규칙 |
|---|---|
| 비숫자 레벨 4개 | 레벨명을 그대로 쓴다. `Hangul-01_...`, `Numbers-01_...`, `Intro-01_...`, `VSL-01_...` |
| 자릿수 | 두 자리로 통일. `02-02`, `10-01`. Level 10~12가 있어 정렬이 깨지는 걸 막는다 |
| 금지 문자 | 폴더가 이미 쓰는 치환 규칙을 따른다. `과/와` → `과_와`. Windows에서 `/ \ : * ? " < >` 와 세로줄을 못 쓴다 |

---

## 4. 진행 중인 스키마

### 4-1. lesson_spec 작성 규칙과 실물 예시

필드 10개의 목록과 `status` 4단계는 [`course_plan.md`](course_plan.md) §5에서 확정했다. 여기는 **어떻게 채우는가**다.

| 필드 | 작성 규칙 |
|---|---|
| `GOAL` | 한 문장. "~를 안다"가 아니라 "~를 할 수 있다"로 쓴다. 이게 없으면 Draft가 어디서 끝날지 모른다 |
| `SKELETON` | 한 줄. [`lesson_design_method.md`](lesson_design_method.md) §1의 뼈대 |
| `TEACHING_POINTS` | 번호 매긴 목록. **순서가 곧 강의 순서다** |
| `NEW` / `PREREQ` / `THROUGH_LINE` | `concept_index.xlsx`의 **표준명만** 쓴다. 임의로 새 이름을 만들지 않는다 |
| `PREREQ` | 레슨 번호를 함께 적는다 (`L1-07 SOV`). 어느 레슨을 딛는지 추적 가능해야 한다 |
| `BUDGET` | 직접 쓰지 않는다. 앞 레슨들의 `NEW` 합산으로 계산한다 |
| `OUT_OF_SCOPE` | 안 다루는 것 + **어느 레슨으로 미루는지**까지 적는다. 레슨 번호가 없으면 그냥 누락이다 |
| `SOURCES` | 우선순위 순. `01_Ji_draft`가 톤 기준, 나머지는 내용 재료 |
| `OPEN` | 막혔을 때 멈추지 말고 여기 적고 넘어간다 |

**실물 예시 (Level 2-02)**

```yaml
---
lesson_id: L2-02
level: 2
lesson_no: 2
title: TSV Sentence Structure #1 - The Rule of Three
status: spec_done
---

## GOAL
"저는 피자가 좋아요"와 "지수는 피자를 좋아해요"를 언제 어느 쪽으로 쓰는지
스스로 판단해서 말할 수 있다.

## SKELETON
한국어는 남의 마음속을 직접 서술하지 못한다. 그래서 문장 구조가 갈라진다.

## TEACHING_POINTS
1. TSV 구조 복습 (이 사람은 제 친구가 아니에요)
2. 이/가 좋다 - 서술 대상이 "피자"인 이유
3. The Rule of Three - 1인칭만 감정 직접 서술 가능
4. 이/가 좋다 vs 을/를 좋아하다 - 언제 갈라지는가
5. 아/어하다 compound verb 도출
6. 아요/어요 평서문도 Rule of Three 적용 대상

## NEW
- Rule of Three
- 이/가 + descriptive verb (좋다)
- 아/어하다 compound verb

## PREREQ
- L2-01 은/는 vs 이/가
- L1-07 SOV, 목적어 을/를, "descriptive verb는 목적어를 못 가진다"
- L1-05 아/어 활용
- L1-11 아니다

## BUDGET
L1-01 ~ L2-01의 NEW 누적 (자동 계산)

## THROUGH_LINE
Rule of Three (코스 전체 관통), TSV (Level 2 관통)

## OUT_OF_SCOPE
- 다른 compound verb 전반 → Level 3 (prerequisite 미충족)
- 번역 안 되는 감정 어휘 (밉다, 억울하다) → L2-03

## SOURCES (우선순위 순)
1. 01_Ji_draft/02-02 TSV Sentence Structure #1 - The rule of three_lesson script.md   [톤 기준, 90% 완성]
2. 02_yt_md/Go Billy_FAQ_좋다 vs 좋아하다.md
3. 02_yt_md/Miss Vicky_영상 전체_좋아요 vs 좋아해요  What's the Difference.md
   (나머지 23개는 참고. 전체 목록은 폴더 참조)

## RAW_DIGEST
(§2-2의 발췌. 출처 3종 표기)

## OPEN
- 6번 항목(아요/어요 평서문)을 이 레슨에 넣을지 L2-08 Context markers로 미룰지
```

### 4-2. concept_index.xlsx 컬럼

| 컬럼 | 용도 |
|---|---|
| `concept_id` | 통일 ID. 이름이 바뀌어도 이건 안 바뀐다 |
| `표준명` | 유일한 정식 이름. spec에는 이것만 쓴다 |
| `별칭` | 소스마다 다르게 부르는 이름들 (예: 은/는 = topic marker = 주제격 조사) |
| `최초레슨` | 이 개념을 `NEW`로 가르치는 레슨. 반드시 1개 |
| `등장레슨` | `NEW`/`PREREQ`에 나오는 레슨 목록 |
| `등장레슨수` | 나중에 개념 페이지가 필요해지면 필터 기준이 된다 |
| `종류` | through_line / 문법 / 어휘 |

**`별칭` 컬럼이 핵심이다.** 196개를 순서대로 작업하면 같은 개념에 다른 이름이 붙는다. 별칭을 한 곳에 모아야 중복이 안 생긴다. 이전 vault에서 개념이 잘게 쪼개진 원인이 정확히 이것이다.

---

## 5. 열린 질문

### 5-1. CLAUDE.md §10에 추가할 gotcha (Q2)

**raw 본문의 `Mapped Ji Lesson` 필드는 구 커리큘럼 번호라 V7과 어긋난다.** Miss Vicky `6 Essential Particles`에 `2-10; 2-21; 2-22; ...`로 적혀 있으나 Level 2는 레슨이 10개뿐이라 2-21, 2-22는 존재하지 않는다. 848개 파일에 이 필드가 있다. **매핑 정본은 index xlsx와 폴더 경로다.**

### 5-2. 나머지

1. **`RAW_DIGEST`를 `spec_done`에서 남길지 (Q1).** 지금은 남기는 쪽으로 잡았다. spec이 너무 길어지면 그때 뗀다
2. **Draft 머리말 필드 이름.** [`02_course_creation.md`](02_course_creation.md)에 있던 `THROUGH_LINE::` / `USE_CONCEPTS::`는 spec과 겹쳐서 2026-09-04에 삭제했다. **개념 이름의 원본은 spec 하나다.** Draft가 쓸 머리말 이름은 Draft를 실제로 만들 때 겹치지 않게 새로 정한다
3. **트랙 폴더 밖에 있는 .md 1개 (Q3).** `01_Intro/2_How_to_study_vocabulary/자주_쓰이는_한국어_낱말_5800_link.md`
