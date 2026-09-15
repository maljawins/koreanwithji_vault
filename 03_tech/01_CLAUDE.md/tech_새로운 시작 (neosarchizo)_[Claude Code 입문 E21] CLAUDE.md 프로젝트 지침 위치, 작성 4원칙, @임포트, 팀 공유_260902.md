# 새로운 시작 (neosarchizo) | [Claude Code 입문 E21] CLAUDE.md 프로젝트 지침: 위치, 작성 4원칙, @임포트, 팀 공유

## Metadata
- **채널:** 새로운 시작 (neosarchizo)
- **URL:** https://youtu.be/Lqeq8Rb1SSE
- **Duration:** 16:31
- **Upload Date:** 2026-04-24
- **목적:** 01_CLAUDE.md
- **변환일:** 2026-09-02

---

## 핵심 요약
- `CLAUDE.md`는 `Claude Code` 세션 시작 시 자동으로 로드되어 빌드 명령, 코딩 컨벤션 등 영속적인 컨텍스트를 제공하는 마크다운 파일이다.
- 파일 크기는 200줄 이하로 유지하는 것이 권장되며, 내용이 많아질 경우 `@import` 구문이나 `.claude/rules/` 폴더를 활용해 모듈화한다.
- 프로젝트 루트(`Project`), 사용자 홈(`User`), 조직 표준(`Managed`), 로컬 전용(`Local`)의 4가지 계층 구조를 통해 지침의 적용 범위를 관리할 수 있다.

---

## 적용 지식

### CLAUDE.md의 역할과 Auto Memory 비교 [00:22]

`Claude Code` 세션은 매번 빈 컨텍스트로 시작되므로, 동일한 프로젝트임에도 불구하고 빌드 명령이나 폴더 구조를 매번 다시 설명해야 하는 번거로움이 있습니다. `CLAUDE.md`는 이러한 문제를 해결하기 위해 프로젝트 루트에 배치하는 마크다운 파일입니다. 사용자가 직접 작성하며, 작업 표준이나 워크플로우를 정의하는 데 사용됩니다. 반면 `Auto Memory`는 `Claude`가 작업을 수행하며 스스로 학습한 패턴(빌드 명령, 디버깅 인사이트 등)을 저장하는 용도로, `CLAUDE.md`와는 작성 주체와 목적에서 차이가 있습니다. `CLAUDE.md`는 강제적인 설정 파일이 아닌 행동 가이드(Behavior Guide)이자 컨텍스트로 취급되므로, 구체적이고 간결하게 작성할수록 `Claude`의 준수율이 높아집니다.

### 지침 파일의 4가지 위치와 우선순위 [01:59]

`Claude Code`는 지침을 찾기 위해 작업 디렉토리부터 상위 트리로 올라가며 파일을 검색합니다. 발견된 모든 파일은 컨텍스트에 추가되며, 더 구체적인 위치에 있는 설정이 나중에 추가되어 우선권을 가집니다.

- **Managed (조직 표준):** `/Library/Application Support/ClaudeCode/` 경로에 위치하며 조직 전체 사용자에게 공유됩니다.
- **Project (팀 공유):** `./CLAUDE.md` 파일로, `Git`을 통해 팀원과 공유되는 표준 지침입니다.
- **User (개인 전역):** `~/.claude/CLAUDE.md` 경로에 두며, 해당 사용자의 모든 프로젝트에 공통 적용됩니다.
- **Local (개인 로컬):** `./CLAUDE.local.md` 파일로, `Git`에 커밋하지 않고 해당 프로젝트에서만 사용하는 개인 설정(테스트용 자격 증명 등)입니다.

### CLAUDE.md 초기화 및 인터랙티브 모드 [03:20]

빈 파일에서 시작할 필요 없이 `Claude Code` 내부에서 `/init` 명령을 실행하면 코드베이스를 분석하여 빌드/테스트 명령과 컨벤션을 포함한 시작용 파일을 생성해 줍니다. 더 정교한 생성을 원한다면 환경 변수를 설정하여 인터랙티브 모드를 활성화할 수 있습니다.

```bash
# 인터랙티브 모드 활성화
export CLAUDE_CODE_NEW_INIT=1
```
이 모드에서는 `subagent`가 코드베이스를 탐색하고 사용자에게 후속 질문을 던진 뒤, `CLAUDE.md`, `Skills`, `Hooks` 중 선택한 산출물에 대한 제안서를 먼저 보여줍니다.

### 효과적인 작성을 위한 4가지 원칙 [04:11]

1. **Size (크기):** 가급적 200줄 이하를 유지해야 합니다. 파일이 너무 길면 컨텍스트 소비가 늘어나고 지침 준수율이 떨어집니다.
2. **Structure (구조):** 헤더와 불릿 포인트를 사용하여 관련 지시를 정리합니다. `Claude`는 밀집된 문단보다 구조화된 섹션을 더 잘 파악합니다.
3. **Specificity (명확성):** 추상적인 표현 대신 검증 가능한 구체적인 지시를 사용합니다. 예를 들어 "코드를 잘 포맷하라" 대신 "2-space indentation을 사용하라"고 적고, "테스트하라" 대신 "npm test를 실행하라"고 명시합니다.
4. **Consistency (일관성):** 규칙이 충돌하면 `Claude`는 임의로 선택합니다. 프로젝트가 커지면 `.claude/rules/` 등과 비교하여 오래된 지시를 정기적으로 정리해야 합니다.

### 권장되는 섹션 구성 예시 [05:42]

대부분의 프로젝트에서 유용한 공통 카테고리는 다음과 같습니다.

- **프로젝트 정보:** 기술 스택(React 18, TypeScript 등)과 주요 기능 정의.
- **Build & Test Commands:** 개발 서버 실행, 빌드, 린트 명령 명시.
```markdown
## Commands
- Dev server: `pnpm dev`
- Build: `pnpm build`
- Test: `pnpm test`
- Lint: `pnpm lint`
- Type check: `pnpm typecheck`
```
- **Coding Conventions:** 함수형 컴포넌트 사용 여부, `Result` 타입을 이용한 에러 처리 등 팀 합의 규칙.
- **폴더 구조:** `src/features`, `src/api/handlers/` 등 각 폴더의 역할 정의.
- **Git Conventions:** `Conventional Commits` 준수 여부 및 브랜치 접두사(`feature/`, `bugfix/`) 정의.
- **Warnings:** `.env` 커밋 금지, 마이그레이션 파일 수정 금지 등 주의사항.

### @Import 구문과 외부 파일 참조 [07:50]

`CLAUDE.md` 내에서 `@path/to/file` 구문을 사용하여 다른 파일의 내용을 컨텍스트에 포함할 수 있습니다. 이는 재귀적으로 작동하며 최대 5단계 깊이까지 지원합니다.

```markdown
# 외부 파일 임포트 예시
@README.md
@package.json
@docs/git-instructions.md

# 개인 노트 공유 (홈 디렉토리 참조)
@~/.claude/my-project-instructions.md
```
작업 디렉토리 외부의 파일을 임포트할 경우 `Claude Code`는 보안을 위해 승인 다이얼로그를 띄웁니다. 또한, 다른 도구에서 사용하는 `agent.md`가 있다면 `CLAUDE.md` 상단에 `@agent.md`를 추가하는 브릿지 패턴을 통해 지침을 공유할 수 있습니다.

### 세션 관리 및 디버깅 명령 [11:58]

- `/memory`: 현재 세션에 로드된 `CLAUDE.md`, `CLAUDE.local.md`, `rules` 파일 목록을 확인합니다. 지침이 무시된다면 이 명령으로 로드 여부를 먼저 확인해야 합니다.
- `/compact`: 긴 세션 도중 컨텍스트를 압축합니다. 이때 루트의 `CLAUDE.md`는 디스크에서 다시 읽혀 재주입되지만, 하위 디렉토리의 파일은 자동으로 재주입되지 않으므로 주의가 필요합니다.

---

## 주의사항

- **컨텍스트 압축 시 유실:** `/compact` 실행 후에는 대화로만 전달했던 지시나 하위 디렉토리의 `CLAUDE.md` 지침이 사라질 수 있습니다. 영속적인 규칙은 반드시 루트의 `CLAUDE.md`에 작성하십시오.
- **개인 설정 노출 방지:** `CLAUDE.local.md`에는 개인적인 자격 증명이나 메모가 포함되므로 반드시 `.gitignore`에 추가해야 합니다. `/init` 실행 시 `personal` 옵션을 선택하면 자동으로 처리됩니다.
- **시스템 프롬프트와의 차이:** `CLAUDE.md`는 시스템 프롬프트가 아닌 사용자 메시지 레벨로 전달됩니다. 따라서 지침이 모호하면 엄격하게 지켜지지 않을 수 있습니다. 강력한 제어가 필요하다면 CLI 실행 시 `--append-system-prompt` 플래그를 사용하십시오.
- **HTML 주석 처리:** `CLAUDE.md` 내의 블록 레벨 HTML 주석(`<!-- comment -->`)은 컨텍스트 주입 전 제거되므로 사람을 위한 메모 용도로만 사용하십시오. 단, 코드 블록 내부의 주석은 보존될 수 있습니다.
- **모노리포 설정:** 대규모 모노리포에서 특정 `CLAUDE.md`가 불필요하게 컨텍스트를 차지한다면 `.claude/settings.local.json` 파일에 `claudeMdExcludes` 패턴을 설정하여 제외할 수 있습니다. (단, `Managed` 정책 파일은 제외 불가)
- **파일 목록 예시:** 프로젝트 구조 설계 시 `.editorconfig`, `.eslintignore`, `.eslintrc.cjs`, `.husky`, `.npmrc`, `.nvmrc`, `.prettierignore`, `.prettierrc.cjs`, `.vscode`, `20260423-optimization.md`, `electron-builder.yml`, `ELECTRON-FILE-MERGER`, `electron.vite.config.ts` 등의 설정 파일 위치를 명확히 인지하고 지침에 반영해야 합니다.