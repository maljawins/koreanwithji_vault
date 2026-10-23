# 01_inbox 인덱스

> 이 폴더는 **Ji와 에이전트 사이의 완충 지대**다. 자료가 최종 위치로 가기 전, 결과물이 승인되기 전에 잠시 머무는 곳이다.
> 동시에 **메모리 관리 시스템의 출발점**이다. 모든 작업 기록은 여기서 시작해 `00_daily_worklog`로 넘어간다.
> 최종 갱신: 2026-10-22

---

## 폴더 구조

```
01_inbox\
├─ 01_inbox.md              ← 이 파일. 폴더 인덱스
└─ conversation_log\
    └─ conversation_log.md  ← 작업 중 실시간 대화 기록 (메모리의 출발점)
```

---

## 각 항목의 역할

| 항목 | 역할 |
|---|---|
| [`conversation_log.md`](conversation_log/conversation_log.md) | 에이전트가 **답변할 때마다 실시간으로** 요청과 이행 내용을 남기는 곳. 하루가 끝나면 이 내용이 그날의 worklog 근거가 된다 |

할 일과 개인 메모는 Ji가 vault 밖에서 직접 관리한다. 기존 `to_do.md`와 `prompt.md`는 삭제되었으며 에이전트가 다시 만들거나 관리하지 않는다.

업무 기억의 관리 기준은 [AGENTS.md](../AGENTS.md), 날짜별 과거 기록은 [00_daily_worklog index](../00_daily_worklog/00_daily_worklog.md), audit 보관 자료는 [_archive index](../_archive/_archive.md)에서 확인한다.

---

## conversation_log.md 작성 규칙

에이전트가 답변할 때마다 실시간으로 append한다. 항목마다 아래 4가지를 남긴다.

1. **대화 날짜와 시간** (`#YYMMDD_HH:MM` 형식)
2. **Ji가 무엇을 시켰는지**
3. **에이전트가 그 요청을 어떻게 이해했는지**
4. **에이전트가 그것을 어떻게 이행했는지**

작성 문체는 [`.agents/skills/get-to-the-point-skill/SKILL.md`](../.agents/skills/get-to-the-point-skill/SKILL.md)의 원칙을 따른다. 결론 먼저, 군더더기 없이.

**중요**: 이 내용을 `00_daily_worklog`로 옮기는 것은 **Ji가 요청할 때만** 한다. 하루 1회, 그날 작업이 끝날 때다. 에이전트가 스스로 판단해서 옮기지 않는다.

---

## 하루 마감 절차

Ji가 하루 마감을 명시했을 때만 다음을 수행한다.

1. `conversation_log.md`에서 해당 날짜의 요청·이행·미완료 사항을 확인한다.
2. `00_daily_worklog/YYMMDD_log/YYMMDD_log.md`에 근거가 확인된 내용을 정리하고 날짜별 index에 연결한다. 기존 기록과 Ji의 검수 상태를 보존한다.
3. 기록 확인 장치가 turn ID를 전달했다면 날짜 로그와 index에 각각 `<!-- codex-day-close:TURN_ID -->`를 남긴다. 이 표시는 마감 완료 확인용이다.
4. 경로·수치·중복을 검증한 뒤, 날짜 로그로 옮긴 항목만 `conversation_log.md`에서 정리한다.

---

## Drop-off Zone 역할

Ji가 에이전트에게 읽히고 싶은 새 자료를 임시로 넣는 곳이기도 하다. 여기 들어온 파일은 아직 분류되지 않은 상태이므로, 에이전트는 그것을 어디로 보낼지 **먼저 Ji에게 확인한 뒤** 옮긴다. 이렇게 해야 vault 구조가 처음부터 지저분해지지 않는다.

---

## 작업 시작 전 확인할 것

- 코스 제작 요청은 [코스 제작 지도](../02_product/02_course_creation/02_course_creation.md)의 해당 단계부터 연다. 관련 과거 판단이 필요할 때 작업 기록의 해당 부분만 찾는다.
- 그 밖의 작업은 세션을 시작하면 [`conversation_log.md`](conversation_log/conversation_log.md)와 최근 `YYMMDD_log.md`의 항목을 훑어 직전 맥락을 잡는다.
- 더 앞선 맥락이 필요하면 [`00_daily_worklog/00_daily_worklog.md`](../00_daily_worklog/00_daily_worklog.md)의 인덱스 표를 본다.
- 이 폴더의 파일은 임시다. 여기 있는 내용을 다른 문서의 근거로 삼지 않는다.
- 단 `conversation_log.md`는 임시 파일이 아니라 작업 기억을 관리하는 상시 구성 요소다.
