# lesson_spec_tracking 사용 설명서

> `lesson_spec_tracking.xlsx`의 역할과 status 기록법이다. 작업 기준은 [[course_plan]], 실행 순서는 [[lesson_spec_pilot_instruction]], 용어는 [[glossary]]를 따른다.
> 최종 갱신: 2026-09-27

## 역할과 정본

tracking workbook은 레슨별 자료 매핑, 진행 상태, 검토 결과, 예외 처리 이력을 연결하는 관제표다. raw 본문이나 발췌 구간을 이곳에 복사하지 않는다.

| 정보 | 정본 |
|---|---|
| 레벨·레슨 번호·제목 | [[00_curriculum_and_index]]의 `Korean Course Curriculum Map_Final_V7.xlsx` |
| 파일별 Ref_No·raw 경로 | [[00_curriculum_and_index]]의 5종 index와 Hangul `06_ext_sources_index.xlsx` |
| 중복 매핑 묶음 ID·연결 레슨·Ref_No | `01_range_set/duplicate_material_selection.xlsx` |
| 레슨별 설명 경계와 Ji 검토 | `01_range_set/<레벨>/<레슨>/<레슨 ID>_range_set_review.md` |
| Ref_No별 최종 사용 판정과 원문 구간 | `01_range_set/range_set_source_spans.xlsx` |
| 제작 status·작업 이력 | `lesson_spec_tracking.xlsx` |
| 원문 발췌·lesson_spec·OUTLINE·DRAFT | 각 단계의 산출물 파일 |

concept index와 Structured Output JSON은 `range_set`이나 `topic_raw`의 선행 조건이 아니다.

## status

| 순서 | status | 기록 조건 |
|---|---|---|
| 1 | `raw_mapped` | Ref_No, 레슨, raw 경로가 index와 일치 |
| 2 | `range_set` | 카드의 Ji 설명 경계 검토와 XLSX의 모든 Ref_No 최종 판정·원문 구간 대조, 진행을 막는 판단 완료 |
| 3 | `topic_raw` | 확정 구간의 원문·Ref_No·경로·줄 번호를 발췌하고 문자 대조 완료 |
| 4 | `topic_shaped` | 발췌를 비교해 영상의 설명 범위·순서 구성 |
| 5 | `lesson_spec` | 필수 필드, 출처, 범위, 예문 BUDGET 검증 완료 |
| 6 | `outline` | lesson_spec을 바탕으로 OUTLINE을 만들고 Ji 검수 완료 |
| 7 | `draft` | 승인 OUTLINE을 바탕으로 DRAFT를 만들고 검증 완료 |

status는 순서대로 올린다. 현재 파일럿 44개 카드와 538개 Ref_No XLSX는 제안 초안이다. XLSX의 `사용 후보 / 제외 후보 / 보류`를 확정 판정으로 보지 않는다. 카드 생성이나 중복자료 표의 과거 상태만으로 `range_set`으로 올리지 않는다. `검토 상태`와 `발췌 대상`은 레슨 status와 별개다.

## 시트별 사용

| 시트 | 한 행 | 역할 |
|---|---|---|
| `레슨진행` | 레슨 1개 | 공식 status, 자료 수, 산출물 경로, 다음 조치 |
| `파일관리` | raw 파일 1개 | Ref_No·상대경로, 검토 상태, 발췌 포함·제외 판단 |
| `외부자료` | Hangul 외부자료 복사본 1개 | 해당 index의 4개 Ref_No를 별도 관리 |
| `작업이력` | 변경 사건 1개 | status 변경, 중복자료 판단, 예외 처리 근거 |
| `이전_초안` | 과거 구조 | 참고 전용 |

`검토 상태`는 `미검토 / 진행 중 / 확인 대기 / 완료 / 보류 / 제외`, `발췌 대상`은 `미정 / 포함 / 제외 / 보류`를 쓴다. workbook의 산출물 경로 열은 `topic_raw`, `topic_shaped`, `lesson_spec`만 있다. `range_set`은 정해진 레슨 폴더에서 파일 존재를 확인하고, OUTLINE·DRAFT 경로는 `작업이력`에 남긴다. 없는 열을 있다고 가정하지 않는다.

## 갱신 순서와 검증

1. `레슨진행`에서 레슨을 고르고 `파일관리`·`외부자료`에서 모든 매핑 Ref_No를 확인한다.
2. 중복 자료는 후보 표와 원문을 대조하고, 단독 매핑 자료도 레슨 주제에 맞는 구간을 확인한다.
3. 레슨별 카드에서 설명 경계를 Ji와 확정하고, XLSX에서 모든 Ref_No를 `사용 / 사용 안 함`으로 확정한다. 사용 구간을 원문과 대조하고 출처 충돌·자료 부족을 해결한다.
4. `topic_raw`부터 DRAFT까지 각 단계의 완료 조건을 통과할 때 status, 작업일자, 산출물 경로와 이력을 갱신한다.

`레슨진행`의 자료 수는 실제 `파일관리`·`외부자료` 행 수와 일치해야 한다. `range_set` 이상에는 대응하는 범위 파일이, `topic_raw` 이상에는 대응 산출물이 있어야 한다. raw는 읽기 전용이다.
