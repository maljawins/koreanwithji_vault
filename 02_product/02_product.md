# 02_product 인덱스

> 이 폴더는 **판매할 상품을 실제로 만드는 곳**이다. 지금의 상품은 한국어 온라인 코스 하나다. (Phase 1)
> 원본 자료를 쌓아두는 곳(`01_raw`)과 그 자료로 강의를 만드는 곳(`02_course_creation`)이 분리돼 있다.
> 최종 갱신: 2026-09-15

---

## 폴더 구조

```
02_product\
├─ 02_product.md                    ← 이 파일. 폴더 인덱스
├─ 01_raw\                          ← 원본 자료 저장소 (읽기 전용 성격)
│   └─ 01_raw.md                    ← 자료 배치 규칙과 트랙 설명
└─ 02_course_creation\              ← 강의 제작 작업장
    ├─ 02_course_creation.md        ← 폴더 index (지도만)
    ├─ course_plan.md               ← 강의 제작 로드맵·계획의 유일한 출처
    ├─ glossary.md                  ← 코스 제작 용어 사전
    ├─ lesson_design_method.md      ← 레슨 상세 설계법 (outline, draft 단계)
    ├─ course_tech_stack.md         ← 코스 제작에 쓰는 도구와 기술
    ├─ 00_curriculum_and_index\     ← 커리큘럼 맵과 자료 index xlsx
    ├─ 01_lesson_spec\              ← [층 2] lesson_spec 작업장. topic_copy·raw·shaped 하위 폴더 포함
    ├─ 02_concept\                  ← concept_index.xlsx 작업장
    └─ 03_course_outline_and_draft\ ← [층 3] OUTLINE + [층 4] DRAFT 산출물
```

---

## 각 항목의 역할

| 항목 | 역할 |
|---|---|
| `01_raw\` | **입력.** 강의를 만들 재료가 되는 원본 .md가 전부 여기 있다 (1,747개). 에이전트는 여기서 읽기만 하고, 작업 산출물을 여기에 쓰지 않는다. 자료 배치 규칙은 [`01_raw.md`](01_raw/01_raw.md) 참조 |
| `02_course_creation\` | **작업장과 출력.** 원본을 근거로 개념을 정리하고 OUTLINE과 DRAFT를 만드는 모든 작업이 여기서 일어난다 |
| [`02_course_creation.md`](02_course_creation/02_course_creation.md) | 폴더 **지도**. 무엇이 어디 있는지와 단일 출처 규칙만 |
| [`course_plan.md`](02_course_creation/course_plan.md) | **강의 제작 로드맵과 계획의 유일한 출처.** 실시/미실시 사항, 현황 수치, 4층 구조, 작업 규칙, STEP 정의, 결정 기록, 리스크 |
| [`glossary.md`](02_course_creation/glossary.md) | 코스 제작 **용어** 단일 출처 |
| [`lesson_design_method.md`](02_course_creation/lesson_design_method.md) | 레슨 **상세 설계법** 단일 출처. outline, draft 단계에서 쓴다. Skeleton, Flesh, Comprehensible Input, 줌인 반복, 실생활 예시, 4MAT |
| [`course_tech_stack.md`](02_course_creation/course_tech_stack.md) | 코스 제작의 **도구** 단일 출처. Obsidian LLM Wiki, 영상 제작 자동화, 필요 역량 |
| `00_curriculum_and_index\` | 커리큘럼 맵 정본([`Korean Course Curriculum Map_Final_V7.xlsx`](02_course_creation/00_curriculum_and_index/Korean%20Course%20Curriculum%20Map_Final_V7.xlsx))과 자료 트랙별 index xlsx 5종 |
| `03_course_outline_and_draft\` | 레슨별 OUTLINE(층 3)과 DRAFT(층 4) 산출물이 쌓이는 곳. 한 레슨 폴더에 둘을 나란히 둔다 |

---

## 이 폴더의 대전제

**코스 완성이 사업 전체의 축이다.** 강의 Draft가 나와야 영상이 나오고, 거기서 숏폼, 롱폼, eBook, 블로그, 마케팅이 전부 파생된다. Draft가 비면 사업 전체가 빈다. 그래서 이 폴더가 Phase 1이고 최우선이다.

성패는 하나로 측정한다: **"Ji가 손으로 안 써도 Draft가 안정적으로 쌓이는 시스템이 도는가."**

---

## 작업 시작 전 확인할 것

- **작업 방법을 알고 싶으면** [`02_course_creation.md`](02_course_creation/02_course_creation.md)를 연다. 거기 지도가 있다. 이 파일에는 절차가 없다.
- **도구나 기술 얘기면** [`course_tech_stack.md`](02_course_creation/course_tech_stack.md)를 연다.
- **왜 이 순서로 하는지, 사업 전체에서 어디쯤인지**가 궁금하면 [`_about/Koreanwithji_기획서_v6_260902.md`](../_about/Koreanwithji_기획서_v6_260902.md)를 연다.
- **브랜드 톤과 메시지**는 [`_about/01_brand.md`](../_about/01_brand.md)가 단일 출처다. Draft를 쓸 때 반드시 근거로 삼는다.
- eBook은 Phase 2다. 코스 대본이 완성된 뒤 시작하므로 지금은 폴더를 만들지 않는다.
