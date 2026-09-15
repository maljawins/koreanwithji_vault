# _vault_setup 인덱스

> 이 폴더는 **obsidian vault를 만들고 운영하기 위한 도구와 규칙서**를 모아둔 곳이다.
> 에이전트는 이 폴더 안의 작업을 시작하기 전에 이 파일을 먼저 읽는다.
> 최종 갱신: 2026-09-15

---

## 폴더 구조

```
_vault_setup\
├─ _vault_setup.md              ← 이 파일. 폴더 인덱스
├─ 01_md_convert\               ← 외부 자료를 .md로 변환하는 작업 전체 (현재는 유튜브 영상, 추후 PDF·웹페이지 캡쳐 이미지 등으로 확장 예정)
│   ├─ korean_yt_md_guide.md    ← Korean 트랙 규칙서
│   ├─ korean_yt_md_convert.xlsx← Korean 트랙 변환 대상 목록 (정본)
│   ├─ tech_yt_md_guide.md      ← Tech 트랙 규칙서
│   ├─ tech_yt_md_convert.xlsx  ← Tech 트랙 변환 대상 목록
│   ├─ result_check\            ← 변환 결과물 검토 대기소 (2026-09-03: 01_inbox에서 이동)
│   │   ├─ convert_O\           ← 검증 통과분 (tech·korean 공용, tech는 여기가 유일한 성공 저장소)
│   │   └─ convert_F\           ← 검증 실패분 (tech·korean 공용)
│   └─ _scripts\
│       ├─ kor_yt_md_pipeline.py    ← Korean 트랙 변환 스크립트
│       ├─ kor_monitor_server.py    ← Korean 변환 진행상황 대시보드
│       ├─ tech_yt_md_pipeline.py   ← Tech 트랙 변환 스크립트
│       ├─ tech_monitor_server.py   ← Tech 변환 진행상황 대시보드
│       └─ claude_gen\              ← 실행 로그·실패 로그·재개 manifest
├─ 02_vault_ops\                ← vault 운영에 관련된 tech 참고자료 보관
│   ├─ Karpathy_LLM_wiki_gist_git.md
│   └─ tech_jaredrhod_How I Set Up Obsidian with Claude Code_260831.md
└─ 03_second_brain_info\        ← Ji가 별도 관리. 에이전트는 지시가 없으면 건드리지 않는다
```

---

## 각 항목의 역할

| 항목 | 역할 |
|---|---|
| `01_md_convert\` | 외부 자료를 구조화된 .md로 바꾸는 작업 전체. 현재는 유튜브 영상 변환만 돌아가지만, 추후 PDF나 웹페이지 캡쳐 이미지 등 다른 형태의 자료도 이 폴더에서 .md로 변환할 예정이다. 목적이 다른 **Korean 트랙**과 **Tech 트랙**으로 나뉘고, 두 트랙은 규칙서·스크립트가 완전히 분리되어 있다. 입력·출력·파일명·작성 규칙 등 상세 내용은 각 트랙 가이드 파일에 있다 |
| [`korean_yt_md_guide.md`](01_md_convert/korean_yt_md_guide.md) | Korean 트랙의 유일한 근거 문서. 이 파일 하나만 읽고 korean 작업이 가능하다 |
| [`tech_yt_md_guide.md`](01_md_convert/tech_yt_md_guide.md) | Tech 트랙의 유일한 근거 문서. 이 파일 하나만 읽고 tech 작업이 가능하다 |
| [`korean_yt_md_convert.xlsx`](01_md_convert/korean_yt_md_convert.xlsx) / [`tech_yt_md_convert.xlsx`](01_md_convert/tech_yt_md_convert.xlsx) | 각 트랙의 변환 대상 목록. 정본은 이 경로뿐이며 사본을 만들지 않는다 |
| `result_check\` | 변환된 .md가 Ji의 수동 검토를 거치는 대기소. `convert_O\`(검증 통과)와 `convert_F\`(검증 실패)로 나뉘고 tech·korean 두 트랙이 같이 쓴다. Ji가 검토 후 직접 최종 위치로 옮긴다 |
| [`_scripts\kor_yt_md_pipeline.py`](01_md_convert/_scripts/kor_yt_md_pipeline.py) / [`tech_yt_md_pipeline.py`](01_md_convert/_scripts/tech_yt_md_pipeline.py) | 각 트랙의 변환 파이프라인. 한국어 전용 지점과 영어 전용 지점이 코드 곳곳에 박혀 있어 서로 복사해서 고치지 않는다 (이유는 각 가이드 참고) |
| [`_scripts\kor_monitor_server.py`](01_md_convert/_scripts/kor_monitor_server.py) / [`tech_monitor_server.py`](01_md_convert/_scripts/tech_monitor_server.py) | 각 트랙의 변환 진행상황 브라우저 대시보드 |
| `_scripts\claude_gen\` | 파이프라인 실행 로그·실패 로그·재개 manifest |
| `02_vault_ops\` | vault 구조 설계, Obsidian·Codex 세팅 등 **vault 운영 자체**에 관한 tech 참고자료를 모아두는 곳. 일반 tech 지식(03_tech로 가는 것)과 구분해서 여기 따로 둔다 |
| `03_second_brain_info\` | Ji가 별도 관리하는 자료. 에이전트는 지시가 없으면 건드리지 않는다 |

---

## 작업 시작 전 확인할 것

- korean 작업인지 tech 작업인지 먼저 정하고, 해당 트랙 가이드만 읽는다. 두 가이드를 동시에 참조하면 규칙이 충돌한다.
- 트랙별 상세 규칙(상태값, 파일명, 출력 경로, 파이프라인 구조, 미완 항목 등)은 이 파일이 아니라 [`korean_yt_md_guide.md`](01_md_convert/korean_yt_md_guide.md) / [`tech_yt_md_guide.md`](01_md_convert/tech_yt_md_guide.md)를 본다.
