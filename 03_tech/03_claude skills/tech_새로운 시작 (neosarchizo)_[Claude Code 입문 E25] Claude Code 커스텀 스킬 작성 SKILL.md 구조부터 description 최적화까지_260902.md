# 새로운 시작 (neosarchizo) | [Claude Code 입문 E25] Claude Code 커스텀 스킬 작성: SKILL.md 구조부터 description 최적화까지

## Metadata
- **채널:** 새로운 시작 (neosarchizo)
- **URL:** https://youtu.be/_je6aq87I9c
- **Duration:** 22:54
- **Upload Date:** 2026-05-09
- **목적:** 03_claude_skills
- **변환일:** 2026-09-02

---

## 핵심 요약
- `SKILL.md`는 스킬의 진입점이며, `description` 필드는 사용자가 직접 호출하지 않을 때 Agent가 스킬 사용 여부를 결정하는 핵심 트리거 기준이 된다.
- 스킬 본문은 Agent가 이미 알고 있는 일반 지식(HTTP, PDF 정의 등)을 배제하고, 프로젝트 전용 컨벤션이나 구체적인 실행 절차(Procedure) 위주로 작성하여 컨텍스트 창(context window)을 최적화해야 한다.
- 실행 스크립트는 비상호작용(non-interactive) 환경에서 동작해야 하므로 TTY 프롬프트를 금지하고, 모든 입력은 플래그나 환경 변수로 처리하며 `stdout`과 `stderr`를 분리하여 설계한다.

---

## 적용 지식

### 커스텀 스킬 디렉토리 구조와 필수 규칙 [00:31]
Claude Code의 스킬은 단일 파일이 아닌 디렉토리 단위로 구성됩니다. `SKILL.md` 파일은 스킬의 메타데이터와 지시사항을 담는 진입점 역할을 수행합니다. 이 외에 선택적으로 세 가지 디렉토리를 포함할 수 있습니다. `scripts/`에는 Agent가 직접 실행할 코드를 배치하고, `references/`에는 상세 문서나 API 명세 등 필요할 때만 로드할 자료를 넣습니다. `assets/` 디렉토리는 템플릿, 스키마, 데이터 파일 등 정적 리소스를 관리하는 용도로 사용됩니다. 중요한 규칙은 `scripts/`나 `references/`에 포함된 서포팅 파일들을 Agent가 인식할 수 있도록 `SKILL.md` 본문에서 명시적으로 언급해야 한다는 점입니다. 단순히 디렉토리에 파일을 넣어두는 것만으로는 Agent가 해당 파일의 존재를 알 수 없습니다.

### SKILL.md의 구조와 프론트매트 제약 사항 [01:14]
`SKILL.md`는 YAML 프론트매트(frontmatter)와 마크다운(Markdown) 본문의 두 부분으로 나뉩니다. 프론트매트의 `name` 필드는 1~64자 사이의 소문자, 숫자, 하이픈만 허용되며, 시작과 끝에 하이픈을 쓸 수 없고 연속된 하이픈(`--`)도 금지됩니다. 또한 `name`은 반드시 부모 디렉토리 이름과 정확히 일치해야 합니다. `description` 필드는 1~1024자 사이로 작성하며, Claude Code는 `description`과 `when to use`를 합쳐 최대 1536자까지만 인식하고 나머지는 잘라냅니다.

```yaml
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, and merge multiple PDFs. Use this when the user mentions PDFs, forms, or document extraction.
---

# 스킬 본문 지시사항이 여기에 위치합니다.
```

### 확장 필드를 활용한 실행 제어 [02:49]
기본 필드 외에도 다양한 확장 필드를 통해 스킬의 동작 방식을 세밀하게 제어할 수 있습니다. `disable-model-invocation: true`로 설정하면 Agent가 자동으로 스킬을 트리거하는 것을 막고 사용자가 슬래시(`/`) 명령어로 직접 호출할 때만 작동하게 합니다. 이는 배포(`deploy`), 커밋(`commit`), 메시지 발송 등 사이드 이펙트(side effect)가 있는 작업에 필수적입니다. `context: fork`를 사용하면 해당 스킬을 별도의 서브에이전트(subagent) 환경에서 격리하여 실행할 수 있습니다.

| Field | Purpose |
| :--- | :--- |
| `model` | 특정 모델로 오버라이드 |
| `effort` | `effort` 레벨 변경 |
| `hooks` | 수명 주기 훅(Lifecycle hooks) 정의 |
| `paths` | 특정 파일 패턴(Glob match)에 따른 활성화 |
| `shell` | `bash` 또는 `powershell` 지정 |

### 컨텍스트 최적화와 본문 작성 원칙 [07:13]
`SKILL.md`의 본문은 활성화 시 컨텍스트 창(context window)에 직접 포함되므로 토큰(token)을 절약하는 것이 중요합니다. Agent가 이미 학습을 통해 알고 있는 일반적인 기술 정의(예: "PDF는 문서 포맷이다")는 과감히 삭제해야 합니다. 대신 프로젝트 고유의 컨벤션, 도메인별 절차, 특정 API의 엣지 케이스 등 Agent가 모를 수 있는 정보에 집중하십시오. 작성 시 "이 지시문이 없으면 Agent가 실수할까?"라는 질문을 던져보고, 답이 "아니오"라면 삭제하는 것이 원칙입니다.

- **나쁜 예시:** PDF는 텍스트와 이미지를 포함하는 일반적인 파일 포맷입니다. 텍스트 추출을 위해 라이브러리가 필요합니다.
- **좋은 예시:** 텍스트 추출 시에는 `pdfplumber`를 기본으로 사용하십시오. OCR이 필요한 스캔 문서의 경우 `pdf2image`와 `pytesseract`를 조합하여 처리하십시오.

### 효과적인 본문 패턴: Gotchas와 템플릿 [12:10]
잘 짜여진 스킬 본문에는 반복되는 패턴이 존재합니다. `Gotchas` 섹션은 환경 특화적인 사실이나 Agent가 자주 실수하는 지점을 기록하여 즉각적인 교정을 유도합니다. 예를 들어 "DB에서 사용자 ID는 `user_id`이지만, Billing API에서는 `account_id`로 참조해야 한다"와 같은 정보를 명시합니다. 또한 출력 형식이 중요한 경우 구체적인 마크다운 템플릿을 제공하면 Agent의 패턴 매칭 능력을 활용해 결과물의 일관성을 높일 수 있습니다.

```markdown
## Gotchas
- 유저 테이블 조회 시 반드시 `WHERE deleted_at IS NULL` 조건을 포함하여 소프트 딜리트된 데이터를 제외하십시오.
- Health 체크 API는 200을 반환하더라도 응답 본문의 `ready` 필드가 `true`인지 확인해야 실제 DB 연결 상태를 알 수 있습니다.

## Output Template
# [Analysis Title]
## Executive summary
[내용 요약]
## Key findings
- Finding 1 with data
```

### 워크플로우 제어 패턴 [13:50]
복잡한 작업은 다단계 체크리스트(Multi-Step Checklist)나 계획-검증-실행(Plan-Validate-Execute) 패턴을 사용합니다. 특히 파괴적인 작업이나 배치 작업 시에는 중간 단계에서 JSON 형태로 계획을 수립하고, 이를 원본 데이터(Source of Truth)와 대조하여 검증한 뒤 최종 실행하도록 지시합니다.

```markdown
### Progress Checklist
- [ ] Step 1: Analyze form (`analyze_form.py`)
- [ ] Step 2: Create field mapping (`fields.json`)
- [ ] Step 3: Validate (`validate_fields.py`)
- [ ] Step 4: Fill form (`fill_form.py`)
- [ ] Step 5: Verify output (`verify_output.py`)
```

### Agent 전용 스크립트 디자인 [15:08]
Agent가 실행할 스크립트는 사람이 사용하는 것과 설계 원칙이 달라야 합니다. 가장 중요한 요구 사항은 비상호작용(non-interactive) 환경 보장입니다. TTY 프롬프트가 뜨면 Agent는 응답할 수 없어 무한 대기 상태에 빠집니다. 따라서 모든 입력은 플래그(flags), 환경 변수(env vars), 또는 `stdin`을 통해 받아야 합니다.

- **Bad:** `python scripts/deploy.py` 실행 후 "Target environment:" 입력 대기
- **Good:** `python scripts/deploy.py --env staging --tag v1.2.3` 처럼 명확한 인자 전달. 필수 인자 누락 시 사용법(Usage)과 함께 에러 메시지 출력.

또한 데이터와 진단 정보를 분리해야 합니다. 구조화된 데이터(JSON, CSV 등)는 `stdout`으로 내보내고, 진행 상황이나 디버깅 메시지는 `stderr`로 내보내어 Agent가 결과를 파싱하기 쉽게 만듭니다.

### 스크립트 의존성 관리 [17:06]
스크립트 내부에 의존성을 선언하여 격리된 환경에서 실행되도록 구성합니다. Python의 경우 PEP 723을 준수하여 상단에 인라인 의존성을 적고 `uv run`으로 실행합니다.

```python
# /// script
# dependencies = [
#   "beautifulsoup4",
# ]
# ///
from bs4 import BeautifulSoup
# ... 스크립트 로직
```
다른 언어들도 유사한 방식을 지원합니다. Deno는 `npm:` 임포트를, Bun은 자동 설치를, Ruby는 `bundler/inline`을 활용하여 별도의 설치 단계 없이 스크립트를 실행할 수 있습니다.

### Description 최적화 및 검증 [18:09]
스킬의 자동 트리거 성능을 높이려면 `description`을 명령형(Imperative)으로 작성하고 사용자 의도(User intent)를 포함해야 합니다. "이 스킬은 ~를 한다"는 설명보다 "사용자가 ~를 하려 할 때 이 스킬을 사용하라"는 지시가 더 효과적입니다. 트리거가 너무 잦다면 범위를 좁히고, 트리거가 안 된다면 자연스러운 키워드가 포함되었는지 확인하십시오. `skills-ref validate ./my-skill` 명령어를 사용하여 배포 전 프론트매트 유효성과 네이밍 컨벤션을 점검할 수 있습니다.

---

## 주의사항
- **트리거 제한:** Claude Code는 `description`과 `when to use` 필드를 합쳐 앞부분 1536자까지만 트리거 결정에 사용하므로, 핵심 사용 사례는 반드시 앞부분(front-loaded)에 배치해야 합니다.
- **상호작용 금지:** 스크립트 실행 중 사용자 입력을 기다리는 TTY 프롬프트가 발생하면 Agent가 무한 대기에 빠지므로 절대 사용해서는 안 됩니다.
- **사이드 이펙트 관리:** 배포나 삭제 등 되돌리기 어려운 작업을 수행하는 스킬은 반드시 `disable-model-invocation: true`를 설정하여 Agent의 임의 실행을 방지해야 합니다.
- **네이밍 규칙:** 스킬 이름(`name`)은 반드시 소문자, 숫자, 하이픈만 사용해야 하며 부모 디렉토리 이름과 일치해야 합니다. 대문자나 연속된 하이픈은 유효하지 않습니다.