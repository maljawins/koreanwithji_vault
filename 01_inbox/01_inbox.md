# 01_inbox 인덱스

> 이 폴더는 **Ji와 에이전트 사이의 완충 지대**다. 자료가 최종 위치로 가기 전, 결과물이 승인되기 전에 잠시 머무는 곳이다.
> 동시에 **메모리 관리 시스템의 출발점**이다. 모든 작업 기록은 여기서 시작해 `00_daily_worklog`로 넘어간다.
> 최종 갱신: 2026-09-15

---

## 폴더 구조

```
01_inbox\
├─ 01_inbox.md              ← 이 파일. 폴더 인덱스
└─ conversation_log\
    ├─ conversation_log.md  ← 작업 중 실시간 대화 기록 (메모리의 출발점)
    ├─ to_do.md             ← 지금 할 일 (worklog의 반대편)
    └─ prompt.md            ← Ji의 프롬프트 메모장
```

---

## 각 항목의 역할

| 항목 | 역할 |
|---|---|
| [`conversation_log.md`](conversation_log/conversation_log.md) | 에이전트가 **답변할 때마다 실시간으로** 요청과 이행 내용을 남기는 곳. 하루가 끝나면 이 내용이 그날의 worklog 근거가 된다 |
| [`to_do.md`](conversation_log/to_do.md) | `00_daily_worklog`가 **지나간 일**의 기록이라면 이 파일은 **지금 할 일**의 목록이다. 세션을 시작한 에이전트가 다음 행동을 여기서 잡는다. 전체 로드맵은 `course_plan.md` |
| [`prompt.md`](conversation_log/prompt.md) | Ji가 지시를 미리 적어두는 개인 메모장. 에이전트가 임의로 고치지 않는다. 맥락 파악용 참조 대상이 아니다 |

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

## to_do.md 작성 요령

[`to_do.md`](conversation_log/to_do.md)를 쓰거나 고칠 때 지키는 규칙이다.

1. **"지금" 할 것만 쓴다.** 지금 착수한 STEP의 할 일과 그걸 막고 있는 Ji 결정만 담는다. 나중 STEP, 뒤로 미룬 것, 전체 로드맵은 [`course_plan.md`](../02_product/02_course_creation/course_plan.md) §3-2 미실시 사항에 둔다.
2. **큰 그림 먼저, 디테일 나중.** 맨 위에 현재 위치와 "지금 할 일"의 흐름 한 줄을 두고, 그 아래에 상세 표를 둔다.
3. **지금은 course creation이 축이다.** 코스 제작과 직접 이어지는 일만 쓴다.
4. **항목마다 완료 조건을 쓴다.** "무엇이 되면 끝인가"가 없는 줄은 넣지 않는다.
5. **Ji 결정 대기 항목은 맨 앞에 둔다.** 에이전트가 혼자 못 넘어가는 지점이다.
6. **수치는 실측한다.** 기억이나 다른 문서에서 베끼지 않는다 ([AGENTS.md](../AGENTS.md) §7).
7. **규칙과 근거는 쓰지 않는다.** to_do는 "무엇을 지금"만 담고, 규칙과 근거는 `course_plan.md`를 가리킨다.
8. **끝난 항목은 `course_plan.md` §3-1 실시 사항으로 옮기고 to_do에서 뺀다.** 비워진 자리는 §3-2 미실시 사항에서 다음 것을 가져와 채운다.

**갱신 시점: 세션 마감 시 1회.** Ji가 마감을 지시하면 `conversation_log.md`를 근거로 `YYMMDD_log.md`와 `to_do.md`를 같이 갱신한다. 작업 도중에는 건드리지 않는다.

---

## Drop-off Zone 역할

Ji가 에이전트에게 읽히고 싶은 새 자료를 임시로 넣는 곳이기도 하다. 여기 들어온 파일은 아직 분류되지 않은 상태이므로, 에이전트는 그것을 어디로 보낼지 **먼저 Ji에게 확인한 뒤** 옮긴다. 이렇게 해야 vault 구조가 처음부터 지저분해지지 않는다.

---

## 작업 시작 전 확인할 것

- 세션을 시작하면 [`conversation_log.md`](conversation_log/conversation_log.md)와 최근 `YYMMDD_log.md`의 항목을 훑어 직전 맥락을 잡는다.
- 더 앞선 맥락이 필요하면 [`00_daily_worklog/00_daily_worklog.md`](../00_daily_worklog/00_daily_worklog.md)의 인덱스 표를 본다.
- 이 폴더의 파일은 임시다. 여기 있는 내용을 다른 문서의 근거로 삼지 않는다.
- 단 `conversation_log.md`와 `to_do.md`는 예외다. 이 둘은 임시 파일이 아니라 메모리 시스템의 상시 구성 요소다.
