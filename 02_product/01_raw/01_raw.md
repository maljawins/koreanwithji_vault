# 01_raw 인덱스

> 이 폴더는 **강의를 만들 재료가 되는 원본 자료 저장소**다. 1,747개의 .md가 들어 있다.
> 에이전트는 여기서 **읽기만 한다.** 작업 산출물은 `02_course_creation`에 쓴다.
> 최종 갱신: 2026-09-03

---

## 이 폴더가 만들어진 전제 3가지

1. **Obsidian Vault는 `.md`만 읽는다.** 그래서 보유한 모든 자료(PPT, DOCX, PDF, Zoom 녹화 영상)를 `.md`로 변환해 두었다.
2. **시각 정보 보존이 중요하다.** 단순 텍스트 변환 도구(`markitdown`)만 쓰면 슬라이드와 영상 속 그림이 "그림1, 그림2"로만 남아 시각 정보가 유실된다. 그래서 핵심 자료는 **Gemini Vision API**로 이미지의 시각적 의미까지 텍스트로 추론해 보존했다.
3. **"일맥상통하게 병합"의 뜻.** 한 레슨에 대한 여러 출처(PPT, Script, 영상)를 서로 모순 없이 하나의 `.md`로 통합했다는 뜻이다. 목표는 **LLM이 그 파일 하나만 읽고 레슨 전체를 이해하는 것**이다.

---

## 폴더 구조

```
01_raw\
├─ 01_raw.md              ← 이 파일. 폴더 인덱스
├─ 01_by_level_lesson\    ← 레슨별로 정리된 자료 (핵심). 레벨 16개, 레슨 폴더 196개
├─ 02_ext_sources\        ← 레슨에 매이지 않는 범용 참고 자료
└─ 03_original_PDF\       ← 변환 전 원본 PDF 보관
```

---

## 1. 01_by_level_lesson (핵심 자료)

강의 레슨 하나가 폴더 하나다. 그 안에 **자료 출처별 트랙 폴더**가 들어 있다. 폴더 트리는 커리큘럼 맵과 일치한다.

```
01_by_level_lesson\
└─ Level_1\
    └─ 5_Verb_101_Present_Tense_Conjugation\
        ├─ 01_Ji_draft\   ← Ji가 직접 쓴 미완성 Draft
        ├─ 02_yt_md\      ← 유튜브 영상 변환본
        ├─ 03_Amira\      ← 1:1 학생 Amira 레슨 자료
        ├─ 04_HTSK\       ← howtostudykorean.com
        └─ 05_Reddit\     ← 일부 레슨에만 존재
```

### 레벨별 레슨 수 (폴더 기준)

| 레벨 | 레슨 | 레벨 | 레슨 | 레벨 | 레슨 |
|---|---|---|---|---|---|
| 00_VSL | 1 | Level_3 | 14 | Level_8 | 12 |
| 01_Intro | 2 | Level_4 | 14 | Level_9 | 12 |
| 02_Hangul | 6 | Level_5 | 12 | Level_10 | 14 |
| 03_Numbers | 7 | Level_6 | 12 | Level_11 | 22 |
| Level_1 | 21 | Level_7 | 20 | Level_12 | 17 |
| Level_2 | 10 | | | **합계** | **196** |

> 이 표는 **폴더 실측치**다. 커리큘럼 정본은 [`02_course_creation/00_curriculum_and_index/Korean Course Curriculum Map_Final_V7.xlsx`](../02_course_creation/00_curriculum_and_index/Korean%20Course%20Curriculum%20Map_Final_V7.xlsx)이며, 둘이 어긋나면 xlsx가 이긴다.

### 트랙별 자료 수

| 트랙 | .md 개수 |
|---|---|
| `01_Ji_draft` | 97 |
| `02_yt_md` | 849 |
| `03_Amira` | 438 |
| `04_HTSK` | 339 |
| `05_Reddit` | 4 |

**주의 2가지**
1. **빈 트랙 폴더는 만들지 않는다.** 레슨 안에 `01_Ji_draft`, `02_yt_md`, `03_Amira`, `04_HTSK` 중 특정 트랙 폴더가 없으면 그 레슨에는 해당 출처의 자료가 매핑되지 않았다는 뜻이다(폴더 자체를 안 만들어 표시). 반드시 폴더 존재로 자료 유무를 확인하고, 없으면 없다고 보고한다. Ji가 직접 가져오거나 md 변환을 통해서 가져오지 않는 이상 임의로 폴더나 파일을 만들지 않는다.

---

### 1-1. `01_Ji_draft` (가장 중요)

Ji가 직접 작성해 둔 **미완성 Draft** 모음이다.

- Draft가 있는 레슨도 있고 없는 레슨도 있다. 초반부 레벨일수록 완성도가 높다. 1차 Drafting 이후 커리큘럼 맵이 바뀌어서 Draft가 없는 레슨도 있다.
- Ji의 Rough Idea이므로, 에이전트가 Draft 초안을 만들 때 **Base 자료**로 쓴다.
- **완성도 90% 수준의 본보기 3개**: Level 1-1 *How Korean works*, Level 2-1 *은/는 & 이/가*, Level 2-2 *TSV Sentence Structure #1 - The Rule of Three*. Ji 고유의 설명법과 unique style이 고스란히 들어 있다.
- **"TSV Sentence Structure"와 "Rule of Three"는 Ji가 직접 만든 용어다.** 특히 "Rule of Three"는 강의 전반에 걸쳐 incorporate될 central concept이다. 임의로 다른 이름으로 바꾸지 않는다.
- 이 트랙은 **brand voice의 기준**이기도 하다. 톤 규칙의 단일 출처는 [`_about/01_brand.md`](../../_about/01_brand.md) §8.

### 1-2. `02_yt_md`

- 커리큘럼 맵에 매핑된 유튜브 영상을 `.md`로 변환해, 맵의 폴더 구조와 일치하게 정리한 자료.
- 단순 YouTube transcript만으로는 에이전트가 영상 내용을 이해할 수 없다. 그래서 **Gemini Vision**으로 시각 정보까지 캡처했다.
- 변환 규칙과 파이프라인은 [`_vault_setup/01_md_convert/korean_yt_md_guide.md`](../../_vault_setup/01_md_convert/korean_yt_md_guide.md)가 단일 출처다.

### 1-3. `03_Amira`

Ji가 직접 1:1로 가르친 학생 **Amira**와의 Zoom 레슨 자료를 `.md`로 변환한 모음이다. 원본은 PPT, Lesson Script, Zoom 녹화 영상 3종이다.

이 트랙에는 **3가지 자료 형태**가 있다.

| 형태 | 파일명 패턴 | 내용 |
|---|---|---|
| 1 | `Lesson script.md` | 레슨 전에 미리 써둔 `Script.docx`를 `markitdown`으로 단순 변환한 것. PPTX 직접 변환본은 시각 정보가 유실돼 삭제했다 |
| 2 | `1on1 lesson XX_XXXX [PPT+Script 통합].md` | **레슨 진행 전 준비 자료(Script + PPT)만** 통합한 것. Zoom 녹화본은 쓰지 않았다. 슬라이드를 이미지로 추출해 Gemini Vision(Flash)으로 시각적 의미를 추론한 뒤 Script와 병합했다 |
| 3 | `Amira_DayXX_XXXX_PartX_Lesson.md` | **실제 진행한 Zoom 녹화 영상**의 내용. Gemini Vision으로 시각 정보를 해석하고, Ji와 Amira가 실제 발화한 내용을 토대로 레슨을 재구성했다 |

**예외 사례들 (녹화 누락 복원)**

| 세션 | 누락 유형 | 처리 |
|---|---|---|
| Day 10 (0322) | 앞부분 누락 | Part 1 앞부분 녹화 미시작. 도입부를 `[PPT+Script 통합].md`로 복원하고 `⚠ Recording started mid-lesson` 배너 삽입 |
| Day 20 (0707) | 앞부분 누락 + Script 없음 | 동일하게 head-clip 처리. **Script 파일 자체가 없어** 세션 18·19·21을 few-shot 예시로 삼아 Gemini로 Script를 합성 생성한 유일한 세션 |
| Day 05-06 (0226) | 끝부분 누락 | Part 3 전체 미녹화. `⚠ NO ZOOM RECORDING` 배너 + PPT+Script로 복원 |
| Day 12 (0406) | Part 1 누락 | Part 2만 실제 영상 존재. Part 1을 PPT+Script로 복원 + 배너 |
| Day 17 (0507) | Part 2 누락 | Part 1·3은 존재. Part 2를 대본으로 복원 + 배너 |

> Day 20의 Script는 **AI가 생성한 것**이다. Ji가 실제로 말한 내용이 아니므로 brand voice 근거로 쓰지 않는다.

### 1-4. `04_HTSK`

howtostudykorean.com의 모든 Unit과 레슨을 `.md`로 변환한 자료다.

### 1-5. `05_Reddit`

Reddit에서 Obsidian Web Clipper로 가져온 .md. 2026-09-02 기준 4개뿐이다.

---

## 2. 02_ext_sources (범용 참고 자료)

특정 레슨에 매이지 않고 여러 레슨에 걸쳐 쓰이는 자료다.

### `01_공부법\` — 언어 학습법
| 파일 | 비중 |
|---|---|
| `Fluent Forever.md` | **중요.** 언어 학습법 베스트셀러 원문 |
| `Fluent Forever_학습법 정리.md` | **중요.** 책의 학습법을 정리한 것 |
| `Fluent Forever_사업 적용.md` | **중요.** 책 내용을 이 사업에 적용하는 방안 리포트 |
| `CosmoJina.md` | 단순 참고. 크리에이터 "코스모지나"의 언어 학습법 |

> Fluent Forever 3종은 **브랜드 교육 철학의 학술적 백본**이다. 활용 방침은 [`_about/01_brand.md`](../../_about/01_brand.md) §9가 단일 출처다.

### `02_한글\`
국립국어원 공식 자료. 한글 맞춤법, 발음 법칙, 외래어 표기법 규정집. **Hangul 섹션 레슨 제작 시 활용한다.**

### `03_textbook\` — 교재 변환본
Gemini Vision으로 시각 정보까지 캡처했다. 단, **변환이 온전하지 않은 것이 있다.**

| 교재 | 상태 |
|---|---|
| Korean Grammar in Use (Beginner/Intermediate/Advanced) | 오류와 토큰 과다로 **변환 미실시.** 원본 PDF만 있음 |
| 연세한국어 1-1 | 동일 사유로 **변환 미실시.** 원본 PDF만 있음 |
| Conversational Korean grammar | 원본 298p 중 **133p까지만 변환됨. 검토 필요** |
| LP's Korean Language Learning | 원본 205p 중 **135p까지만 변환됨. 검토 필요** |
| TTMIK, Go Billy (Korean Made Simple) | 변환본 존재 |

### `04_about_korean\`
국립국어원 *Everything You Wanted to Know about the Korean Language* 변환본. 학습 자료가 아니라 한국어에 관한 정보 위주다.

---

## 3. 03_original_PDF (변환 전 원본)

`.md` 변환이 제대로 안 됐거나 원본 보관이 필요한 자료를 PDF로 모아둔 곳이다. **Obsidian은 `.md`만 읽으므로 LLM이 이 폴더를 직접 읽지는 않는다.** 재변환이 필요하거나 원본 대조가 필요할 때만 쓴다.

| 하위 폴더 | 내용 |
|---|---|
| `01_textbook\` | 위 §2 표에서 변환 실패·부분 변환으로 표시된 교재 6권의 원본 |
| `02_1on1_PDF\` | 1:1 강의 당시 PPT를 PDF로 변환해 보관. 내용은 이미 `03_Amira` 트랙의 `[PPT+Script 통합].md`에 Gemini Vision으로 통합돼 있다 |

> 1:1 레슨에서 쓴 PPT를 PDF로 변환해 이 폴더에 추가하였다.

---

## 자료 사용 규칙

1. **읽기 전용이다.** 이 폴더의 파일을 고치거나 새로 만들지 않는다. 산출물은 `02_course_creation`에 쓴다.
2. **출처를 반드시 남긴다.** 개념이나 예문을 가져오면 어느 트랙의 어느 파일에서 왔는지 기록한다. 근거 없는 내용은 만들지 않는다.
3. **`01_Ji_draft`가 톤의 기준이다.** 다른 트랙은 내용의 재료이고, Ji의 말투와 설명 방식은 이 트랙에서 가져온다.
4. **트랙 폴더가 없으면 그 레슨에 해당 자료가 없다는 뜻이다.** 없으면 없다고 보고하고 다음 단계를 Ji에게 묻는다.
5. **PDF를 직접 읽어야 하면 Ji에게 먼저 알린다.** 토큰 소모가 크다.
6. **트랙별 index**는 `02_course_creation/00_curriculum_and_index`의 xlsx 5종이 관리한다. 자료 커버리지를 확인할 때 그쪽을 먼저 본다.
