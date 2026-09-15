# course_creation 전략 재설계 작업 계획

> 작성일: 2026-09-03
> 용도: course_creation 재설계 작업의 실행 계획. STEP 3 이후가 확정되면 내용이 [`02_course_creation.md`](02_course_creation.md)로 흡수되고 이 파일은 삭제 대상이 된다.
> 관련 문서: [`brainstorm.md`](brainstorm.md)(전략 선택지), [`02_course_creation.md`](02_course_creation.md)(절차 단일 출처), [`lesson_design_method.md`](lesson_design_method.md)(교수법 단일 출처)

---

## Context

**왜 고치나.** 이전 vault의 방식은 "raw 자료 전체 → 개념 추출 → 전역 백링크"였다. raw 본문에 `[[concept_x]]`를 직접 삽입했기 때문에 엣지가 만 단위로 늘었고, Obsidian 그래프가 털뭉치가 됐다. 더 큰 문제는 그래프 모양이 아니라 **조준 실패**다. 링크가 아무리 많아도 "2-3 레슨 Draft를 쓰려면 어느 파일을 읽어야 하나"에 답이 안 나온다. 개념이 레슨에 종속되지 않고 소스에 종속됐기 때문이다.

**Ji가 제안한 보완.** 순서를 뒤집는다. 레슨별 주제를 먼저 정형화하고, 그 주제에 raw를 매칭한 다음, 레슨 단위로 개념을 추출한다.

**조사 결과 가장 중요한 발견.** 이 방식에 필요한 재료가 **이미 vault에 있다.**
1. [`Korean Course Curriculum Map_Final_V7.xlsx`](00_curriculum_and_index/Korean%20Course%20Curriculum%20Map_Final_V7.xlsx)의 4번째 컬럼 "Ji 레슨 주제"에 196개 레슨 전부의 teaching point가 Ji 손으로 적혀 있다.
2. `01_by_level_lesson/Level_X/N_레슨명/트랙/` 폴더 구조 자체가 이미 "레슨 ↔ raw" 매칭이다. 링크 없이 경로만으로 조준된다.
3. 레슨 설계 교수법(Skeleton → Flesh → Comprehensible Input → 줌인 반복 → 실생활 예시 + 4MAT)이 이미 [`02_course_creation.md`](02_course_creation.md) 284~382행에 있었다. 위치만 틀렸다.

즉 새로 만들 것은 **재료를 담을 그릇(schema)과 채우는 순서(STEP)**뿐이다.

---

## 산출물 4개

| # | 파일 | 종류 | 내용 |
|---|---|---|---|
| 0 | [`work_plan.md`](work_plan.md) | 신규 | 이 파일 |
| 1 | [`02_course_creation.md`](02_course_creation.md) | 수정 | 죽은 내용 제거 + 신규 STEP 1·2. STEP 3 이후는 자리만 비움 |
| 2 | [`lesson_design_method.md`](lesson_design_method.md) | 신규 | 교수법 블록 이관 |
| 3 | [`brainstorm.md`](brainstorm.md) | 신규 작성 | 전략 선택지 문서. Ji가 읽고 고르면 STEP 1 종료 |

---

## 파일 1. [`02_course_creation.md`](02_course_creation.md) 처리표

**방침**: 확정 안 된 내용을 문서에 박지 않는다. 죽은 내용을 걷어내고 STEP 1과 2만 채운 뒤 STEP 3 이후는 자리만 비운다.

| 기존 위치 | 내용 | 처리 |
|---|---|---|
| 8~30행 | Phase 1 로드맵 | 삭제. `_about/Koreanwithji_기획서_v6_260902.md §2`와 중복 |
| 31~46행 | LLM Wiki 목적 | 축약. Wiki 도구 설명은 `course_tech_stack.md §2`가 단일 출처 |
| 48~92행 | 구 mermaid | 교체 |
| 95~103행 | 목적과 의도 | 유지, 축약 |
| 105~122행 | 현황 분석 | 수치 갱신 (1,416 → 실측, 맵 V6 → V7) |
| 125~139행 | Karpathy 원리 매핑 | 삭제. STEP 매핑표가 무효 |
| 142~158행 | Draft 포맷 (BEAT) | 유지. STEP 2 이관 예고 |
| 162~168행 | 최종 목표 | 갱신 |
| 172~216행 | STEP 1~6 | 전면 교체 |
| 219~227행 | LOE | 갱신 |
| 231~238행 | 결정 사항 | DP-1 유지 + STEP 1 결정 5건 추가 |
| 242~252행 | 리스크 | 갱신 |
| 255~281행 | 용어 사전 | 유지 + 신규 용어 추가 |
| 284~382행 | 교수법 블록 | [`lesson_design_method.md`](lesson_design_method.md)로 이관 |
| 383~386행 | 강의 영상 제작 | 삭제. `course_tech_stack.md §3`과 중복 |

---

## 파일 3. [`brainstorm.md`](brainstorm.md) 구성

- A. 진단: 왜 털뭉치가 됐나 (원인 3가지)
- B. 이미 가진 것 (발견 3가지)
- C. 구조 제안: 3층 (raw / lesson_spec / outline·draft)
- D. lesson_spec 스키마 초안 + Level 2-02 실제 예시
- E. 개념 페이지 정책 3안 비교
- F. 진행 순서 2안 비교
- G. Ji가 STEP 1에서 결정할 것 5개
- H. 열린 질문

---

## 검증 ([`CLAUDE.md`](../../CLAUDE.md) §7)

1. **수치 검증 (실측 완료 2026-09-03, 이후 09-03 재실측으로 갱신됨)**: `01_raw` 전체 .md 1,794개 / `01_by_level_lesson` 1,775개 / 레슨 폴더 196개 / 레벨 16개. 트랙별 `01_Ji_draft` 143, `02_yt_md` 849, `03_Amira` 438, `04_HTSK` 339, `05_Reddit` 4. [`01_raw.md`](../01_raw/01_raw.md)의 표와 전부 일치(당시 기준. 현재 수치는 [`01_raw.md`](../01_raw/01_raw.md) 참조).
2. **경로 검증**: 새 문서에 적은 모든 경로가 실재하는지 확인.
3. **중복 검사**: 지운 내용이 기획서 v6 §2, [`course_tech_stack.md`](course_tech_stack.md) §2·§3, [`01_brand.md`](../../_about/01_brand.md) §10에 실제로 있는지 확인.
4. **참조 갱신**: [`master_index.md`](../../master_index.md)의 "구버전 내용 잔재" 표기, [`02_product.md`](../02_product.md)의 항목 표.
5. **로그**: [`01_inbox/conversation_log/conversation_log.md`](../../01_inbox/conversation_log/conversation_log.md) 기록.

---

## 이번 작업에서 하지 않는 것

- STEP 3~6 본문 작성 (Ji가 brainstorm 읽고 결정한 뒤)
- `lesson_spec_template.md` 등 template 실제 작성 (STEP 2 소관)
- `old_files_to_be_deleted_after_use/` 삭제 ([`02_course_creation.md`](02_course_creation.md) 작업이 완전히 끝난 뒤)
- index xlsx 경로 수정

---

## 미해결 부수 발견 (Ji 확인 필요)

- **(2026-09-03 갱신)** Ji가 직접 3가지를 처리함: (1) `01_Ji_draft` 내 Amira_Source 중복 파일 전체 삭제 (2) 트랙 폴더 밖 orphan 중 `03_Numbers/Youtube Transcript.md` 삭제 (3) index xlsx 5종의 `폴더위치` 컬럼 삭제. 상세는 [`brainstorm.md`](brainstorm.md) §H 참조.
- 트랙 폴더 밖 orphan은 이제 1개만 남음: `01_by_level_lesson/01_Intro/2_How_to_study_vocabulary/자주_쓰이는_한국어_낱말_5800_link.md`. 보고만 하고 손대지 않았다.
- ~~신규 발견: Amira_Source 삭제로 내용물이 0개가 된 `01_Ji_draft` 빈 폴더 12개~~ **해결됨 (2026-09-03).** Ji 확인 후 12개 전부 삭제, 빈 트랙 폴더 0개 확인.
