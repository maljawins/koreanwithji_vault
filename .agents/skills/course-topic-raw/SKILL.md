---
name: course-topic-raw
description: "Korean With Ji 코스에서 확정된 range_set 사용 구간을 레슨별 RAW_DIGEST로 원문 그대로 발췌하거나 검증할 때 사용한다. 자료 사용 여부나 영상 설명 방식을 새로 결정하는 작업에는 사용하지 않는다."
---

# Course topic_raw

확정된 원문 구간을 출처와 함께 보관해 다음 `topic_shaped` 단계에 넘긴다. 판단의 정본은 vault 루트 기준 `02_product/02_course_creation/course_plan.md` §4·§7, 실행법은 `02_product/02_course_creation/01_lesson_spec/lesson_spec_pilot_instruction.md`의 `topic_raw` 절이다. 현행 계획과 레슨별 Ji 결정을 먼저 확인한다.

## 진입 조건

1. `02_product/02_course_creation/01_lesson_spec/01_range_set/range_set_source_spans.xlsx`의 `파일판정`·`사용구간`, 해당 `<레슨 ID>_range_set_review.md`, `02_product/02_course_creation/01_lesson_spec/lesson_spec_tracking.xlsx`를 대조한다. 모든 Ref_No가 최종 판정되고 Ji의 설명 경계 검토와 진행을 막는 `OPEN` 해결이 끝난 레슨만 발췌한다. 이미 작성된 `topic_raw`를 수정할 때도 현재 정본을 다시 대조한다.
2. `사용`인 Ref_No와 그 구간을 모두 모은다. 해당 레슨에 실제로 매핑된 raw 사본의 경로·Ref_No·줄 번호가 맞는지 index와 원문으로 확인한다. XLSX는 헤더명으로 읽는다. 경로나 판정이 불일치하거나 사용할 구간이 하나도 없으면 발췌를 중단하고 `range_set`의 판단을 먼저 바로잡는다. `02_product/01_raw/`는 읽기 전용이다.

## 작성 방법

`02_product/02_course_creation/01_lesson_spec/02_topic_raw/<레벨>/<레슨 폴더>/<레슨 ID>_topic_raw.md`에 레슨 ID와 `status: topic_raw`를 표시하고 `## RAW_DIGEST` 아래에 출처별 발췌를 둔다. 레벨·레슨 폴더명은 해당 raw 폴더와 맞춘다. Hangul 1~6의 `*_topic_raw.md`가 형식 사례다.

- 각 Ref_No에 실제 raw 사본으로 가는 링크, vault 루트 기준 상대경로, 원문 제목을 적는다. 선택 구간마다 원문 위치를 알 수 있는 짧은 주제와 **1부터 센** 시작·끝 줄을 붙인다. 한 Ref_No의 떨어진 구간은 각각 표시한다.
- 지정된 줄의 제목·본문·빈 줄·문장부호를 원문 그대로 붙인다. Ji Draft의 전체 사용 구간에는 frontmatter를 포함한 1~마지막 줄 전체를 붙인다. Markdown 안에 코드 울타리가 있으면 발췌를 감싸는 울타리를 더 길게 해 원문을 훼손하지 않는다.
- 같은 주제에 여러 출처가 있으면 설명이나 원인 해석이 달라도 Ref_No별로 각각 발췌한다. 여기서 요약·번역·교정·출처 혼합·Ji식 재서술을 하지 않는다. 설명의 채택·조화와 영상 순서는 `topic_shaped`에서 판단한다.

## 대조와 완료

각 발췌를 **해당 Ref_No의 실제 raw 사본**에서 지정한 줄과 문자 그대로 대조한다. 제목이나 본문 누락, 줄 밀림, 범위 밖 문장, 필요한 조건·예외 누락을 발견하면 원문을 임의로 덧붙이지 말고 `range_set`의 XLSX 구간을 먼저 고친 뒤 검토 카드와 발췌문을 맞춘다. 서로 다른 출처의 설명 차이만으로 발췌를 막지 않는다. 출처 충돌이나 정확성 우려는 발췌문을 고쳐 숨기지 않고 다음 단계에서 검토할 근거와 함께 별도로 남긴다.

XLSX의 `사용` Ref_No와 `사용구간`이 발췌물에 각각 한 번씩 대응하는지 세고, `사용 안 함` 자료가 들어가지 않았는지 확인한다. 링크·상대경로·제목·줄 번호·문자가 맞으면 tracking의 `레슨진행`을 `topic_raw`로 올리고 산출물 경로와 `작업이력`을 기록한다. 문자 대조 전에는 status를 올리지 않는다.
