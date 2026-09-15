# korean_yt_md_guide.md

> Korean 트랙 전용 규칙서. 이 파일 하나만 읽고도 한국어 강의 영상 변환 작업이 가능하도록 작성됨.
> AI·코딩·개발 등 tech 영상 변환은 이 파일이 아니라 `tech_yt_md_guide.md`를 따른다.
> 두 트랙은 **스크립트까지 완전히 분리**되어 있다. 서로 참조하지 않고 코드도 공유하지 않는다.
> 최종 갱신: 2026-08-30

---

## 1. 프로젝트

`korean_yt_md_convert.xlsx`에 나열된 YouTube 영상을 시청·이해해서 .md 파일로 변환하는 작업.

**변환된 .md의 목적**
한국어 학습 관련 영상을 레슨별 강의 Draft의 원료로 쓴다. `01_inbox\`에 떨어지면 Ji가 검토한 뒤 해당 레슨 폴더(`02_course_creation\01_raw\01_by_level_lesson\Level_{n}\{레슨}_*\02_yt_md\`)로 직접 옮긴다. 이후 OUTLINE → DRAFT 작성의 근거 자료가 된다.

**따라서 korean .md는 "정보 보존"이 목적이다.**
tech 트랙과 정반대다. 강사가 실제로 한 말, 예문, 뉘앙스, 설명 순서를 전부 남긴다. 요약해서 버리면 나중에 Draft를 쓸 때 근거가 사라진다.

**현재 상태 (2026-08-30 기준)**
xlsx 9개 행 전부 `O`(변환 완료). 기존 결과물은 이미 각 레슨 폴더에 들어가 있다. 신규 변환 대상 없음. 영상을 추가하려면 xlsx에 행을 넣고 md보유여부를 `X`로 둔다.

---

## 2. 트랙 경계

| 항목 | Korean 트랙 (이 문서) | Tech 트랙 |
|---|---|---|
| 스크립트 | `kor_yt_md_pipeline.py` | `tech_yt_md_pipeline.py` |
| 입력 xlsx | `korean_yt_md_convert.xlsx` | `tech_yt_md_convert.xlsx` |
| 파일명 접두어 | `kor_` | `tech_` |
| 결과물 소비자 | Ji + Claude (강의 Draft 원료) | Claude (vault 운영·코드 작성) |
| 영상 다운로드 화질 | 480p | 1080p |
| Whisper 유도 프롬프트 | 한국어 단어를 **한글로** 받아쓰게 유도 | 영문 기술용어를 **영문으로** 받아쓰게 유도 |
| OCR 앵커 | 화면의 **한글** 토큰 수집 | 화면의 **영문** 용어·명령어 수집 |
| 본문 언어 | 전부 영어 | 한국어 + 영어 용어 병기 |
| Transcript | 전문 보존 | 없음 |
| 예문 형식 | 블록 인용 (한국어 예문 + 영어 해석) | 코드블록 (명령어·설정 원문) |
| 섹션 타임스탬프 | 없음 | 있음 |
| 정보 처리 | 보존 (누락 금지) | 압축 (잡음 제거) |
| 출력 폴더 | `01_inbox\` (양쪽 동일) | `01_inbox\` |

### 스크립트를 완전히 분리하는 이유

두 트랙은 4단계(Whisper 받아쓰기)부터 갈라진다. 프롬프트만 다른 게 아니다.

korean 트랙의 Whisper 유도 프롬프트는 "한국어 단어는 로마자가 아니라 한글로 받아쓸 것"을 지시한다. 이 지시가 tech 영상에 걸리면 `Agent`가 `에이전트`로, `MCP`가 `엠씨피`로 기록된다. tech 트랙에 필요한 것과 정확히 반대다. OCR 앵커 수집도 마찬가지다. korean은 화면의 한글만 모으는데, tech 영상 화면의 정답지는 영문 명령어와 파일명이다.

그래서 두 스크립트는 공통 모듈 없이 각자 완결된 파일로 둔다. korean 작업과 tech 작업을 동시에 돌릴 일이 없으므로 파일이 갈라져 있어 생기는 불편이 없고, 한쪽을 고치다 다른 쪽이 오염될 위험이 구조적으로 사라진다.

**중요**: `tech_yt_md_pipeline.py`는 이 스크립트를 복사해서 고친 것이 아니다. 위 한국어 전용 지점이 1,000줄 넘는 코드에 흩어져 있어 눈으로 걷어내면 반드시 빠뜨린다. 빠뜨려도 에러가 안 나고 결과만 조용히 나빠진다. 반대 방향도 같다. 한쪽 스크립트를 다른 쪽에 복사하지 않는다.

---

## 3. 입력

**파일**: `C:\vault\Koreanwithji_vault\_vault_setup\01_md_convert\korean_yt_md_convert.xlsx`

> 정본은 이 경로 하나다. 과거 `02_course_creation\00_curriculum_and_index\02_yt_md_convert.xlsx`에 동일 사본이 있었으나 2026-08-30 삭제됨. 사본을 다시 만들지 않는다.

**컬럼**

```
Ji 레벨 / Ji 레슨 / Ji 레슨 Title / Raw 종류 / 채널 / Playlist / Ref_No /
영상 타이틀 / 링크 / md보유여부 / 추가변환 필요여부
```

**md보유여부 3단계 상태값** (tech 트랙과 동일하게 통일)

- `X` = 미변환. **스크립트 처리 대상은 X인 행뿐이다.**
- `O` = 변환 완료
- `F` = 검증 실패. `01_inbox\convert_fail\` 보관, 사람 검토 대기

변환 성공 시 X → O, 검증 실패 시 X → F로 자동 갱신 후 xlsx 저장. O와 F는 재실행 시 건너뛴다. 공란은 X로 간주하지 않는다(오작동 방지).

---

## 4. 출력

### 저장 위치

```
C:\vault\Koreanwithji_vault\01_inbox\
```

평면 저장. 하위 폴더를 만들지 않는다.

`01_inbox`는 AI 산출물이 최종 분류되기 전 Ji가 검토하는 수신함이다. 변환된 .md는 여기 떨어지고, Ji가 읽은 뒤 직접 해당 레슨 폴더로 옮긴다.

**스크립트가 레슨 폴더에 직접 저장하지 않는다.** 레벨·레슨 폴더를 글롭 매칭으로 찾아 자동 저장하던 예전 방식은 폐기됐다. 대신 레벨·레슨 정보를 파일명에 넣어 Ji가 분류할 때 파일을 열어보지 않아도 되게 한다.

### 파일명 규칙

```
kor_[레벨]-[레슨]_[채널]_[영상제목]_[변환일].md
```

- `레벨`, `레슨`: xlsx의 `Ji 레벨`, `Ji 레슨` 값. **두 자리로 0을 채운다.**
  - 레벨 1, 레슨 15 → `01-15`
  - 레벨 10, 레슨 2 → `10-02`
  - 0을 안 채우면 정렬 시 Level 10이 Level 2보다 앞에 온다. 정렬해서 분류하는 게 이 규칙의 목적이므로 0 채우기는 필수다.
  - 레벨 값이 숫자가 아닌 경우(`Hangul`, `Intro`, `VSL`, `Numbers` 등)는 값을 그대로 쓰고 공백은 `_`로 바꾼다. 예: `kor_Hangul-03_...`
- `변환일` = **변환을 실행한 날짜** (YYMMDD). 영상 업로드 날짜를 파일명에 쓰는 것은 **절대 금지**.
- `Playlist`는 파일명에 넣지 않는다. Metadata에만 기록한다.

예:

```
kor_01-15_Go Billy_The HIDDEN meaning of 반갑다 Korean FAQ_260830.md
kor_01-07_Miss Vicky_Object Particles 을 를 usage & what to note_260830.md
```

`kor_` 접두어는 필수다. `01_inbox`가 catchall 폴더라 tech 결과물 및 다른 파일과 섞이는데, 접두어가 있어야 골라낼 수 있다.

### 파일명 금지문자 처리

Windows 파일명에 다음 문자를 쓸 수 없다.

```
\ / : * ? " < > |
```

유튜브 제목에는 `|` 와 `?` 가 자주 들어간다. 실제로 이 xlsx에도 `The HIDDEN meaning of 반갑다 | Korean FAQ` 같은 제목이 있다. 처리 규칙:

1. 위 9개 문자를 **공백 1개로 치환**한다
2. 연속 공백은 1개로 합친다
3. 앞뒤 공백을 잘라낸다
4. 파일명 전체 길이가 200자를 넘으면 영상제목 부분을 잘라낸다 (접두어·레벨·날짜·확장자는 보존)

치환하지 않고 삭제하면 단어가 붙어버려 검색이 안 되므로 반드시 공백으로 치환한다.

### 검증 실패 파일

검증 실패(규칙 위반·커버리지 누락) .md는 **절대 삭제하지 않는다.** 사람이 나중에 쓸만한지 검토할 수 있도록 다음 위치에 원본 파일명 그대로 저장한다.

```
C:\vault\Koreanwithji_vault\01_inbox\convert_fail\
```

접두어를 추가로 붙이지 않는다(파일명이 이미 `kor_`로 시작한다). xlsx의 md보유여부는 F로 갱신한다.

---

## 5. .md 파일 구조

```
# [채널명] | [영상 제목]

## Metadata
(불릿 리스트)

---

## Teaching Points

### Overview
(강사의 접근 방식과 맥락 - 2~3 문단)

---

### [섹션명 - 번호 없음, 설명적]
(내용)

---

## Transcript
(전체 발화, 타임스탬프 없음)
```

### Metadata 형식

불릿 리스트만 허용. 테이블 형식(`| Field | Content |`) 절대 금지.

```
- **Channel:** Learn Korean with GO! Billy Korean
- **Playlist:** FAQ  ← Playlist가 있는 경우만 포함
- **URL:** https://youtu.be/XXXXXXXXXXX
- **Duration:** 7:03
- **Upload Date:** 2023-03-27
- **Mapped Ji Lesson:** 1-07 SOV Sentence Structure
- **변환일:** 2026-08-30
```

`Mapped Ji Lesson`은 Ji가 분류할 때 최종 확인하는 값이다. 반드시 채운다.

---

## 6. 작성 언어 규칙

- 모든 설명·분석은 **영어**로 작성한다. (코스 draft도 영어로 작성 예정)
- 한국어 단어·문장·예문은 **한글 그대로 유지. Romanize 절대 금지.**
  - (O): `이다 is used to mean 'to be'`
  - (X): `ida is used to mean 'to be'`
- 한국어 표현 등장 시 한글 + 영어 해석 병기: `먹다 (to eat)`, `저는 학생이에요 (I am a student)`

---

## 7. Teaching Points 작성 원칙

- 첫 섹션은 반드시 `### Overview`. 강사 접근 방식·맥락·학습 흐름을 2~3 문단으로 서술한다.
- **섹션명**: 번호 prefix 금지. 주제를 설명적으로 표현한다.
  - (O): `### What Is the Possessive Marker 의?`
  - (X): `### 1. What Is the Possessive Marker?`
- **본문 스타일**: 산문 서술체. 불릿 나열 금지.
  - (O): "Billy explains that 의 can be omitted when the meaning is already clear..."
  - (X): "- 의 can be omitted when meaning is clear"
  - 단, 한국어 예문·conjugation 차트·비교표처럼 본질적으로 리스트인 정보는 불릿·테이블 유지 가능.
- **Over-summarize 금지.** 강사가 실제로 설명한 grammar rule, usage condition, exception, nuance, 예문을 빠짐없이 기술한다.
- **가장 중요**: LLM이 이 .md 하나만 보고 해당 영상의 가르침을 충실히 재구성할 수 있는 수준의 상세도를 요구한다.

### 한국어 예문 형식

블록 인용 (독립 예문):

```
> **저는 한국인이 아니에요.** / I am not a Korean person.
```

인라인 (짧은 단어·표현): `가다 (to go), 먹다 (to eat)`

---

## 8. Transcript 작성 원칙

- 섹션 누락 금지. 짧은 영상(5분 미만)도 전체 발화를 기록한다.
- 타임스탬프 제거, 자연스러운 문장 단위로 기록한다.
- 영어 발화는 영어 그대로, 한국어 발화는 한글로. Romanize 금지, 번역 금지.
- 1차 소스는 로컬 Whisper(large-v3) + VAD 필터. **유튜브 자막(CC)은 쓰지 않는다.**
  VAD로 무음 구간을 비워 환각("You You Okay brother" 류)을 차단하고, 화면 OCR로 한글 철자를 교정한다.
- Transcript 섹션 상단에 다음 줄을 넣는다:

```
> **Note:** Transcript reconstructed via local Whisper (large-v3) with VAD. May contain minor recognition errors.
```

---

## 9. 파이프라인 (기술 스택)

**코드**: `_vault_setup\01_md_convert\_scripts\kor_yt_md_pipeline.py`
**환경**: GPU RTX 4070 Laptop (8GB VRAM)
**합성 모델**: Gemini 3 Flash (`gemini-3-flash-preview`). 구형 2.5 아님.
**비용**: 스크립트 내 하드 상한 없음. 한도는 Google AI Studio 콘솔에서 관리. CostTracker가 누적 토큰·원화를 로그에 기록(모니터링용).
**병목**: 로컬 Whisper. 다운로드·OCR·Gemini는 동시 처리.

**핵심 원리**: 돈 드는 일(영상 100시간 보고 듣기)은 전부 로컬에서 무료로 처리하고, Gemini에는 "타임라인 텍스트 + distinct 프레임 이미지"만 보내 .md만 쓰게 한다. 영상 자체를 클라우드에 안 보내므로 비용이 예측 가능하고 Rate Limit 위험이 작다.

### 로컬 도구 (전부 무료)

- **yt-dlp** - **480p** mp4 1개만 다운로드. 강의 영상은 큰 글씨 자막·판서 위주라 480p로 충분하다. (tech 트랙은 1080p를 쓴다. 이유는 tech 가이드 참고.)
- **ffmpeg** - mp4에서 오디오(16k mono) 추출 + 분석용 프레임 추출
- **faster-whisper (large-v3)** - GPU 받아쓰기. VAD 필터 ON
  - 유도 프롬프트: 한국어 단어를 **한글로** 받아쓰고 로마자 표기를 금지하는 지시. 영어는 영어로 유지.
- **변화 감지 키프레임** - 직전 대비 화면이 바뀐 순간만 보존 (지각해시 dedup)
- **PaddleOCR (korean, CPU)** - 보존 프레임의 한글 텍스트 추출. 화면의 **한글 토큰**을 앵커(철자 정답지)로 수집

### 클라우드 LLM

- `GEMINI_API_KEY` (`.env`). Tier 1 = Batch 불가 → 동기 호출 + asyncio 동시성 + 지수 백오프
- 시스템 프롬프트(규칙 + exemplary)는 호출마다 고정 → 암묵 캐싱으로 입력비 절감
- 누적 토큰·원화 실시간 추적 (로그·manifest 기록용)

### v1 문제점 → v2 해결

1. **Transcript 퀄리티** - v1은 유튜브 자막(CC)을 1차로 썼는데 영어 설명 중 한국어 단어를 엉뚱하게 인식했다.
   예: 오디오 "어느, 무슨, 어떤" → 자막 "On, Musen" (https://youtu.be/c1gr-XWoJD0)
   → v2: 자막 안 씀. 항상 Whisper(large-v3, 한국어 프롬프트) + 화면 OCR로 한글 철자 교차검증.
2. **변환 시간 과다** → v2: 단일 다운로드 + 자원별 세마포어로 스테이지 동시 처리(GPU 안 쉼).
3. **Gemini Rate Limit** → v2: 영상 미전송으로 TPM 급감 + 적응형 동시성 + 지수 백오프.
4. **시각 정보 손실 (가장 중요)** → v2: 변화감지 무손실 키프레임 + 프레임 이미지 직접 전송 + AUDIO/SCREEN 타임라인 병합 + 커버리지 검증 루프.

---

## 10. 프레임 시청 처리 원칙 (**매우 중요**)

시각 정보 손실은 v1의 최대 약점이었다. v2는 OCR로 "묘사"시키지 않고 Gemini가 프레임을 직접 본다.

### 캡처 (로컬, 무손실)

- ffmpeg로 내부 초당 2~4장 분석 → 직전 프레임 대비 화면이 의미있게 바뀐 순간만 보존
  ("바뀜" = OCR 텍스트 변화 OR 시각적 변화). 화면에 새 정보가 뜰 때마다 반드시 프레임이 남는다.
- 같은 화면 연속은 지각해시로 1장 합침(정보 없는 중복만 버림). 애니메이션은 단계별로 여러 장 보존.
- 무음 구간이든 발화 구간이든 동일 적용 → 시각 누락이 구조적으로 불가능.

### 전송·기록

- 보존된 distinct 프레임을 전부 Gemini에 이미지로 전송 (장당 약 258토큰).
  단, 그래픽 없이 글자만 있는 게 확실한 슬라이드는 OCR 텍스트로 대체 가능(비용 밸브). 애매하면 이미지.
- 프레임을 timestamp 목록으로 .md에 따로 나열하지 않는다. 시각적으로 이해한 내용은 반드시 Teaching Points 산문에 통합한다.
  예: "The instructor visually demonstrates how 먹다 transforms: 다 is removed, then 어요 is added, resulting in 먹어요."
- 통합 대상: 글자 변형 애니메이션, conjugation 차트·표, 화면 예문, 비교 차트, 색 강조, 손짓 nuance.

### 검증

생성 후 보존 프레임의 핵심 **한글** OCR 문자열이 출력 .md에 반영됐는지 자동 점검한다. 누락 시 1회 재생성.

---

## 11. 시스템 프롬프트 / 사용자 입력 형식

### 시스템 프롬프트

`kor_yt_md_pipeline.py` 안에 korean 전용 프롬프트를 둔다. 내용:

- 본 `korean_yt_md_guide.md`의 작성 규칙 전체 (섹션 5, 6, 7, 8, 10)
- korean exemplary output 전문 (아래 섹션 15 참고)

tech 프롬프트를 이 스크립트에 넣지 않는다. 두 스크립트는 프롬프트를 공유하지 않는다.

### 사용자 입력 (영상 1개당)

```
[VIDEO METADATA]
Channel / Playlist / URL / Duration / Upload Date / Mapped Ji Lesson / Title

[TIMELINE]  ← AUDIO 트랙과 SCREEN(OCR) 트랙을 시간순으로 병합. 무음은 (무음)으로 명시.
[03:12–03:16] AUDIO: "...So just remember this."
[03:16–03:45] AUDIO: (무음)
  SCREEN: "1. With strangers or people you just met, you speak formal 존댓말 ..."
  SCREEN: "2. If you are not of age yet, you should speak formal 존댓말 to adults."
  SCREEN: "3. You speak casual 반말 with people who you personally know ..."
  ...

[KEY FRAMES]  ← 보존된 distinct 프레임 이미지 N장 (시간순 첨부). Gemini가 직접 봄.

[OCR ANCHORS]  ← 화면에서 추출한 한글 단어·표현 목록 (Whisper 철자 교정용 정답지)

[INSTRUCTION]
Generate the .md file per the system prompt. Output the .md content only, no preamble.
```

---

## 12. 중복 영상 처리 원칙

xlsx에서 동일 URL이 여러 레슨(Ji 레벨·레슨)에 매핑된 경우 (예: Level 8-11 / 8-12):

- **영상 시청·변환은 1회만.** 처음 만났을 때만 다운로드·Whisper·OCR·Gemini를 돌린다.
- 결과 .md를 **매핑된 레슨 수만큼 파일로 저장한다.** 파일명의 레벨-레슨 부분만 다르고 내용은 동일하다.
  - `kor_08-11_Go Billy_..._260830.md`
  - `kor_08-12_Go Billy_..._260830.md`
  - 각 파일의 Metadata `Mapped Ji Lesson` 값은 해당 레슨으로 맞춰 쓴다.
- 평면 저장이므로 Ji는 각 파일을 그대로 해당 레슨 폴더로 옮기면 된다.
- xlsx 상 해당 행 전부 md보유여부를 O로 갱신한다.

---

## 13. 완성 파일 체크리스트

- [ ] Metadata: 불릿 리스트 형식 (테이블 아님), `Mapped Ji Lesson`·`변환일` 포함
- [ ] Teaching Points: `### Overview` 섹션 포함
- [ ] 섹션명: 번호 없음, 설명적 제목
- [ ] 본문: 산문 서술체
- [ ] 한국어 예문: 블록 인용 또는 인라인, 영어 해석 포함
- [ ] Frame 시각 정보: Teaching Points에 통합
- [ ] Transcript: 섹션 존재, 전체 발화 포함, Note 줄 포함
- [ ] Romanization: 없음
- [ ] Over-summarize: 없음
- [ ] 파일명: `kor_레벨-레슨_채널_영상제목_변환일.md`, 레벨·레슨 두 자리, 금지문자 치환 완료
- [ ] 저장 위치: `01_inbox\` 평면

---

## 14. 작업 진입 순서

### 1단계: 스크립트 이름 변경 (완료 2026-08-30)

```
yt_to_md_pipeline_v2.py  →  kor_yt_md_pipeline.py
```

같은 날 아래도 함께 처리됐다.
- docstring·사용법 안내의 구 파일명 교체
- `_detect_base_dir()`이 vault 루트를 못 찾던 버그 수정.
  스크립트가 `_vault_setup\01_md_convert\_scripts\`로 세 단계 깊이 옮겨졌는데
  코드는 여전히 한 단계 위를 루트로 보고 있었다 → `parents[3]`으로 교정.

### 2단계: `kor_yt_md_pipeline.py` 수정 (미완)

BASE_DIR은 고쳐졌지만 그 아래 경로 상수들이 아직 폐기된 구조를 가리킨다.
현재 상태로 실행하면 입력 xlsx부터 못 찾는다.

1. **BASE_DIR**: 스크립트 위치(`_vault_setup\01_md_convert\_scripts\`) 기준으로 vault 루트를 재계산.
2. **입력 경로**: `_vault_setup\01_md_convert\korean_yt_md_convert.xlsx` 직접 파싱.
   (구 `01_Raw\00_Curriculum_and_index\02_yt_md_convert.xlsx` 경로 폐기. 커리큘럼맵 .md 표 파싱 방식도 폐기됨.)
3. **출력 경로**: `01_inbox\` 고정. **레벨·레슨 폴더 글롭 매칭 로직 전체 삭제.**
4. **파일명 생성**: `kor_레벨-레슨_채널_영상제목_변환일.md`. 레벨·레슨 0 채우기, 금지문자 치환 함수 추가.
5. **중복 영상**: 레슨 폴더 복사 로직을 삭제하고, 매핑 수만큼 파일명만 바꿔 저장하는 방식으로 교체.
6. **xlsx 갱신**: 성공 X→O, 실패 X→F 후 저장.
7. **경로 상수**: GEN_DIR = `_scripts\claude_gen\`, FAILED_MD_DIR = `01_inbox\convert_fail\`.
   (구 `02 Obsidian` 경로, vault 루트 `04_convert_fail\` 경로는 존재하지 않는다.)

`--track` 같은 트랙 분기 플래그는 넣지 않는다. 이 스크립트는 korean 전용이다.

### 3단계: 시범 변환 후 전체 실행

`--limit 2`로 영상 2개 → exemplary와 1:1 비교, 프롬프트 튜닝 → 검증 통과 시 나머지 실행. manifest로 재개 지원.

```
python kor_yt_md_pipeline.py --dry-run    # 작업 목록만 (API 호출 없음)
python kor_yt_md_pipeline.py --limit 2    # 시범 2개
python kor_yt_md_pipeline.py              # 전체(X 상태) 일괄
python kor_yt_md_pipeline.py --level 1    # 특정 레벨만
python kor_yt_md_pipeline.py --turbo      # Whisper large-v3-turbo (속도 우선)
```

---

## 15. 참고 경로

| 항목 | 경로 |
|---|---|
| vault 루트 | `C:\vault\Koreanwithji_vault\` |
| 변환 대상 xlsx | `_vault_setup\01_md_convert\korean_yt_md_convert.xlsx` |
| 코드 | `_vault_setup\01_md_convert\_scripts\kor_yt_md_pipeline.py` |
| 출력 | `01_inbox\` |
| 검증 실패 보관 | `01_inbox\convert_fail\` |
| 로그·재개 manifest | `_vault_setup\01_md_convert\_scripts\claude_gen\` |
| Korean exemplary output | `02_course_creation\01_raw\01_by_level_lesson\Level_1\4_Yes_No\02_yt_md\Your Korean Saem_A Full Korean Conversation Just With 네!.md` |
| Ji가 분류해 넣을 최종 위치 | `02_course_creation\01_raw\01_by_level_lesson\Level_{n}\{레슨}_*\02_yt_md\` |
