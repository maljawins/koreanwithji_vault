---
name: vault-day-close
description: Ji가 "오늘 마감", "하루 마감", "작업 마감", "작업 로그 정리" 또는 daily worklog 작성을 명시했을 때만 사용한다. conversation_log를 근거로 날짜 worklog, worklog index, to_do를 함께 마감한다. 일반 작업이나 단순 진행 보고에는 사용하지 않는다.
---

# Vault Day Close

Ji의 명시 요청은 이 workflow에서 필요한 파일 생성·수정과, daily log로 옮긴 conversation 항목 삭제의 승인이다. 그 밖의 파일은 건드리지 않는다.

1. `01_inbox/conversation_log/conversation_log.md`, `01_inbox/conversation_log/to_do.md`, `00_daily_worklog/00_daily_worklog.md`와 오늘의 기존 날짜 log가 있으면 읽는다.
2. 오늘 conversation 항목만 근거로 `00_daily_worklog/YYMMDD_log/YYMMDD_log.md`를 새로 만들거나 이어 쓴다. 기존 날짜 log의 문체와 구조를 따른다.
3. `00_daily_worklog.md` index에 날짜 링크, 목적, 처리결과, 비고를 한 행으로 추가하거나 그날 행을 갱신한다.
4. `to_do.md`는 완료·변경된 현재 할 일만 갱신한다. 더 먼 계획이나 작업 규칙은 넣지 않는다. `기준일`도 오늘로 바꾼다.
5. hook이 전달한 turn ID가 있으면, 아래 HTML marker를 각각 한 번 넣는다. 화면에는 보이지 않지만 hook의 완료 확인용 영수증이다.

```text
daily log:       <!-- codex-day-close:TURN_ID -->
daily index:     <!-- codex-day-close:TURN_ID -->
to_do:           <!-- codex-day-close:TURN_ID -->
```

6. 새 날짜 log 경로, index 링크, 수치, 중복을 확인한다. 확인이 끝난 항목만 `conversation_log.md`에서 지운다.
7. 결과에는 만든 날짜 log와 바뀐 `to_do` 핵심만 보고한다.

plan mode에서는 파일을 쓰지 않는다. 그 사실을 Ji에게 알리고, 다음 편집 가능한 turn으로 넘긴다.
