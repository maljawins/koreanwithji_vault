# GritAI Studio | How to Use CLAUDE.md in Claude Code in 5 Minutes

## Metadata
- **채널:** GritAI Studio
- **URL:** https://youtu.be/h7QJL2_gEXA
- **Duration:** 06:39
- **Upload Date:** 2026-01-25
- **목적:** CLAUDE.md 작성
- **변환일:** 2026-08-31

---

## 핵심 요약
- `CLAUDE.md`는 Claude Code의 프로젝트 메모리 시스템으로, 아키텍처, 코딩 표준, 과거의 실수 등을 저장하여 세션 간 컨텍스트(context)를 유지한다.
- `/init` 명령어로 프로젝트 구조를 분석하여 기초 파일을 생성하고, `/memory` 명령어나 대화를 통해 실시간으로 학습 내용을 추가하며 관리한다.
- 메모리 계층 구조(Managed policy > Project memory > Project rules > User memory > Project local)를 이해하고, `.claude/rules/`를 활용해 모듈화된 규칙을 적용한다.

---

## 적용 지식

### CLAUDE.md의 역할과 초기화 방법 [00:58]
`CLAUDE.md`는 프로젝트의 영구적인 메모리 역할을 수행한다. Claude Code가 시작될 때마다 이 파일을 읽어 프로젝트의 기술 스택, 주요 디렉토리 구조, 코딩 패턴 및 과거에 해결한 문제들에 대한 정보를 파악한다. 이를 통해 Claude가 매번 토큰(token)을 낭비하며 코드베이스를 탐색하는 과정을 줄일 수 있다.

처음부터 파일을 직접 작성할 필요 없이, 터미널에서 `/init` 명령어를 실행하면 Claude가 `package.json`과 디렉토리 구조를 스캔하여 기초적인 `CLAUDE.md` 파일을 생성한다.

```bash
# Claude Code 실행 후 초기화 명령어
/init
```

### 메모리 계층 구조와 우선순위 [01:58]
Claude Code는 여러 위치의 메모리 파일을 참조하며, 상위 계층의 설정이 하위 설정을 덮어쓰는 우선순위를 가진다.

1.  **Managed policy (최상위):** 조직 차원의 코딩 표준 및 보안 정책. 개인이 수정할 수 없다.
    - 경로(macOS): `/Library/Application Support/claudeCode/CLAUDE.md`
2.  **Project memory:** 팀이 공유하는 프로젝트별 지침.
    - 경로: `./CLAUDE.md` 또는 `./.claude/CLAUDE.md`
3.  **Project rules:** 특정 언어나 프레임워크에 특화된 모듈형 규칙.
    - 경로: `./.claude/rules/*.md`
4.  **User memory:** 모든 프로젝트에 적용되는 개인 설정 및 단축키.
    - 경로: `~/.claude/CLAUDE.md`
5.  **Project memory (local):** Git에 커밋되지 않는 개인적인 프로젝트 노트.
    - 경로: `./CLAUDE.local.md` (자동으로 `.gitignore`에 추가됨)

### 모듈형 규칙과 경로별 설정 [03:42]
프로젝트 규모가 커지면 단일 `CLAUDE.md` 파일이 비대해질 수 있다. 이때 `.claude/rules/` 디렉토리에 `testing.md`, `security.md`, `code-style.md`와 같이 주제별로 파일을 분리하여 관리하는 것이 효율적이다.

특히 YAML 프론트매터(frontmatter)의 `paths` 필드를 사용하면 특정 파일 패턴에만 적용되는 규칙을 정의할 수 있다.

```markdown
---
paths:
  - src/api/**/*.ts
---
# API Development Rules
- 모든 API 엔드포인트는 표준 에러 응답 형식을 사용해야 함.
```

### 실시간 메모리 업데이트 및 관리 [03:18]
디버깅 중 까다로운 문제를 해결했거나 새로운 패턴을 적용했을 때, Claude에게 이를 기억하도록 요청할 수 있다. "이 해결책을 프로젝트 메모리에 추가해줘"라고 말하면 Claude가 `CLAUDE.md`를 업데이트한다.

또한 `/memory` 명령어를 통해 현재 로드된 메모리 상태를 확인하고 직접 편집할 수 있다.

```bash
# 메모리 관리 인터페이스 호출
/memory
```

### 외부 파일 참조 및 임포트 [04:10]
`CLAUDE.md` 내에서 `@` 기호를 사용하여 다른 파일의 내용을 참조하거나 임포트할 수 있다. 이를 통해 메인 설정 파일을 깔끔하게 유지하면서 상세 문서를 연결할 수 있다.

```markdown
# CLAUDE.md 예시
프로젝트 개요는 @README.md를 참조하고, 사용 가능한 명령어는 @package.json을 확인하십시오.

## 추가 지침
- Git 워크플로우: @docs/git-instructions.md
- 개인 설정: @~/.claude/my-project-instructions.md
```

---

## 주의사항

- **간결성 유지:** `CLAUDE.md`는 매 대화마다 로드되므로 너무 길어지면 성능에 부정적인 영향을 줄 수 있다. 상세한 내용은 별도 파일로 분리하고 임포트 기능을 활용한다.
- **주기적 검토:** 프로젝트가 진행됨에 따라 오래된 규칙은 삭제하거나 업데이트해야 한다. Claude에게 "우리 `CLAUDE.md` 파일을 검토해서 중복되거나 단순화할 부분을 찾아줘"라고 요청하여 관리할 수 있다.
- **데이터 날짜 기입:** 학습 내용을 추가할 때 발견된 날짜나 컨텍스트를 함께 기록하면 나중에 Claude가 상황을 판단하는 데 도움이 된다.
- **로컬 설정 주의:** `CLAUDE.local.md`는 개인용이므로 팀 전체가 알아야 할 규칙은 반드시 `./CLAUDE.md`에 작성해야 한다.