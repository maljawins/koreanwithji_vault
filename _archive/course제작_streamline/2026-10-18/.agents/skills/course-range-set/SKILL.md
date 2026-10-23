---
name: course-range-set
description: "Korean With Ji 코스에서 레슨별 영상 설명 경계와 매핑된 Ref_No의 raw 사용 구간을 확정하거나 수정할 때 사용한다. 확정 구간의 원문 발췌만 하는 topic_raw 작업에는 사용하지 않는다."
---

# Course range_set

레슨 한 편이 직접 설명할 내용과 자료별 사용 구간을 결정한다. 판단의 정본은 vault 루트 기준 `02_product/02_course_creation/course_plan.md` §2~3·§7이다. 실행법은 `02_product/02_course_creation/01_lesson_spec/lesson_spec_pilot_instruction.md`, status 기록법은 `02_product/02_course_creation/01_lesson_spec/lesson_spec_tracking.md`에서 현재 내용을 확인한다. 이 skill과 Hangul 사례가 현행 계획보다 앞서지 않는다.

## 시작할 때

1. vault의 `AGENTS.md`와 위 계획을 확인하고, 이번 요청의 레슨과 허용된 수정 범위를 잡는다.
2. V7의 `Ji 레슨 Title`과 `Ji 레슨 주제 (brainstorm)`, 앞뒤 레슨을 확인한다. brainstorm은 Ji의 구상 단서이며 확정 범위가 아니다.
3. 트랙별 index와 `lesson_spec_tracking.xlsx`의 `파일관리`·`외부자료`에서 이 레슨에 매핑된 **모든** Ref_No와 실제 raw 사본 경로를 대조한다. XLSX는 열 번호 대신 헤더명으로 읽는다. 필수 헤더가 없거나 중복되면 멈춰 보고하고, raw가 없거나 매핑이 어긋나면 추측해 채우지 않는다. `02_product/01_raw/`는 읽기 전용이다.

## 설명 경계를 정할 때

1. V7 제목 → brainstorm 참고 → 매핑된 Ji Draft → 매핑된 모든 raw 본문 순서로 읽는다. 여러 자료가 다루는 공통 설명 대상을 찾아 **이번 영상의 직접 설명**을 먼저 제안한다. 일부 자료에만 있는 조건·예외·예문도 설명에 필요하면 보조 근거로 남긴다. 공통 주제가 없거나 Ji Draft·제목과 충돌하면 근거를 모아 Ji의 방향 결정을 받는다.
2. 직접 설명을 정한 뒤 앞선 레슨의 짧은 복습과 다른 레슨에서 자세히 설명할 내용을 나눈다. 앞뒤 V7 레슨과 중복 매핑된 원문을 근거로 경계를 Ji에게 보여준다. Ji에게 명확한 줄마다 승인을 요구하지 않는다.
3. 같은 주제를 설명하는 서로 다른 출처의 관련 대목은 설명 방식이 달라도 각각 남긴다. 어느 설명을 영상에 채택하고 조합할지는 `topic_shaped`에서 판단한다. 개념 전수 추출, 표준명 등록, Structured Output JSON 생성은 이 단계의 조건이 아니다.

## Ref_No별로 판정할 때

- `01_Ji_draft`는 매핑된 파일 전체를 `사용`, `1~마지막 줄`의 한 구간으로 기록한다. 추론한 설명 경계와 어긋나는 대목은 자르지 않고 해당 Ref_No의 `판정 이유`에 Ji 판단이 필요한 근거를 적는다.
- 다른 자료는 전체를 자동 포함하지 않는다. YouTube는 `Teaching Points`를 먼저 보고 필요할 때 관련 `Transcript`를 읽는다. Amira의 동일 수업은 녹화 레슨 → PPT+Script 통합본 → Script 순서로 확인하며 같은 수업의 반복 설명을 독립 근거로 세지 않는다. Day 20 AI Script를 Ji의 실제 발화 근거로 쓰지 않는다. HTSK·web은 설명 본문을 확인한다. `02_ext_sources`·`03_original_PDF`는 Ji가 레슨과 범위를 지정했을 때만 쓰며, 매핑된 Hangul `06_ext_sources`는 index를 따른다.
- `02_product/02_course_creation/01_lesson_spec/01_range_set/duplicate_material_selection.xlsx`는 같은 원본의 연결 레슨·Ref_No를 찾는 단서다. 파일명만 믿지 말고 실제 본문을 대조한다. 각 대목을 어느 레슨에서 직접 설명할지 확인하고 충돌은 Ji에게 보인다. 이 표의 과거 발췌·제외 칼럼을 판정 근거로 쓰거나 다시 채우지 않는다.
- 관련 대목이 없으면 해당 Ref_No를 `사용 안 함`으로 판정하고 구체적인 이유를 적는다. 다른 자료에도 같은 주제가 있다는 이유만으로 관련 구간을 제외하지 않는다.

## 단일 검토 workbook

`02_product/02_course_creation/01_lesson_spec/01_range_set/range_set_review.xlsx`의 `Sheet1`이 자료 선택과 Ji 검토의 정본이다. 매핑된 모든 Ref_No를 `사용` 또는 이유가 있는 `사용 안 함`으로 판정하고, 떨어진 구간은 같은 Ref_No의 별도 행으로 둔다. `줄`을 실제 raw 사본과 대조해 제목만 있고 본문이 없거나 필요한 조건·예외가 빠지거나 다른 레슨의 상세 설명이 섞인 구간을 바로잡는다. `판정 이유`에는 **최초 Agent의 파일·구간 채택 이유와 판단 배경**을 남기고 이후 피드백을 반영해도 덮어쓰지 않는다. 기존 후보 판정은 미확정이다.

`원문 Ref_No`에는 해당 번호의 **실제 raw 사본을 바로 여는 하이퍼링크**를 건다. `자료명`은 이름만 표시한다. 링크 대상은 트랙별 index와 실제 파일을 대조한다. Ji는 `Ji 검토여부`에 직접 `O`를 표시하고 `Ji feedback`에 의견을 쓴다. Agent는 Ji 입력을 보존하고 원문 확인 → 같은 XLSX 수정 순서로 처리한다. 별도 `feedback.md`를 작성하거나 레슨별 Markdown 검토 카드를 동기화하지 않는다. 기존 `range_set_source_spans*.xlsx`는 새 판정의 입력처가 아니며 `duplicate_material_selection.xlsx`는 중복 매핑 확인용으로 보존한다.

## 완료 조건

모든 매핑 Ref_No의 최종 판정, 사용할 구간과 실제 원문의 대조, Ji의 직접 설명·복습·다른 레슨 경계 검토, 진행을 막는 문제 해결이 끝난 레슨만 tracking의 `레슨진행`을 `range_set`으로 올리고 `작업이력`에 근거를 남긴다. Ji의 빈 검토 칸을 승인으로 해석하거나 Agent가 `O`를 대신 표시하지 않는다. Ref_No·링크·상태·구간·이유가 실제 raw와 일치하는지 확인한다.

과거 Hangul-1·5·6의 Ji 결정은 참고 사례일 뿐이다. 다른 레슨의 규칙으로 복사하지 않고 현행 결정은 `range_set_review.xlsx`에서 확인한다.
