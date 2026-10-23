# _vault_setup 인덱스

vault 운영 도구와 외부 자료를 .md로 변환하는 작업의 지도다.

최종 갱신: 2026-10-22

## 자료 변환

요청에 맞는 트랙의 가이드에서 입력·출력·작성 규칙을 확인한다.

| 트랙 | 규칙서 | 변환 대상 목록 | 실행 도구 |
|---|---|---|---|
| Korean | [korean_yt_md_guide.md](01_md_convert/korean_yt_md_guide.md) | [korean_yt_md_convert.xlsx](01_md_convert/korean_yt_md_convert.xlsx) | [kor_yt_md_pipeline.py](01_md_convert/_scripts/kor_yt_md_pipeline.py) |
| Tech | [tech_yt_md_guide.md](01_md_convert/tech_yt_md_guide.md) | [tech_yt_md_convert.xlsx](01_md_convert/tech_yt_md_convert.xlsx) | [tech_yt_md_pipeline.py](01_md_convert/_scripts/tech_yt_md_pipeline.py) |
| Teaching | [teaching_yt_md_guide.md](01_md_convert/teaching_yt_md_guide.md) | [teaching_yt_md_convert.xlsx](01_md_convert/teaching_yt_md_convert.xlsx) | [teaching_yt_md_pipeline.py](01_md_convert/_scripts/teaching_yt_md_pipeline.py) |

| 위치 | 역할 |
|---|---|
| `01_md_convert/result_check/convert_O/` | 가이드에 지정된 검증 통과 대기 경로. 현재 폴더는 없음 |
| [result_check/convert_F/](01_md_convert/result_check/convert_F/) | 변환 검증 실패 자료 |
| [kor_monitor_server.py](01_md_convert/_scripts/kor_monitor_server.py) | Korean 변환 진행 확인 도구 |
| [tech_monitor_server.py](01_md_convert/_scripts/tech_monitor_server.py) | Tech 변환 진행 확인 도구 |
| [ji_shorts_transcribe.py](01_md_convert/_scripts/ji_shorts_transcribe.py) | Ji Shorts 받아쓰기 도구 |
| [claude_gen/](01_md_convert/_scripts/claude_gen/) | 변환 실행·실패·재개 기록 |

## vault 운영 참고자료

| 문서 | 주제 |
|---|---|
| [Karpathy_LLM_wiki_gist_git.md](02_vault_ops/Karpathy_LLM_wiki_gist_git.md) | LLM Wiki 구조 참고자료 |
| [Obsidian with Claude Code](02_vault_ops/tech_jaredrhod_How%20I%20Set%20Up%20Obsidian%20with%20Claude%20Code_260831.md) | Obsidian과 에이전트 연결 참고자료 |

## 현재 지침·스킬·보관 위치

| 위치 | 역할 |
|---|---|
| [AGENTS.md](../AGENTS.md) | 현재 에이전트 규칙과 업무 기억 관리 기준 |
| [get-to-the-point-skill](../.agents/skills/get-to-the-point-skill/SKILL.md) | 간결한 응답을 위한 로컬 스킬 |
| [i-have-adhd](../.agents/skills/i-have-adhd/SKILL.md) | ADHD 모드 응답을 위한 로컬 스킬 |
| [_archive index](../_archive/_archive.md) | audit 보관 자료와 수정 전 파일 찾기 |
| [03_tech index](../03_tech/03_tech.md) | 일반 tech 학습 자료 찾기 |
