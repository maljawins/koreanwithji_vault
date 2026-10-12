# 01_range_set 인덱스

> 이 폴더는 레슨별로 raw에서 사용할 원문 구간을 확정하는 작업장이다. 판단·완료 기준은 [[course_plan]], 파일럿 실행 순서는 [[lesson_spec_pilot_instruction]]에 있다.

| 항목 | 역할 |
|---|---|
| `duplicate_material_selection.xlsx` | 같은 원본이 여러 레슨에 매핑된 묶음 ID·레슨·Ref_No를 찾는 목록. 발췌·제외 내용의 출처로 쓰지 않는다 |
| `<레벨>/<레슨>/<레슨 ID>_range_set_review.md` | 44개 파일럿 카드와 Level 3~12의 1차 후보 카드 149개. 레슨별 설명 경계, 모든 매핑 Ref_No의 원문 링크·XLSX 판정 현황, Ji와 Agent의 확인 사항을 보여 준다 |
| `range_set_source_spans.xlsx` | 1,677개 Ref_No의 사용 판정·후보와 원문 구간을 관리하는 단일 작업표. `파일판정`과 `사용구간` 시트를 쓴다 |
| `range_set_source_spans_pilot.xlsx` | Hangul 2 최초 시범본. 현행 판정에는 사용하지 않고 위 단일 작업표를 따른다 |

레벨·레슨 폴더명은 `02_product/01_raw/01_by_level_lesson/`의 해당 폴더와 같게 쓴다. 원문 본문은 여기로 복사하지 않는다. XLSX가 자료 판정·구간의 정본이고 카드의 자료표는 Ji 검토용 반영본이다. Ji는 표 아래 질문에 답하고 자료별 변경은 Ref_No와 원하는 방향을 `Ji 검토`에 적는다. Agent는 원문 확인 → XLSX 수정 → 카드 재반영 순서로 처리하며 Ji의 기존 답변을 보존한다. 현재 XLSX의 `사용 후보 / 제외 후보 / 보류`는 검증 전 상태다. Agent가 실제 원문을 다시 읽고 후보를 `사용 / 사용 안 함`으로 확정하며, Ji가 카드의 설명 경계를 검토하고 진행을 막는 문제를 해결해야 `range_set`이 완료된다. `topic_raw`에는 그때 확정한 `사용` 구간만 입력한다.
