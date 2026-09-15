# 새로운 시작 (neosarchizo) | [Claude Code 입문 E26] Claude Code 실전 스킬 만들기: PR 리뷰, 테스트 생성, 문서 생성 SKILL.md 예제

## Metadata
- **채널:** 새로운 시작 (neosarchizo)
- **URL:** https://youtu.be/eTXP2qPCYEI
- **Duration:** 16:42
- **Upload Date:** 2026-05-12
- **목적:** 03_claude_skills
- **변환일:** 2026-09-02

---

## 핵심 요약
- `SKILL.md`는 Agent가 모르는 프로젝트 고유의 관례(Conventions)와 함정(Gotchas)을 정의하여 빌트인(Built-in) 기능의 일반성을 보완한다.
- `context: fork`와 `agent: Explore`를 조합하여 대규모 변경 사항이 메인 컨텍스트를 오염시키지 않도록 격리된 환경에서 처리한다.
- `Plan-validate-execute` 패턴과 `assets/` 폴더 분리를 통해 토큰 효율성을 높이고 파괴적인 작업(Bulk destructive tasks)의 안전성을 확보한다.

---

## 적용 지식

### 커스텀 스킬 제작의 필요성과 기준 [00:34]
Claude Code는 `/review`, `/security-review`, `/simplify`, `/init`, `/batch` 등 강력한 빌트인 명령과 번들 스킬을 이미 갖추고 있다. 하지만 빌트인 기능은 일반적(Generic)이어서 팀의 특정 컨벤션이나 도메인 특유의 함정, 원하는 출력 형식을 알지 못한다. 따라서 `SKILL.md`에는 Agent가 이미 알고 있는 일반 지식은 제외하고, 해당 프로젝트에만 한정된 지식(Project-Specific facts)만 작성하는 것이 효율적이다.

### Skill 1: PR 리뷰 스킬 (review-pr) [01:43]
PR(Pull Request)의 변경 사항을 격리된 환경에서 동적 컨텍스트와 함께 검토하는 스킬이다. `context: fork`를 사용하여 서브 에이전트(Subagent) 환경에서 실행함으로써 대량의 Diff 데이터가 메인 컨텍스트 창(Context window)을 오염시키는 것을 방지한다.

**Design Decisions**
- **Content type:** Task content
- **Isolation:** `context: fork`
- **Subagent:** `agent: Explore` (코드 탐색 최적화)
- **Pre-approved tools:** `gh *`, `git *`
- **Dynamic context:** `!gh pr diff`

**SKILL.md Frontmatter**
```yaml
---
description: >
  Review the current branch's pull request for code quality, bugs, performance, and project conventions. 
  Use when the user asks to review a PR, audit pending changes before merge, or check what's about to ship – 
  even if they don't say the word "PR."
context: fork
agent: Explore
allowed-tools: Bash(gh *) Bash(git diff *) Bash(git log *)
---
```

**Dynamic Context Block**
느낌표(`!`)와 백틱으로 쉘 명령을 감싸면 스킬 호출 시점에 실시간 데이터가 주입된다. 이는 Claude가 `SKILL.md`를 읽기 전에 실행되므로, Claude는 "Diff를 가져와라"라는 명령이 아닌 실제 Diff 텍스트를 직접 수신하게 된다.
```markdown
## PR Context
- Diff: !`gh pr diff`
- Comments: !`gh pr view --comments`
- Files: !`gh pr diff --name-only`
- Recent commits: !`git log -10 --oneline`
```

**Project-Specific Gotchas 예시**
```markdown
## Gotchas
- `users` table is soft-deleted – must include `WHERE deleted_at IS NULL`
- Same user ID has 3 names: `user_id`, `uid`, `accountId`
- `/health` returns 200 even if DB is down – use `/ready`
- React components: `function`, not `const X = () =>`
- New env vars need `.env.example` update
```

**Output Template**
자유 서술 대신 표 형식과 고정된 열거형(Enum) 심각도를 사용하여 구조를 강제한다.
| Severity | File:Line | Issue | Fix |
| :--- | :--- | :--- | :--- |
| 🔴 High | api/users.ts:42 | SQL concat | parameterize |
| 🟡 Medium | Card.tsx:15 | const arrow | function decl |
| 🟢 Low | docs/api.md:80 | stale path | update to v2 |

### Skill 2: 테스트 생성 스킬 (generate-tests) [05:48]
`$ARGUMENTS`로 파일 경로를 전달받아 테스트가 통과할 때까지 검증 루프(Validation loop)를 수행하는 스킬이다.

**Design Decisions**
- **Arguments:** `$ARGUMENTS` (file path)
- **Hint:** `argument-hint: [file-path]`
- **Isolation:** `inline` (메인 컨텍스트에서 즉시 검증)
- **Pre-approved:** `Read`, `Write`, `Bash(npm test*)`
- **Pattern:** Validation loop

**Workflow (Procedures, not declarations)**
1. **Analyze file:** `$ARGUMENTS` 파일을 읽고 `export function`, `export class` 등 심볼을 추출하여 시그니처와 외부 의존성을 파악한다.
2. **Design cases:** 정상 경로, 경계값(빈 입력 등), 에러 케이스(외부 호출 실패 등)를 설계한다.
3. **Write tests:** `Given-When-Then` 구조를 사용하여 테스트 코드를 작성한다.
4. **Run tests (Validation Loop):** `npm test <file>`을 실행한다.
   - `Pass`: 종료(`done`).
   - `Fail`: 원인 진단(`diagnose`). 테스트 오류면 테스트 수정, 코드 버그면 중단 후 사용자 보고, Mock 설정 오류면 설정 점검 후 재시도.
   - 최대 5회(`5-try cap`)까지 반복(`retry`)한다.

**File Location Convention**
선택지를 주지 않고 하나의 고정된 패턴(`Defaults, not menus`)을 사용한다.
- Source: `src/utils/parse.ts`
- Test: `src/utils/__tests__/parse.test.ts`

### Skill 3: 문서 생성 스킬 (generate-docs) [09:47]
`Plan-validate-execute` 패턴과 `assets/` 폴더를 활용하여 API 레퍼런스 문서를 일괄 생성하는 스킬이다.

**Design Decisions**
- **Arguments:** `[source-dir]`
- **Pattern:** `Plan-validate-execute`
- **Assets:** 출력 템플릿 분리 (`token-efficient`)
- **Pre-approved tools:** `Read`, `Write`, `Glob`, `Grep`

**SKILL.md Frontmatter**
```yaml
---
description: >
  Generate API reference documentation in markdown for a TypeScript source directory. 
  Extracts exported functions, classes, and types with signatures, descriptions, return values, and usage examples from JSDoc.
argument-hint: [source-dir]
allowed-tools: Read Write Glob Grep
---
```

**3단계 실행 패턴**
1. **Step 1: Plan** - 대상 파일 목록과 덮어쓰기 여부를 사용자에게 구체적으로 보여준다.
2. **Step 2: Validate** - 사용자의 승인(`Proceed?`)을 기다린다. 일괄 파괴적 작업(Bulk destructive tasks) 전의 안전장치다.
3. **Step 3: Execute** - 각 파일에 대해 `.Extract`, `.Parse` 과정을 거쳐 `assets/api-template.md` 형식을 적용한 후 `Write` 한다. 진행 상황을 로그(`Log progress: [3/18] ...`)로 남긴다.

**assets/api-template.md**
템플릿을 `SKILL.md` 외부에 두어 토큰을 절약한다.
```markdown
# {ModuleName}
## Functions
### `functionName(p1: T1, p2: T2): ReturnType`
{JSDoc summary}
**Parameters**
- `p1` (`T1`) - {description}
- `p2` (`T2`) - {description}
**Returns** `ReturnType` - {description}
```

### 전체 워크플로우 통합 (Combining All Three) [13:43]
개별 스킬은 작고 응집력 있는 단위(`One Coherent Unit`)로 유지하며, 필요에 따라 체인처럼 조합하여 사용한다.
1. 기능 구현 작업
2. `//generate-test`로 테스트 생성 및 검증
3. `//generate-docs`로 문서 갱신
4. 빌트인 `//commit` 및 `//pr` 실행
5. `//review-pr`로 최종 검토

---

## 주의사항

- **자동 호출(Auto-invocation) 실패 시:** `description`에 자연스러운 사용자 표현이 포함되었는지, 1,536자 제한 내에 있는지, `disable-model-invocation: true` 설정이 실수로 켜져 있지 않은지 확인해야 한다. [14:39]
- **작업 중 스킬 효과 소실:** 오토 컴팩션(Auto-compaction) 발생 시 첫 5,000 토큰만 다시 첨부(`re-attachec`)되므로, 긴 작업 중 스킬이 무시되는 것 같으면 해당 스킬을 다시 호출(`invoke`)하여 전체 내용을 갱신해야 한다. [15:16]
- **느낌표(!) 명령 실행 불가:** Claude Code 설정에서 `disableSkillShellExecution`이 활성화되어 있는지, 블록 내 문법 오류나 백틱 인용이 깨지지 않았는지 점검한다. [15:36]
- **격리 환경의 이점:** `context: fork`를 사용하지 않고 대규모 PR Diff를 메인 세션에 직접 불러오면 컨텍스트 창이 금방 가득 차서 이전 대화 내용을 잊어버릴 수 있다. [05:08]