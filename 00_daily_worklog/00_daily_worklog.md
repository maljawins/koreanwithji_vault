# 00_daily_worklog 인덱스

> 이 폴더는 **날짜별 작업 로그를 저장하고, 과거 작업을 빠르고 정확하게 추적하기 위한 색인**이다.
> 에이전트는 하루 작업을 마칠 때 이 파일의 인덱스 표와 해당 날짜 로그를 함께 갱신한다.
> 최종 갱신: 2026-09-15

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
| [`01_inbox\conversation_log\to_do.md`](../01_inbox/conversation_log/to_do.md) | 이 폴더가 **지나간 일**을 담는다면 그 파일은 **지금 할 일**을 담는다. 하루 마감 때 둘을 같이 갱신한다. 작성 요령은 [`01_inbox.md`](../01_inbox/01_inbox.md) |

---

## 활용 방식

1. 작업 중에는 [`01_inbox\conversation_log\conversation_log.md`](../01_inbox/conversation_log/conversation_log.md)에 요청·답변을 실시간으로 남긴다.
2. 하루 작업이 끝나면 그 내용을 바탕으로 `YYMMDD_log\YYMMDD_log.md`를 작성한다.
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

---

## 작업 시작 전 확인할 것

- 새 날짜 로그를 시작하기 전에 인덱스 표의 최근 행을 훑어 직전 작업 맥락을 파악한다.
- 상세 판단 근거나 코드 위치까지 필요하면 인덱스 표가 아니라 해당 `YYMMDD_log.md`를 연다.
