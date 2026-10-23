# 코스 제작 계획

> 이 문서는 코스 제작 로드맵·작업 규칙·결정 기록의 단일 출처다.
> 최종 갱신: 2026-09-23

## 1. 바꾸는 것과 유지하는 것

기존 workflow에서 **concept index 제외**. 자료 매핑과 Ref_No, 그리고 `range_set → topic_raw → topic_shaped → lesson_spec → OUTLINE → DRAFT` 순서는 유지한다.

새 시작 단계는 `중복 자료 선별 xlsx → Ji 확인 → Structured Output JSON 구조 공동 결정`이다.

## 2. 새 workflow

1. 기존 index xlsx에서 레슨별 자료 매핑과 Ref_No를 읽는다.
2. 여러 레슨에 매핑된 같은 원본 자료만 `duplicate_material_selection.xlsx`에 목록화한다.
3. Agent는 각 레슨에서 사용할 teaching point·원문 구간, 제외 내용과 이유를 제안한다.
4. Ji가 xlsx에서 선별 기준과 결과를 확인·수정한다. Ji의 최종 선택 전에는 다음 단계로 진행하지 않는다.
5. xlsx 검토 결과를 보고 Ji와 Structured Output JSON의 종류·형태·필드·저장 위치를 결정한다.
6. 결정된 JSON으로 레슨별 teaching point를 종합한다.
7. 기존 `range_set`에서 원본 자료의 최종 사용 범위를 확정한다.
8. 기존 `topic_raw`에서 확정 범위의 원문을 발췌한다.
9. 기존 `topic_shaped`에서 발췌 내용을 teaching point 순서와 설명 경계로 정리한다.
10. 기존 lesson_spec·OUTLINE·DRAFT 규칙을 적용한다.

## 3. 중복 자료 선별 xlsx

경로: `01_lesson_spec/duplicate_material_selection.xlsx`

한 행은 **중복 원본 자료 × 대상 레슨**이다. 원본 자료 묶음은 동일 파일명의 여러 레슨 사본을 우선 후보로 삼고, 실제 원문과 출처가 다르면 Agent가 중복 후보에서 제외 사유를 기록한다.

| 칼럼 | 역할 |
|---|---|
| 원본 자료 묶음 ID | 같은 원본 자료 사본을 묶는 고정 번호 |
| 자료 제목·출처 | 어떤 자료인지 확인하는 이름과 트랙 |
| 대상 레슨·Ref_No·경로 | 해당 레슨의 실제 사본을 찾는 주소 |
| 전체 매핑 레슨 | 같은 원본이 쓰인 모든 레슨 |
| 자료 teaching point | 자료 전체에서 확인한 가르칠 내용 |
| Agent 제안 사용 내용·원문 구간 | 이 레슨에서 쓸 내용과 줄 번호 |
| 제외 내용·이유 | 다른 레슨으로 남기거나 쓰지 않는 내용 |
| Ji 검토 의견·최종 선택·상태 | Ji의 수정과 다음 단계 진입 여부 |

xlsx는 JSON보다 먼저 만들며, Agent의 선별 방식을 Ji가 직접 검토하는 기준표다.

## 4. 유지 규칙

- raw는 읽기 전용이다.
- Ref_No와 레슨별 자료 매핑의 정본은 기존 index xlsx다.
- `range_set`은 원본 자료에서 실제로 사용할 범위를 확정한다.
- `topic_raw`는 확정 범위의 원문 발췌다.
- `topic_shaped`는 발췌 내용을 teaching point 순서로 정리하는 단계다.
- 같은 Amira 세션의 Script·통합본·녹화본은 한 수업의 다른 기록이다. 서로 보완해 읽되, 독립 출처 여러 개로 세지 않는다.
- 출처·Ref_No·경로·원문 구간, BUDGET과 예문 검증, VSL·Intro 분리, [[01_lesson_spec/05_outline_and_draft/lesson_design_method]]는 유지한다.

## 5. 검증과 다음 결정

- 중복 자료 xlsx의 각 묶음에는 모든 매핑 레슨과 Ref_No가 있어야 한다.
- Agent 제안은 실제 원문을 읽은 뒤에만 작성한다. 원문 확인 전 상태는 `미검토`다.
- Ji 최종 선택이 없는 행은 JSON·`range_set`으로 넘기지 않는다.
- JSON의 개수, 필드, 저장 위치, 기존 Markdown 산출물과의 연결 방식은 xlsx 검토 후 Ji와 결정한다.
