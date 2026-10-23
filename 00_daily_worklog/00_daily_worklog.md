# 00_daily_worklog 인덱스

> 이 폴더는 **날짜별 작업 로그를 저장하고, 과거 작업을 빠르고 정확하게 추적하기 위한 색인**이다.
> Ji가 하루 마감을 요청했을 때 이 파일의 인덱스 표와 해당 날짜 로그를 함께 갱신한다.
> 최종 갱신: 2026-10-22 (audit 실행 결과와 기록 위치 반영)

---

## 폴더 구조

```
00_daily_worklog\
├─ 00_daily_worklog.md      ← 이 파일. 폴더 인덱스 + 날짜별 작업 요약 표
├─ YYMMDD_log\
│   └─ YYMMDD_log.md
└─ (이후 YYMMDD_log 폴더가 하루 단위로 계속 추가됨)
```

---

## 각 항목의 역할

| 항목 | 역할 |
|---|---|
| `00_daily_worklog.md` | 이 폴더의 인덱스. 날짜별 로그로 가는 링크와, 각 로그의 작업 항목을 한 줄씩 요약한 표를 담는다 |
| `YYMMDD_log\YYMMDD_log.md` | 해당 날짜의 작업 로그 원본. 그날 있었던 작업을 항목별로 정리한다 |
| [`01_inbox\conversation_log\conversation_log.md`](../01_inbox/conversation_log/conversation_log.md) | 작업 중 Ji와 에이전트가 주고받은 요청·답변을 실시간으로 남기는 곳. 하루가 끝나면 이 내용을 근거로 YYMMDD_log.md 파일을 갱신한다 |

---

## 활용 방식

1. 작업 중에는 [`01_inbox\conversation_log\conversation_log.md`](../01_inbox/conversation_log/conversation_log.md)에 요청·답변을 실시간으로 남긴다.
2. Ji가 하루 마감을 요청하면 그 내용을 바탕으로 `YYMMDD_log\YYMMDD_log.md`를 작성한다.
3. 동시에 이 파일의 인덱스 표에도 해당 날짜의 행을 추가한다.
4. 시간이 흐른 뒤에도 AI가 과거 특정 일일 노트를 추적하여 "정확히 언제, 어떤 방식으로 작업을 시작하고 수행했는지" 빠르고 세밀하게 찾아낼 수 있게 한다.

---

## 인덱스

날짜 칸은 해당 날짜 로그로 연결된다. 한 행은 그날 작업 전체를 요약한다. 시간별 상세 작업은 각 날짜의 `YYMMDD_log.md`에서 확인한다.

| 날짜 | 목적 | 처리결과 | 비고 |
|---|---|---|---|
| [260830](260830_log/260830_log.md) | 유튜브 영상 → .md 변환 작업의 korean/tech 투트랙 설계: 스크립트·규칙서 완전 분리 결정, 두 트랙 가이드 작성·현행화, `_vault_setup` 폴더 인덱스 작성 | 완료 | vault 루트 경로 계산 버그 발견·수정. tech 스크립트 신규 작성은 미완으로 남김 |
| [260831](260831_log/260831_log.md) | tech_yt_md_pipeline.py 신규 작성·검증, 출력 폴더 구조 개편(convert_O/convert_F), 실제 배치 변환 11건 실행 | 완료 (일부 대기) | O=9 F=2, 누적 비용 $0.368(약 496원). tech xlsx 행 수 불일치·exemplary 미확정 항목 남음 |
| [260901](260901_log/260901_log.md) | 260831 밤부터 돌아가던 tech 배치 변환(row 5, 8~12)이 새벽에 끝나는 것을 확인 | 완료 | 새 작업 지시 없음. 지연 원인(긴 영상 + GPU 순차 처리)만 확인, 결과는 260831 배치에 포함된 수치와 동일 |
| [260902](260902_log/260902_log.md) | 에이전트 지침 체계 전체 재구축: vault 운영 지침서(CLAUDE.md)와 각 폴더별 index 작성. 문서를 index와 본문으로 분리해 Single Source of Truth 확립 | **초안 완성 (미확정)** | 신설 3개 + 재작성 8개. CLAUDE.md는 `03_tech/01_CLAUDE.md` 지침 6개를 종합해 172줄로 작성. 전부 Ji 검토 대기 상태이며 확정된 것이 아니다. [`02_course_creation.md`](../02_product/02_course_creation/02_course_creation.md)와 SKILL.md는 미착수 |
| [260903](260903_log/260903_log.md) | hook 자동화·skill 5종 설치로 지침 체계 마무리, `01_raw` 대청소(빈 폴더 275개·중복 Amira_Source 44개·orphan 2개 삭제), `02_course_creation` 생산 라인 전면 재설계(`brainstorm.md`·`work_plan.md`·`lesson_design_method.md` 신설), 예전 vault 유령 백링크(`concept_` 등) 446건 전량 제거 | 완료 (일부 Ji 결정 대기) | `01_raw` 최종 1,746개(`01_by_level_lesson` 1,727개), 빈 폴더·깨진 링크 0건. `brainstorm.md` 결정 5건(DP-2~DP-6)이 남아야 STEP 3 이후 진행 가능 |
| [260904](260904_log/260904_log.md) | 미조치 항목 정리(CLAUDE.md 하드룰·SKILL.md 2종), STEP 1 미정사항 12건(DP-3~DP-12) 전건 결정 확정, `02_course_creation` 문서 3분할 재구성(`glossary.md`·`course_plan.md` 신설, `brainstorm.md` 재작성, index 221→61줄) | 완료 (Ji 판단 4건 대기) | 실측으로 레슨 폴더 196개·빈 폴더 0개 확정(이전 보고 194는 Windows 경로 끝 `...` 문제). 새 gotcha 발견: raw의 `Mapped Ji Lesson`이 구 커리큘럼 번호(848개 파일). `02_lesson_spec/` 신설했으나 아직 빈 폴더 |
| [260907](260907_log/260907_log.md) | 260904 로그·인덱스 갱신, raw `Mapped Ji Lesson` 구 번호 848건 삭제(하드룰 3 예외 적용, Ji 컨펌), `brainstorm.md` Q1~Q3 결정 반영(RAW_DIGEST 존치+Transcript 제외, 하드룰 6·트랙 밖 파일 Ji 직접 처리) | 완료 | 삭제는 raw가 git 미추적이라 diff로 안 잡힘. 로그 자체가 그날 0바이트로 남아 2026-09-13에 소급 작성 |
| [260908](260908_log/260908_log.md) | vault 전체를 실측 기반으로 훑어 `to_do.md` 신설(117줄) | 완료 | 문서-실제 불일치 3건 발견(Ji_draft 보유 39개, 파일럿 빈칸 0개, work_plan.md 이동 이미 완료). git 미추적 리스크를 처음 리스크로 올림. 로그는 2026-09-14 소급 작성 |
| [260910](260910_log/260910_log.md) | `to_do.md`를 index·라우팅 체계에 정식 편입(6개 파일 수정), 작성 요령 8개 항목 신설 | 완료 | 하드룰 1 충돌(수시 업데이트 vs 확인 필요)을 "세션 끝 1회"로 해소. CLAUDE.md 196줄 준수. 로그는 2026-09-14 소급 작성 |
| [260911](260911_log/260911_log.md) | Fable 세션용 vault 점검 + L2-01 관통 테스트 prompt 계획 수립(점검 3개+테스트 7개) | 완료 (계획만, 실행 대기) | 점검으로 심각 2건(git 미추적, `kor_yt_md_pipeline.py` 실행 시 죽음) + 문서 정합성 8건 발견. vault 파일 변경 없음. Ji 결정 대기 6건(Q-A~Q-F). 로그는 2026-09-14 소급 작성 |
| [260913](260913_log/260913_log.md) | `course_plan.md`를 강의 제작 계획의 유일한 출처로 재편(`brainstorm.md` 내용 흡수, 244→472줄), 문서 구조를 3층에서 outline·draft 분리한 4층으로 개정. STEP 순서 재편(재료 모으기 → 개념 indexing+`topic_shaped` 병행 → Schema+`spec_done` → OUTLINE/DRAFT → 확장, STEP 1~5를 1~6으로) | 완료 (`to_do.md` 동기화 대기) | `to_do.md`가 옛 STEP 순서 그대로라 새 계획과 어긋난 채 하루 마감. 남은 결정은 J-1(spec 작성 전 git 정리 여부) 하나. 실 산출물은 여전히 0장 |
| [260914](260914_log/260914_log.md) | `to_do.md`를 STEP 2 재료 모으기 기준으로 재작성하고, 누락된 260908·260910·260911 날짜 로그를 소급 작성. 2026-09-04~13 conversation 기록 18건을 날짜 로그로 이관·정리 | 완료 | J-1(Git 정리)은 당시 대기였으나 2026-09-15 GitHub 첫 백업으로 완료. 변환 파이프라인 보류 2건만 conversation_log에 남김 |
| [260915](260915_log/260915_log.md) | GitHub 첫 백업, lesson_spec 생산라인 재설계, 5종 index 파일별 Ref_No 정비, tracking 구성, 파일럿 기준 확정 | 완료 | `01_by_level_lesson` 1,706개 파일 등록. 파일럿은 44개 레슨·533개 raw 파일이며 VSL·Intro는 제외. 다음은 Ref_No frontmatter 반영과 개념 조사 |
| [260916](260916_log/260916_log.md) | Ref_No 최종 대조·raw frontmatter 반영, 파일럿 개념 전수조사용 `01_concept_index.xlsx` 빈 구조 생성 | 완료 | 1,706개 Markdown의 Ref_No 확인·반영 완료. 다음은 44개 레슨·533개 raw 파일의 개념 조사와 Ji 범위 검수 |
| [260917](260917_log/260917_log.md) | 개념 조사·`range_set` 규칙 정비, Hangul 외부자료 4개를 레슨별 복사본·Ref_No 기준으로 편입 | 완료 | `01_by_level_lesson` 1,711개, 파일럿 538개로 갱신. Hangul 1·3·4·6의 `06_ext_sources` 복사본 4개는 별도 index·tracking 시트에서 관리 |
| [260918](260918_log/260918_log.md) | `Ji-1-6-1` 매핑 보완, `pre-concept` push, 개념 정의·등록 규칙 교정, Hangul 1 매핑 자료 전체 재조사 | 검토용 결과 완료, 확인 8건 대기 | Hangul 1 자료 17개 검토. 개념 31개·근거 82개·이름 근거 42개 기록. 레슨 범위는 미확정 |
| [260923](260923_log/260923_log.md) | concept index 제외 workflow 적용, 중복 자료 선별표 구축, DMS-0001~0010 샘플 발췌 | 완료, Ji 검토 대기 | 중복 후보 266묶음·888개 사본. DMS-0001은 Ji 작성, DMS-0002~0010 39행 Agent 제안 완료. JSON 구조는 xlsx 검토 뒤 결정 |
| [260925](260925_log/260925_log.md) | `course_plan_update.md` 기준 작업지시서·tracking 갱신, 기존 계획·backup archive 이동, DMS-0001~0010 선별표 표현 정리 | 완료, Ji 검토 대기 | concept index는 제외. 확정된 레슨만 `range_set`으로 진행. `course_plan.md`와 tracking backup 2개는 `_archive`에 보관 |
| [260926](260926_log/260926_log.md) | 영상 중심 `range_set` 기준으로 코스 계획 통합, DMS를 중복 매핑 확인용으로 변경, 44개 파일럿 레슨에 검토 카드·Ref_No 구간표 적용 | 검토 초안 완료 | 538개 Ref_No·993개 구간 후보. 사용 후보 422·보류 78·제외 후보 38. 원문 내용 적합성·Ji 경계 검토 전이라 44개 status는 `raw_mapped` |
| [260927](260927_log/260927_log.md) | 44개 `range_set` 카드의 raw 링크·Ji 질문·전체 매핑 근거 정비, Hangul 피드백 확인과 Hangul-5 `topic_raw` 시범 | Hangul-5 시범 완료, 나머지 검증 진행 중 | 마감 시 538개 Ref_No·930개 구간. 44개 중 Hangul-5만 `topic_raw`. Hangul-6 피드백 확인 대기 |
| [260928](260928_log/260928_log.md) | Hangul 1~4·6 `topic_raw`, 출처별 설명 보존 규칙과 skill 2종 정리, Numbers 1~7·Level 1·2 자료 판정 | Hangul 6개 `topic_raw` 완료, 38개 레슨 잠정 판정·Ji 경계 검토 대기 | 파일럿 44개, Ref_No 539개, 선택 구간 714곳. Numbers-6·Level 2-8 자료 부족과 Hangul-4 발음 충돌 검토 필요 |
| [260929](260929_log/260929_log.md) | Numbers 피드백 반영 준비와 Hangul `topic_shaped` 방법 설명 | Ji 요청으로 Numbers 작업 중단. 산출물 수정 없음 | Numbers 피드백 7개와 기존 자료를 읽은 단계에서 중단 |
| [260930](260930_log/260930_log.md) | Raw 이동·복사 6건 정본 반영, Hangul·Numbers 원문 발췌 갱신, Level 3~12의 1차 `range_set` | 9개 레슨 발췌 갱신으로 `topic_raw` 전체 12개. Level 3~12 카드 149개는 잠정 판정 | 전체 카드 193개·Ref_No 1,677개. Numbers-6 근거 보강, Level 1~12 경계 검토 대기 |
| [261001](261001_log/261001_log.md) | `topic_shaped` 계획과 산출물 형식 문서화, 9월 29·30일 작업 마감 | 완료 | 당시 `topic_raw` 완료 레슨만 다음 단계로 넘기는 기준을 세움 |
| [261003](261003_log/261003_log.md) | Level 1-1~4 피드백 반영과 `topic_raw` 원문 발췌, 1-5 피드백 확인 | 1-1~1-4 완료. 전체 `topic_raw` 16개, `raw_mapped` 180개 | 1-5의 YT-1-5-2 `60~52줄` 확인 대기 |
| [261007](261007_log/261007_log.md) | vault 내부 Superpowers·Taskmaster 준비, Level 1-5~1-11 `topic_raw`, Draft까지의 제작 과정 검토 | 1-5~1-11 완료. 전체 `topic_raw` 23개, `raw_mapped` 173개. 개선 계획은 채팅 제안 | Ji의 지정에 따라 10월 8일 새벽 작업 포함. 보고서 파일과 정식 `topic_shaped` 산출물은 아직 없음 |
| [261009](261009_log/261009_log.md) | `range_set_review.xlsx`에 193개 카드의 구간별 2,595행 반영, Ji feedback 대조, Numbers-6 범위 확인 | 일부 확인 대기 | Numbers-6 판정 이유 1셀 쓰기 실패와 부수 파일 삭제 미완을 기록 |
| [261012](261012_log/261012_log.md) | Level 1-12 `topic_raw` 작성 및 `range_set-1-12` branch 백업 | 완료 | 처음의 tag 해석을 branch로 바로잡아 push |
| [261013](261013_log/261013_log.md) | range_set 검토 정본을 단일 workbook으로 정리, 1-1 단일 파일럿 지시서 수정, Ref_No 원문 링크 반영 | 완료 | 이전 44개 파일럿 범위가 당시 `course_plan.md`에 남아 있었음 |
| [261014](261014_log/261014_log.md) | CLEAR·4MAT 교수 설계 기준 개정, 1-1 `topic_shaped` 작성 및 원문 줄 링크 적용 | 완료, Ji 검토 대기 | 출처 간 용어·조건 차이는 OPEN으로 유지 |
| [261015](261015_log/261015_log.md) | 1-1 `lesson_spec`·OUTLINE·DRAFT 작성, 교육·소통 검토 후 수정, 대사 스킬 교체 | 초안·수정 완료, Ji 검수 대기 | 실제 낭독과 학습 효과는 미확인 |
| [261016](261016_log/261016_log.md) | 1-1 Word Draft 후반부 CLEAR·4MAT 식별과 원본 보존 주석 사본 작성 | 주석 사본 완료 | 문법 정확성·최종 샘플 채택은 검증하지 않음 |
| [261019](261019_log/261019_log.md) | 코스 제작 지침을 다섯 단계로 통합하고 1-3 OUTLINE·대사 초안 작성 | 문서·초안 완료, Ji 낭독 대기 | 이전 절차 239개 파일 보관, BEATS 미작성 |
| [261020](261020_log/261020_log.md) | Teaching 두 영상 변환, Ji Shorts 24편 받아쓰기, Transcript 줄 대조와 코스 지시서 정리 | 변환·기록 완료, 내용 검수 대기 | Python 3.12 가상환경 생성 실패, Transcript 4행은 `확인 필요` |
| [261021](261021_log/261021_log.md) | 4MAT·CLEAR 지침 반영, Level 1 대사 v2·1-4 v3 작성, Ji Draft 출처·Intro 조사 | 산출물 작성, Ji 검수 대기 | 레슨별 학습 범위 분리 계획은 승인 대기 |
| [261022](261022_log/261022_log.md) | `pre-audit-1022` push 추진 과정과 workspace AI 설정 감사·보관 정리 | 보관 정리 실행. 추가 기록은 대화 로그에 있음 | [최신 실행 기록](../01_inbox/conversation_log/conversation_log.md) · [감사 보관소](../_archive/_archive.md). GitHub 반영 최종 확인은 미기록 |

<!-- codex-day-close:260918 -->

<!-- codex-day-close:01a0d6c0-dc8c-71e3-a91a-b36be92da50e -->

<!-- codex-day-close:01a0dc8b-eb6a-7d90-9e8a-157345254efc -->

<!-- codex-day-close:01a0dea0-b071-7222-9446-de4c5111d9fe -->
<!-- codex-day-close:01a0e2d4-c935-7272-9b21-08844b544c3c -->

---

## 작업 시작 전 확인할 것

- 새 날짜 로그를 시작하기 전에 인덱스 표의 최근 행을 훑어 직전 작업 맥락을 파악한다.
- 상세 판단 근거나 코드 위치까지 필요하면 인덱스 표가 아니라 해당 `YYMMDD_log.md`를 연다.

<!-- codex-day-close:01a0e876-afd0-7c01-9e8b-52f0c68894f2 -->
<!-- codex-day-close:01a0f5d3-4063-74f2-bc37-ef7333a5f6e4 -->
<!-- codex-day-close:01a11030-1291-7230-abf7-b5f6e29b33e6 -->
<!-- codex-day-close:01a11a0c-08d3-74c0-926a-44daa1ed2fec -->
