# 01_lesson_spec 인덱스

> 이 폴더는 lesson_spec 작업장이다. 전체 순서와 규칙은 [[course_plan]]이 단일 출처다.

```text
01_lesson_spec/
├─ 01_range_set/              중복 매핑 목록, 레슨별 범위 검토 카드, Ref_No 구간표
├─ 02_topic_raw/              승인 범위의 원문 발췌 spec
├─ 03_topic_shaped/           설명 범위·순서를 구성한 spec
├─ 04_spec_done/              검증 완료 lesson_spec
├─ 05_outline_and_draft/      OUTLINE·DRAFT와 영상 설계법
├─ lesson_spec_tracking.xlsx  파일·레슨 작업 검토표
├─ lesson_spec_tracking.md    작업 검토표의 목적·칼럼·사용법
├─ lesson_spec_pilot_instruction.md  44개 레슨·538개 raw 파일 실행 지시서
└─ 01_lesson_spec.md          이 파일
```

`topic_copy`는 사용하지 않는다. `_archive/01_topic_copy/`의 보관본은 새 spec의 입력·양식·파일 틀로 쓰지 않는다.

tracking의 목적과 칼럼별 사용법은 [[lesson_spec_tracking]]에서 관리한다.

`raw_mapped`·`range_set`·`topic_raw`·`topic_shaped`·`lesson_spec`·`outline`·`draft`는 tracking에서 쓰는 status다. 모든 산출물 폴더는 [`01_raw/01_by_level_lesson/`](../../01_raw/01_by_level_lesson/)의 레벨·레슨 폴더명과 정확히 같아야 한다.

중복 매핑은 [`duplicate_material_selection.xlsx`](01_range_set/duplicate_material_selection.xlsx)에서 찾는다. 설명 경계는 레슨별 `<레슨 ID>_range_set_review.md`, Ref_No 판정·원문 줄은 [`range_set_source_spans.xlsx`](01_range_set/range_set_source_spans.xlsx)에 둔다. 실행 순서는 [[lesson_spec_pilot_instruction]], status와 검토표 사용법은 [[lesson_spec_tracking]]을 본다. Hangul 외부자료 복사본의 Ref_No는 [`06_ext_sources_index.xlsx`](../00_curriculum_and_index/06_ext_sources_index.xlsx)가 정본이다.
