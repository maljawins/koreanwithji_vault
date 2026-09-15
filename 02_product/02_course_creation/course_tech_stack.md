# 코스 제작 기술 스택

> 이 문서는 **한국어 코스를 만드는 데 직접 쓰이는 도구와 기술**의 단일 출처다.
> 사업 전체 도구 스택(사이트 빌더, 이메일 도구, Skool Bot 등)은 `_about/Koreanwithji_기획서_v6_260902.md §3`에 있다. 여기서 다루지 않는다.
> tech 개념 자체를 공부하거나 참고 문서가 필요하면 [`03_tech/03_tech.md`](../../03_tech/03_tech.md)를 본다.
> 작업 절차와 STEP 정의는 [`course_plan.md`](course_plan.md)가 단일 출처다. 여기는 **도구**만 다룬다.
> 최종 갱신: 2026-09-02

---

## 1. 코스 제작에 쓰이는 도구 한눈에

| 용도 | 도구 | 결정 상태 | 비고 |
|---|---|---|---|
| 강의 Draft 작성 | Obsidian LLM Wiki + Claude Code | 확정 | 아래 §2 |
| Vault와 Claude 연결 | Obsidian MCP + Skill | 확정 | DP-1 확정 완료 |
| 유튜브 자료 .md 변환 | 자체 파이프라인 (Whisper + LLM) | 운영 중 | 규칙서는 [`_vault_setup/01_md_convert/korean_yt_md_guide.md`](../../_vault_setup/01_md_convert/korean_yt_md_guide.md) |
| 강사 등장 영상 | HeyGen (얼굴과 목소리 cloning) | 확정 방향 | 아래 §3 |
| 한글 모션 그래픽 | Remotion 또는 HeyFrames | **둘 중 미정** | 코드 기반 합성이라는 방향만 확정 |
| 영상 스타일 일관성 | Replicate | 확정 방향 | 모델은 미정 |
| 음성 트랙 | HeyGen 또는 ElevenLabs API | **둘 중 미정** | 어차피 목소리 cloning을 쓰므로 HeyGen에서 함께 뽑는 안이 유력. 그러나 더 자연스럽게 발화가 되는 도구 선택 예정. |
| 최종 인코딩 | FFmpeg | 확정 방향 | |
| 강의 업로드 | Teachable (유력) | 잠정 | 플랫폼 최종 선택은 기획서 v6 §6 |

---

## 2. Obsidian LLM Wiki (Draft 작성 핵심 도구)

> Karpathy의 LLM Wiki 패턴을 이 사업에 맞게 적용한 것이다.
> 패턴 원리 자체의 단일 출처는 [`_vault_setup/02_vault_ops/Karpathy_LLM_wiki_gist_git.md`](../../_vault_setup/02_vault_ops/Karpathy_LLM_wiki_gist_git.md). 여기서 재설명하지 않는다.
> 실제 vault 세팅은 [`_vault_setup/02_vault_ops/tech_jaredrhod_How I Set Up Obsidian with Claude Code_260831.md`](../../_vault_setup/02_vault_ops/tech_jaredrhod_How%20I%20Set%20Up%20Obsidian%20with%20Claude%20Code_260831.md)를 응용했다. 이 문서도 Karpathy의 LLM Wiki를 기반으로 하되 더 고도화된 실전 세팅을 담고 있다.

### 2-1. 왜 RAG가 아니라 Wiki인가
- 강의 Draft의 핵심은 "다중 자료 종합 + Ji의 brand voice 일관성"이다.
- Vector RAG는 chunk 단위로 조각을 꺼내므로 brand voice가 흔들리고 종합력이 약하다.
- Wiki는 LLM이 .md 페이지에 누적 정리하므로 일관성이 유지되고 Ji가 직접 눈으로 검증할 수 있다.
- Ji가 Python 초보라 LangChain 학습 곡선(2~4주)은 과하다. Obsidian은 1주 안에 쓸 수 있다.
- Phase 4의 Skool Bot에서 LangChain이 필요해지는데, 그때 이 Wiki가 그대로 base data가 된다.

### 2-2. 역할 분담

| Ji | Claude |
|---|---|
| 자료 소싱하고 Vault에 반입 | 자료를 읽고 Wiki 페이지 생성 및 갱신 |
| 방향 결정과 검수 | cross-reference 유지, 모순 발견 시 플래그 |
| 질문 (이 강의를 어떻게 구성할지) | Wiki 기반으로 답하고 Draft 생성 |
| Obsidian에서 결과 확인 | 작업 이력을 log에 기록 |

### 2-3. Wiki의 목적은 Draft에서 끝나지 않는다
사업 운영 내내 키우는 살아있는 지식 창고다. 콘텐츠, 마케팅, 학생 Q&A의 소스가 되는 AI Second Brain이며 쌓일수록 모든 작업의 기반이 단단해지는 복리 자산이다.

---

## 3. 영상 제작 자동화

### 3-1. 왜 자동화가 필수인가
Ji가 직접 촬영하고 편집하면 200개가 넘는 레슨에 몇 개월이 걸린다. 강의의 특징이 **시각적 변화 + 음향효과 + voiceover** 조합이라 편집 부담이 특히 크다.

예: "먹다 → 먹었어요" 변형 설명 한 장면
```
1. '먹다' 표시
2. '다' 제거 (모션: 글자 사라짐 + 효과음)
3. '었' 추가 (모션: 슬라이드인 + 효과음)
4. '어' 추가 (모션 + 효과음)
5. '요' 추가 (모션 + 효과음)
→ 최종 '먹었어요' + voiceover 설명
```

### 3-2. 스택 구성
- **HeyGen**: Ji의 얼굴과 목소리를 cloning해 강사 등장 영상 자동 생성
- **Remotion / HeyFrames**: JavaScript 기반 영상 합성. 위 예시 같은 한글 모션 그래픽을 코드로 만든다. Coding Agent가 구현을 담당
- **Replicate**: 편집 스타일 일관성 유지
- **음성 트랙**: HeyGen 또는 ElevenLabs API. 강사 영상에 이미 목소리 cloning을 쓰므로 HeyGen에서 음성까지 함께 뽑는 쪽이 관리가 단순하다. 다만 음질과 한국어 발음 자연스러움을 비교해보고 정한다
- **FFmpeg**: 최종 인코딩

### 3-3. Python의 역할
Python이 영상을 직접 그리지 않는다. API 호출, subprocess로 렌더 트리거, 배치 처리 오케스트레이션만 담당한다.

---

## 4. 이 스택을 쓰려면 Ji가 알아야 하는 것

**Phase 1에서 실제로 필요한 것만 적는다.**

- Obsidian 설치와 설정, Vault 구조 이해, MCP 연결
- Claude Code 운용: CLAUDE.md, Memory, Skills, Subagent
- Claude API 호출과 Structured output (대량 스크립트 생성)
- 파일 입출력과 배치 처리 (200개 레슨 단위 처리)
- HeyGen API 또는 UI, 음성 API 호출
- subprocess로 모션 그래픽 렌더 연동
- Context Engineering, Harness Engineering

**Phase 1에 필요 없는 것**: LangChain, 벡터 스토어, RAG. Phase 4 진입 시 배운다.

---

## 5. 미확정 항목

| 항목 | 내용 | 결정 시점 |
|---|---|---|
| 모션 그래픽 도구 | Remotion vs HeyFrames | Draft 생산이 안정된 뒤 PoC로 검증 |
| 음성 트랙 | HeyGen vs ElevenLabs API | 샘플 비교 후 |
| Replicate 모델 | 어떤 모델을 쓸지 | PoC 시점 |
| PoC | 레슨 1개를 Draft에서 실제 영상까지 끝까지 만들어보기 | 미실시 |

> 코스 제작 절차상의 결정 사항(DP 전체)은 [`course_plan.md`](course_plan.md) §10-2·§11이 관리한다. 여기는 도구 관련 항목만 둔다.
