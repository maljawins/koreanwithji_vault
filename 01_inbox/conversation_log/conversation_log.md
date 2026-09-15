# conversation_log

> 작업 중 Ji와 에이전트가 주고받은 요청·답변을 실시간으로 남기는 곳.
> **날짜별 로그로 옮긴 항목은 여기서 지운다.** 이 파일에는 아직 처리되지 않은 것만 남는다.
> 지난 작업 내역은 `00_daily_worklog/YYMMDD_log/YYMMDD_log.md`에서 본다.
> 최종 정리: 2026-09-15

---

## 실시간 기록

### 2026-09-15 — vault 첫 GitHub 백업

- **Ji가 시킨 것**: 현재 상태의 vault를 `https://github.com/maljawins/koreanwithji_vault`에 첫 백업.
- **이해**: 기존 `vault_renew` Git 기록은 현재 vault 구조와 다르므로 보존만 하고, 현재 작업 트리를 별도 첫 snapshot으로 commit하여 Ji가 지정한 새 GitHub 저장소에 올린다. `.env`와 `cookies.txt`는 민감 정보이므로 commit에서 제외한다.
- **이행**: 완료. 기존 `vault_renew` 기록과 분리된 `main` 첫 snapshot(commit `2b44220`)을 만들고 `https://github.com/maljawins/koreanwithji_vault`에 push했다. 1,887개 파일을 포함했고 `.env`와 `cookies.txt`는 제외했다. GitHub는 57.09MB PDF 1개에 대해 권장 크기(50MB) 초과 경고를 냈으나, 100MB 제한 이하여서 push는 성공했다.

(2026-09-03까지는 [`260903_log.md`](../../00_daily_worklog/260903_log/260903_log.md)로, 2026-09-04~2026-09-13 전체는 [`00_daily_worklog.md`](../../00_daily_worklog/00_daily_worklog.md) 인덱스의 해당 날짜 로그로 옮겨졌다. 새 작업부터 여기 기록한다.)

### 2026-09-15 11:04 — Codex 기록 hook 재구축

- **Ji가 시킨 것**: 사라진 `conversation_log.md`·`daily_worklog` 자동 업데이트 hook을 Codex 환경에서 구현하고, 구현 로직을 한 페이지로 설명해 달라고 요청.
- **이해**: 매 응답 기록과 Ji가 명시한 하루 마감은 다른 주기이므로, 전자는 turn 종료 검사 hook으로, 후자는 명시 요청에서만 작동하는 Skill과 검사 hook으로 분리해야 함.
- **이행**: `.codex/hooks.json`과 `vault_logging.py`를 신설해 UserPromptSubmit·Stop event를 연결했다. `vault-day-close` Skill을 신설했고, `AGENTS.md`에 hook append 승인·plan mode 예외·하루 마감 승인 범위를 명시했다. Python 문법, hooks.json 형식, 일반 turn과 하루 마감 turn의 누락 차단 경로를 검증했다.
- **특이사항**: Windows 환경에서 `.codex` 안에 hook 실행 상태를 만들 수 없어, 상태는 vault 밖 Windows Temp 폴더에만 저장하도록 바꿨다. 검증용 임시 상태는 삭제했다.

<!-- codex-turn:manual-260915-1104 -->

### 2026-09-15 12:34 — Codex 전환과 코스 제작 작업장 정비

- **Ji가 시킨 것**: Claude Code를 Codex로 바꾼 현재 상태, 커리큘럼·Ji Draft index 컬럼 추가, `02_course_creation` 폴더 구조 변경, GitHub 백업 완료를 기록하고 관련 지침을 갱신. `RAW_DIGEST`의 정체와 `spec_done` 이후 보존 여부도 설명.
- **이해**: 실제 폴더와 xlsx를 정본으로 확인한 뒤, 현재 운영 문서의 이전 경로·도구명·Ref_No 규칙을 맞춘다. 과거 작업 로그와 Claude 관련 참고자료는 역사 기록이므로 고치지 않는다.
- **이행**: `AGENTS.md`의 레슨 설계 경로를 실제 위치로 고쳤다. `master_index.md`, `01_inbox.md`, 사업 기획서, course creation index·plan·용어·기술 스택·outline/draft index, vault setup index를 Codex와 새 폴더 구조로 갱신했다. `course_plan.md`에는 `01_lesson_spec/01_topic_copy → 02_topic_raw → 03_topic_shaped → spec_done` 흐름과 `02_concept/concept_index.xlsx` 위치를 기록했고, Ji Draft도 Ref_No와 경로를 함께 쓰도록 DP-10을 개정했다. RAW_DIGEST는 `Ref_No · 파일명 · 섹션 제목 · 원문 발췌`만 남기는 근거 장부로 `spec_done`에도 보존하기로 확정했다.
- **특이사항**: 커리큘럼 맵 첫 행에는 `Draft 보유여부`, `01_Ji_Draft_index.xlsx` 첫 행에는 `Ref_No`와 `Draft 보유여부`가 실제로 있다. `to_do.md`는 세션 마감 때만 갱신하는 규칙에 따라 이번 작업에서는 고치지 않았다.

<!-- codex-turn:manual-260915-1234 -->

### 2026-09-15 12:36 — `spec_done` 완료본 저장 폴더 지정

- **Ji가 시킨 것**: `01_lesson_spec/04_spec_done/` 신설을 반영하고, 완료된 `spec_done` 파일을 상위 `01_lesson_spec/` 바로 아래에 두는 이전 설명을 고침.
- **이해 및 이행**: 새 폴더 존재를 확인한 뒤 `02_course_creation.md`와 `course_plan.md`의 폴더 지도, 단계 흐름, 현황, STEP 4 산출물, DP-11을 모두 `04_spec_done/` 저장으로 통일했다.

<!-- codex-turn:manual-260915-1236 -->

### 2026-09-15 12:40 — 2026-09-14 일일 로그 마감

- **Ji가 시킨 것**: `260914_log.md`와 `00_daily_worklog.md`를 작성하고, `conversation_log.md`의 2026-09-14 작업 기록을 날짜 로그로 이관.
- **이해 및 이행**: `vault-day-close` 절차로 9월 14일 항목만 근거로 날짜 로그를 작성하고, 인덱스에 행을 추가한 뒤 원문을 conversation log에서 삭제했다. 현재 `to_do.md`는 GitHub 백업 완료를 반영해 Git 대기 항목을 제거하고 STEP 2 작업 3개만 남겼다.

<!-- codex-turn:manual-260915-1240 -->

---

## 미조치 항목

### 변환 파이프라인 (260830~260831 작업의 잔여분)

| 항목 | 상태 | 다음 행동 |
|---|---|---|
| `monitor_server.py` 경로 정비 | 보류 (260904, Ji) | 260830에 발견된 항목. **추후 변환 작업할 일이 있을 때 손볼 예정** |
| korean 스크립트 경로 상수 정비 | 보류 (260904, Ji) | `XLSX_PATH` 등을 현재 폴더 구조로 교체 필요. **추후 변환 작업할 일이 있을 때 손볼 예정** (korean xlsx는 전 행 O로 대상 0개라 급하지 않음). `kor_yt_md_pipeline.py`의 죽은 `01_Raw` 경로는 [`course_plan.md`](../../02_product/02_course_creation/course_plan.md) L-4로 이미 이관됨 |

---

## 정리 이력

- **2026-09-02**: 260830~260902 대화 기록 전체를 각 날짜 로그로 옮기고 이 파일에서 삭제. 미조치 항목만 남김.
- **2026-09-03**: 260903 하루치 대화 기록 전체(지침 체계 마무리·`01_raw` 대청소·`02_course_creation` 재설계·유령 백링크 정리)를 [`260903_log.md`](../../00_daily_worklog/260903_log/260903_log.md)로 옮기고 이 파일에서 삭제. 미조치 항목 갱신(tech exemplary 완료 처리, 신규 미해결 2건 추가).
- **2026-09-14**: 2026-09-04~2026-09-13 대화 기록 전체(18개 항목)를 날짜별 로그([260904](../../00_daily_worklog/260904_log/260904_log.md)·[260907](../../00_daily_worklog/260907_log/260907_log.md)·[260908](../../00_daily_worklog/260908_log/260908_log.md)·[260910](../../00_daily_worklog/260910_log/260910_log.md)·[260911](../../00_daily_worklog/260911_log/260911_log.md)·[260913](../../00_daily_worklog/260913_log/260913_log.md), 260908·260910·260911은 이날 소급 작성)로 옮기고 이 파일에서 삭제. 미조치 항목 정리: 완료 확인된 11건 제거(CLAUDE.md 하드룰 6·§10 경로 불일치, gotcha 미기재 결정, SKILL.md 정리, `work_plan.md` 이동, 용어표 `승격` 삭제, temp 파일 삭제, tech exemplary 확정 등 — 근거는 옮긴 날짜 로그에 있음), 낡은 항목 2건 제거(`brainstorm.md` 결정사항·`02_lesson_spec` 착수는 `course_plan.md`/`to_do.md`가 이관 관리), 미해결 3건만 유지.
- **2026-09-15**: 2026-09-14 대화 기록을 [`260914_log.md`](../../00_daily_worklog/260914_log/260914_log.md)로 이관하고 이 파일에서 삭제. GitHub 첫 백업 완료에 따라 `to_do.md`의 Git 결정·실행 항목을 제거하고, STEP 2 실행 항목을 3개로 정리.
