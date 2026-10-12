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

- `01_Ji_draft`는 매핑된 파일 전체를 `사용`, `1~마지막 줄`의 한 구간으로 기록한다. 추론한 설명 경계와 어긋나는 대목은 자르지 않고 카드에 Ji 확인 사항으로 적는다.
- 다른 자료는 전체를 자동 포함하지 않는다. YouTube는 `Teaching Points`를 먼저 보고 필요할 때 관련 `Transcript`를 읽는다. Amira의 동일 수업은 녹화 레슨 → PPT+Script 통합본 → Script 순서로 확인하며 같은 수업의 반복 설명을 독립 근거로 세지 않는다. Day 20 AI Script를 Ji의 실제 발화 근거로 쓰지 않는다. HTSK·web은 설명 본문을 확인한다. `02_ext_sources`·`03_original_PDF`는 Ji가 레슨과 범위를 지정했을 때만 쓰며, 매핑된 Hangul `06_ext_sources`는 index를 따른다.
- `02_product/02_course_creation/01_lesson_spec/01_range_set/duplicate_material_selection.xlsx`는 같은 원본의 연결 레슨·Ref_No를 찾는 단서다. 파일명만 믿지 말고 실제 본문을 대조한다. 각 대목을 어느 레슨에서 직접 설명할지 확인하고 충돌은 Ji에게 보인다. 이 표의 과거 발췌·제외 칼럼을 판정 근거로 쓰거나 다시 채우지 않는다.
- 관련 대목이 없으면 해당 Ref_No를 `사용 안 함`으로 판정하고 구체적인 이유를 적는다. 다른 자료에도 같은 주제가 있다는 이유만으로 관련 구간을 제외하지 않는다.

## 정본과 검토 카드

`02_product/02_course_creation/01_lesson_spec/01_range_set/range_set_source_spans.xlsx`의 `파일판정`·`사용구간`이 정본이다. `사용 후보`·`제외 후보`·`보류`는 미확정이다. 해당 레슨의 모든 Ref_No를 `사용` 또는 이유가 있는 `사용 안 함`으로 판정한다. `사용구간`에는 실제 사본의 시작·끝 줄, 원문 위치, 쓰임, 선택 이유, 검증 상태를 남긴다. 떨어진 대목은 별도 구간으로 두고 `레슨 ID + Ref_No + 구간 순번`으로 구별한다. 선택 구간에 제목만 있고 본문이 없거나, 필요한 조건·예외가 빠지거나, 다른 레슨의 상세 설명이 섞이지 않게 실제 줄을 재확인한다.

`02_product/02_course_creation/01_lesson_spec/01_range_set/<레벨>/<레슨 폴더>/<레슨 ID>_range_set_review.md`에는 직접 설명·복습·다른 레슨의 상세 내용, 그 레슨의 **모든 Ref_No**와 실제 raw 사본 링크, XLSX의 판정·모든 선택 줄·짧고 구체적인 주제·이유를 반영한다. 구간이 없으면 `선택 구간 없음`으로 표시한다. `Ji가 정할 내용`과 이유·답변은 설명 경계, 자료 부족, 출처 충돌처럼 Ji의 결정이 필요한 문제에만 쓴다. 원문 재독과 줄 검증은 `Agent가 확인할 사항`으로 분리한다. 기존 Ji 답변과 검토 의견은 보존한다. 수정 순서는 **원문 확인 → XLSX 수정 → 카드 자료표 반영**이다.

## 완료 조건

모든 매핑 Ref_No의 최종 판정, 사용할 구간과 실제 원문의 대조, Ji의 직접 설명·복습·다른 레슨 경계 검토, 진행을 막는 `OPEN` 해결이 끝난 레슨만 tracking의 `레슨진행`을 `range_set`으로 올리고 `작업이력`에 근거를 남긴다. 후보 판정이나 카드 작성만으로 완료 처리하지 않는다. 카드의 Ref_No·링크·상태·구간·이유가 XLSX와 일치하는지 확인한다.

애매한 경우 Hangul-1 검토 카드의 서로 다른 출처 보존, Hangul-5의 Ji Draft 전체 사용, Hangul-6의 Ji가 허용한 설명 깊이 이월을 **사례**로 볼 수 있다. 레슨별 Ji 결정 자체를 다른 레슨의 규칙으로 복사하지 않는다.
