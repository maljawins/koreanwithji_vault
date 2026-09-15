# to_do — 지금 할 일

> **지금 착수할 것만 담는다.** 전체 로드맵, 작업 규칙, 남은 일 전체는 [`course_plan.md`](../../02_product/02_course_creation/course_plan.md).
> 작성 요령과 갱신 시점은 [`01_inbox.md`](../01_inbox.md).
> 기준일: 2026-09-14.

---

## 현재 위치

**STEP 2 · 재료 모으기: 파일럿 44개 `topic_copy` + `topic_raw`** ([`course_plan.md`](../../02_product/02_course_creation/course_plan.md) §3-2).
2026-09-13에 STEP 순서가 바뀌었다: template을 먼저 만들지 않고, 재료(발췌)와 개념부터 모은다. 산출물 0장.

---

## 지금 할 일

```
① Ji 결정 1건(git) → ② 44개 topic_copy → ③ 44개 topic_raw 발췌 → ④ 문자열 대조 검증 → STEP 2 게이트
```

### ① Ji가 먼저 정할 것

| # | 정할 것 | 권장 | 안 정하면 |
|---|---|---|---|
| J-1 | **spec 44장을 만들기 전에 git을 정리할지** ([`course_plan.md`](../../02_product/02_course_creation/course_plan.md) §12 리스크) | 지금 한 번 정리하고 커밋 | 산출물이 백업 없이 쌓인다. vault 전체가 git 미추적 상태 |

### ② ~ ④ 실행 (`course_plan.md` §3-2 STEP 2 표 2-1~2-5)

| # | 할 일 | 완료 조건 |
|---|---|---|
| N-1 | git 정리 + 커밋 (J-1이 "지금"이면) | 현재 vault가 git에 올라감 |
| N-2 | `topic_copy` 스크립트: V7 4번 컬럼을 레슨당 spec 1장으로 편다 + 파일명 규칙 적용 | 44장 생성 확인 |
| N-3 | `topic_raw` 조준 발췌. 규칙 5개 준수, Ref_No는 index xlsx로 매칭 | 44장 전부 `RAW_DIGEST` 채워짐 |
| N-4 | 발췌문 문자열 대조 검증 스크립트 실행 | 불일치 0. **STEP 2 게이트** |

이번 STEP에서는 template을 만들지 않는다. spec은 최소 뼈대(frontmatter + `TOPIC` + `TEACHING_POINTS` + `RAW_DIGEST`)로만 쓴다 ([`course_plan.md`](../../02_product/02_course_creation/course_plan.md) §6).

---

## 끝나면

N-4가 끝나면 이 목록을 비우고 **STEP 3(개념 indexing + `topic_shaped` 병행, `course_plan.md` §3-2)** 을 가져온다. 끝난 항목은 `course_plan.md` §3-1 실시 사항으로 옮긴다.
