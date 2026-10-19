# 01_range_set 인덱스

> 이 폴더는 레슨별로 raw에서 사용할 원문 구간을 확정하는 작업장이다. 판단·완료 기준은 [[course_plan]], 파일럿 실행 순서는 [[lesson_spec_pilot_instruction]]에 있다.

| 항목 | 역할 |
|---|---|
| `duplicate_material_selection.xlsx` | 같은 원본이 여러 레슨에 매핑된 묶음 ID·레슨·Ref_No를 찾는 목록. 발췌·제외 내용의 출처로 쓰지 않는다 |
| `range_set_review.xlsx` | `Sheet1`이 현행 자료 선택·Ji 검토의 단일 작업표. 최초 Agent의 채택 이유와 판단 배경, Ji가 직접 입력하는 `O`·feedback을 한곳에 둔다. `원문 Ref_No`를 실제 raw 사본으로 연결한다 |
| 기존 `*_range_set_review.md`·`*_range_set_feedback.md` | 과거 기록. 새 판단이나 Ji feedback을 여기에 기록하지 않는다 |
| 기존 `range_set_source_spans*.xlsx` | 과거 구간표. 새 판단의 정본으로 사용하지 않는다 |

레벨·레슨 폴더명은 `02_product/01_raw/01_by_level_lesson/`의 해당 폴더와 같게 쓴다. 원문 본문은 여기로 복사하지 않는다. Agent는 raw 확인 → `range_set_review.xlsx`의 `Sheet1` 수정 순서로 처리하고 최초 채택 이유와 Ji의 기존 feedback을 보존한다. Ji는 `Ji 검토여부`에 직접 `O`를 표시하고 `Ji feedback`에 의견을 쓴다. `원문 Ref_No` 링크는 해당 번호의 실제 raw 사본을 열어야 한다. 기존 후보는 검증 전 상태다. Agent가 원문을 읽고 `사용 / 사용 안 함`으로 확정하며, Ji가 설명 경계를 검토하고 진행을 막는 문제를 해결해야 `range_set`이 완료된다. `topic_raw`에는 그때 확정한 `사용` 구간만 입력한다.
