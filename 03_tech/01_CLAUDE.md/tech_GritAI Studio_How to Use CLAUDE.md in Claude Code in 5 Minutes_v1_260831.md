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
CLAUDE.md는 Claude Code의 프로젝트 메모리 시스템으로, 아키텍처, 코딩 표준, 과거의 실수 등을 저장하여 컨텍스트 창(context window)을 효율적으로 관리한다. `/init` 명령어로 기초 파일을 생성하고, `/memory` 명령어나 대화 중 직접적인 요청을 통해 실시간으로 학습 내용을 업데이트하며 복리적인 엔지니어링(compounding engineering) 효과를 얻을 수 있다. 대규모 프로젝트의 경우 `.claude/rules/` 디렉토리를 통해 규칙을 모듈화하고 경로별로 적용 범위를 제한하여 토큰 낭비를 방지한다.

---

## 적용 지식

### CLAUDE.md의 역할과 초기 설정 [00:58]
CLAUDE.md는 프로젝트의 영구적인 메모리 역할을 한다. Claude Code가 실행될 때마다 이 파일을 읽어 프로젝트의 기술 스택, 주요 디렉토리 구조, 코딩 패턴 및 주의사항을 파악한다. 이를 통해 매 세션마다 코드를 탐색하며 토큰을 낭비하는 것을 방지하고 시니어 팀원과 같은 수준의 이해도를 갖게 한다.

처음부터 직접 작성할 필요 없이 `/init` 명령어를 사용하여 기초 파일을 생성할 수 있다.
```bash
# Claude Code 터미널에서 실행
/init
```
이 명령어를 실행하면 Claude가 `package.json`을 읽고 디렉토리 구조를 스캔하여 빌드 시스템, 테스트 프레임워크, 코드 패턴을 감지한 후 요약된 CLAUDE.md 파일을 자동으로 생성한다.

### 메모리 계층 구조와 우선순위 [01:58]
Claude Code는 네 가지 수준의 메모리 계층을 가지며, 상위 계층의 설정이 우선순위를 갖는다.

- **Managed Policy (관리형 정책):** 조직 전체에 적용되는 보안 정책이나 코딩 표준. 개별 개발자가 수정할 수 없다.
  - 경로(macOS): `/Library/Application Support/claudeCode/CLAUDE.md`
- **Project Memory (프로젝트 메모리):** 팀이 공유하는 프로젝트별 지침. `CLAUDE.md` 또는 `.claude/CLAUDE.md`에 위치하며 Git으로 관리한다.
- **Project Rules (프로젝트 규칙):** `.claude/rules/*.md`에 위치하는 모듈화된 규칙. 특정 경로에만 적용되는 세부 지침을 담는다.
- **User Memory (사용자 메모리):** 모든 프로젝트에 걸쳐 적용되는 개인 선호 설정.
  - 경로: `~/.claude/CLAUDE.md`
- **Project Memory Local (로컬 프로젝트 메모리):** 개인적인 프로젝트 노트나 테스트 데이터. `CLAUDE.local.md` 파일에 저장하며 보통 `.gitignore`에 추가되어 공유되지 않는다.

### 실시간 메모리 관리 및 업데이트 [03:16]
디버깅을 통해 문제를 해결했거나 새로운 패턴을 적용했을 때, 이를 즉시 메모리에 추가하여 같은 실수를 반복하지 않게 할 수 있다. 대화 중에 "이 해결책을 프로젝트 메모리에 추가해줘"라고 요청하면 Claude가 관련 내용을 정리하여 CLAUDE.md를 업데이트한다.

또한 `/memory` 명령어를 통해 현재 로드된 메모리를 확인하고 직접 편집할 수 있다.
```bash
/memory
```

### 모듈형 규칙 및 경로별 규칙 설정 [03:42]
프로젝트가 커지면 하나의 CLAUDE.md 파일이 너무 비대해질 수 있다. 이때 `.claude/rules/` 디렉토리에 개별 마크다운 파일을 만들어 규칙을 분리한다.

**디렉토리 구조 예시:**
```text
your-project/
├── .claude/
│   ├── CLAUDE.md          # 메인 프로젝트 지침
│   └── rules/
│       ├── code-style.md  # 코딩 스타일 가이드라인
│       ├── testing.md     # 테스트 컨벤션
│       └── security.md    # 보안 요구사항
```

특정 파일 패턴에만 규칙을 적용하려면 YAML 프런트매터(frontmatter)의 `paths` 필드를 사용한다.
```markdown
---
paths: src/api/**/*,ts
---
# API Development Rules
- 모든 API 엔드포인트는 표준 에러 응답 형식을 사용해야 함.
```

### 외부 파일 및 URL 임포트 [04:10]
`@` 기호를 사용하여 다른 파일의 내용을 CLAUDE.md로 불러올 수 있다. 이를 통해 메인 파일을 깔끔하게 유지하면서 상세 문서를 참조할 수 있다.
```markdown
# CLAUDE.md
프로젝트 개요는 @README를 참조하고, 사용 가능한 명령어는 @package.json을 확인하십시오.

# 추가 지침
- Git 워크플로우: @docs/git-instructions.md
- 개인 설정: @~/.claude/my-project-instructions.md
```

### 복리적 엔지니어링(Compounding Engineering) 워크플로우 [04:35]
성공적인 워크플로우는 다음과 같은 루프를 따른다.
1. **Plan (계획):** 에이전트가 이슈를 읽고 구현 계획을 수립한다.
2. **Work (작업):** 계획에 따라 코드를 작성하고 테스트를 생성한다.
3. **Review (검토):** 엔지니어가 결과물과 학습된 교훈을 검토한다.
4. **Compound (복리화):** 학습된 내용을 시스템(CLAUDE.md)에 다시 입력하여 다음 루프의 성능을 향상시킨다.

---

## 주의사항
- **Concise (간결함) 유지:** CLAUDE.md는 모든 대화의 시작점에서 로드된다. 내용이 너무 길어지면 토큰 소모가 심해지고 모델의 성능에 부정적인 영향을 줄 수 있으므로 핵심 정보만 남겨야 한다.
- **Outdated Rules (오래된 규칙) 제거:** 주기적으로 `/clear` 명령어로 컨텍스트를 정리하거나 Claude에게 "CLAUDE.md 파일을 검토해서 중복되거나 단순화할 수 있는 부분을 찾아줘"라고 요청하여 최신 상태를 유지해야 한다.
- **Local Preferences:** 팀 공통 규칙은 `CLAUDE.md`에, 개인적인 설정이나 민감한 정보는 `CLAUDE.local.md`나 `.env.local`에 분리하여 관리한다.
- **Version History:** 데이터 구조 변경 시 기존 데이터를 업데이트(`UPDATE`)하는 대신 새로운 행을 삽입(`INSERT`)하는 방식과 같은 중요한 설계 결정은 반드시 메모리에 기록하여 실수를 방지한다.
  ```typescript
  // 예시: search_results 테이블에 새로운 결과 삽입 (버전 기록 보존)
  await supabase
    .from('search_results')
    .insert({
      saved_search_id: savedSearchId,
      results: {
        items: newResults,
        timestamp: new Date().toIsostring(),
        type: searchType
      }
    })
  ```