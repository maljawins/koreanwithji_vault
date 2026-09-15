# bri | CLAUDE.md Complete Guide — The File That Makes Claude Code Actually Useful

## Metadata
- **채널:** bri
- **URL:** https://youtu.be/9DTqFPv0oak
- **Duration:** 16:42
- **Upload Date:** 2026-07-05
- **목적:** CLAUDE.md 작성
- **변환일:** 2026-08-31

---

## 핵심 요약
Claude Code의 성능을 극대화하려면 프로젝트 루트의 `CLAUDE.md`를 중심으로 한 4단계 계층 구조(CLAUDE.md, Skills, Commands, Hooks)를 구축해야 한다. `CLAUDE.md`는 200줄 이내의 간결한 브리핑 문서로 유지하고, 상세한 규칙이나 반복적인 절차는 별도의 파일이나 자동화된 스크립트로 분리하여 컨텍스트 효율성을 높인다. 모든 설정 파일 끝에 "스스로 개선하라"는 지침을 추가함으로써 에이전트가 실수를 통해 학습하고 문서를 최신 상태로 유지하게 만드는 것이 핵심이다.

---

## 적용 지식

### Claude Code 최적화의 핵심: CLAUDE.md [00:29]

`CLAUDE.md`는 Claude Code가 프로젝트 세션을 시작할 때 가장 먼저 읽는 브리핑 문서이다. 이 파일은 에이전트에게 프로젝트의 정체성, 기술 스택, 핵심 컨벤션을 전달하여 매번 같은 설명을 반복하지 않게 한다. 효율적인 `CLAUDE.md` 작성을 위해서는 숙련된 개발자를 온보딩시킨다는 느낌으로 접근해야 한다. 일반적인 개발 지식은 생략하고, 해당 코드베이스만의 특수한 맥락과 규칙에 집중해야 한다. 파일이 너무 길어지면(200줄 이상) 모델이 내용을 무시할 수 있으므로 최대한 간결하게 유지하는 것이 중요하다.

### CLAUDE.md의 구조와 구성 요소 [01:15]

`CLAUDE.md`는 프로젝트 루트 디렉토리에 위치하며, `README.md`, `.gitignore`, `package.json` 등과 함께 관리된다. 문서는 다음과 같은 섹션으로 구분하여 작성하는 것이 권장된다.

1.  **Project Identity**: 프로젝트의 목적을 두 문장 내외로 설명하고 사용된 기술 스택을 명시한다.
2.  **Key Commands**: 일주일에 한 번 이상 실행하는 핵심 CLI 명령어를 설명과 함께 나열한다.
3.  **Conventions**: 코드베이스에서 사용하는 명명 규칙, 파일 구조, 패턴을 정의한다. 내용이 길어질 경우 `import` 기능을 활용해 외부 파일을 참조한다.
4.  **Hard Stops**: 사용자의 명시적 승인 없이 절대 수행해서는 안 되는 작업(의존성 설치, `.env` 읽기, 파괴적인 셸 명령어 등)을 명시한다.
5.  **Known Gotchas**: 과거에 발생했던 일반적인 오류와 그 해결책을 기록하여 에이전트가 시행착오를 줄이게 한다.
6.  **Links**: 핵심 로직 파일이나 문서로 연결되는 경로를 제공한다.

```markdown
# CLAUDE.md

## Key Commands
- `pnpm run lint` - run repository lint checks.
- `pnpm run format:check` - check whitespace formatting.
- `pnpm run verify` - start an in-process server and verify health, API, HTML, and static assets.
- `just verify` - full local verification if `just` is installed.

## Conventions
@docs/conventions.md

## Hard Stops
- Do not install dependencies without explicit approval. The demo is dependency-free on purpose.
- Do not read `.env`, private keys, keypairs, or secret files. Use `.env.example` only.
- Do not run production, mainnet, or destructive shell commands unless the user explicitly approves the exact action.
- Do not replace the app with a framework. The point is to keep setup concepts visible.

## Known Gotchas
- `customerImpact: "outage"` must always produce `SEV1`, even with low report counts.
- The queue sort is domain-specific: severity score first, then SLA state, then revenue at risk.
- Browser code should stay in `src/public/app.mjs`; domain logic belongs in `src/triage/rules.mjs`.
- The dev server uses built-in Node APIs, so API routes live in `src/server.mjs`.
- `pnpm run verify` starts its own temporary server. It does not require a separate dev server.

## Links
- Domain rules: `src/triage/rules.mjs`
- Domain reference skill: `.claude/skills/triage-domain/reference.md`
- Demo prompts: `docs/demo-prompts.md`
- Script review notes: `../SCRIPT_REVIEW.md`
```

### Skills를 통한 특정 도메인 지식 확장 [05:30]

Skills는 에이전트가 필요할 때만 로드하는 온디맨드(on-demand) 컨텍스트이다. 프로젝트 루트의 `.claude/skills/` 디렉토리 내에 각 스킬별 폴더를 만들고 그 안에 `SKILL.md` 파일을 작성하여 관리한다. 예를 들어 `triage-domain`이라는 스킬을 만들면 에이전트는 해당 도메인과 관련된 작업을 할 때만 이 정보를 참조한다. 모든 스킬 파일의 마지막에는 "해결되지 않은 문제가 발생하면 이를 해결하고 다음을 위해 이 파일을 업데이트하라"는 지침을 추가하여 에이전트가 스스로 문서를 유지보수하게 한다.

```markdown
# Triage Domain Reference

## Severity Rules
| Severity | Meaning | Target Response |
| --- | --- | --- |
| SEV1 | Outage or high customer-impact incident | 30 minutes |
| SEV2 | Degraded critical path or substantial revenue risk | 120 minutes |
| SEV3 | User-visible issue with limited scope | 480 minutes |
| SEV4 | Low-risk operational issue | 2880 minutes |

## Sort Order
1. Higher score first.
2. `breached` SLA before `watch`, then `healthy`.
3. Higher `revenueAtRisk`.
4. Older incident.

If you hit a blocker not covered here, solve it and update this file for next time.
```

### Commands와 Hooks를 이용한 워크플로우 자동화 [08:14]

Commands는 `/verify`와 같이 슬래시 명령어로 호출할 수 있는 실행 절차이다. `.claude/commands/` 폴더에 마크다운 파일로 저장하며, 실행해야 할 단계들을 순차적으로 기술한다. 

Hooks는 특정 생명주기 이벤트(lifecycle events)에서 자동으로 실행되는 결정론적 코드이다. `.claude/settings.json` 파일에 정의하며, 환각(hallucination) 없이 정확한 스크립트를 실행해야 할 때 사용한다. 세션 시작 시 컨텍스트를 로드하거나, 코드 수정 후 자동으로 포맷팅을 수행하는 등의 용도로 활용된다.

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "node scripts/hooks/session-context.mjs"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash|Read|Grep|Glob",
        "hooks": [
          {
            "type": "command",
            "command": "node scripts/hooks/block-risky-command.mjs"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "node scripts/hooks/format-after-edit.mjs"
          }
        ]
      }
    ]
  }
}
```

### Subagents를 활용한 역할 분리 [12:59]

Subagents는 메인 세션과 분리된 독립적인 Claude 인스턴스이다. `.claude/agents/` 디렉토리에 마크다운 파일로 정의하며, 특정 모델(예: `sonnet`)이나 도구 제한, 전용 시스템 프롬프트를 설정할 수 있다. 예를 들어 `code-reviewer.md`를 생성하면 메인 세션의 대화 기록에 오염되지 않은 상태로 코드 리뷰만 전문적으로 수행하는 에이전트를 호출할 수 있다. 이는 토큰 비용을 절감하고 특정 작업의 정확도를 높이는 데 유리하다.

---

## 주의사항

- **CLAUDE.md 길이 제한**: 파일이 200줄을 초과하면 에이전트가 내용을 무시하거나 컨텍스트 창(context window)을 과도하게 점유할 수 있다. 상세 내용은 반드시 Skills나 별도 문서로 분리해야 한다.
- **Global Hooks 주의**: `~/.claude/settings.json`에 설정된 전역 훅은 컴퓨터의 모든 프로젝트 세션에 적용되므로, 특정 프로젝트를 망가뜨리지 않도록 충분히 테스트한 후 적용해야 한다.
- **Self-improving 지침**: Command나 Skill 파일에 스스로 업데이트하라는 지침이 없으면 사용자가 수동으로 문서를 관리해야 하는 번거로움이 발생한다. 에이전트가 학습한 내용을 직접 기록하게 유도해야 한다.
- **보안**: `Hard Stops` 섹션에 `.env`나 비밀 키 파일에 대한 접근 금지 명령을 명시하여 에이전트가 실수로 민감한 정보를 읽지 않도록 방어막을 쳐야 한다.