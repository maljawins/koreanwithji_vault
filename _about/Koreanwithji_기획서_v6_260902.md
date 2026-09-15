# Koreanwithji 사업 기획서 v6

> 최종 수정일: 2026-09-02
> 강사: Ji (Koreanwithji)
> 이 문서의 용도: **Ji의 한국어 온라인 교육 사업 전체 운영 로드맵의 단일 출처.** Agent가 "지금 무엇을 먼저 해야 하는가"를 판단하는 근거.
> 브랜드 정의는 [`01_brand.md`](01_brand.md), 퍼널과 가격은 [`04_marketing/marketing_plan.md`](../04_marketing/marketing_plan.md), 코스 제작 실행은 [`02_product/02_course_creation/02_course_creation.md`](../02_product/02_course_creation/02_course_creation.md)를 본다. 여기서 재설명하지 않는다.

---

## 변경 이력

| 버전 | 날짜 | 주요 변경 |
|---|---|---|
| v4 | 2026-05-28 | 초안 작성, Phase 1~4 구조 확정 |
| v5 | 2026-05-30 | Phase 1 Draft 작성 도구를 Obsidian LLM Wiki로 변경. LangChain RAG는 Skool Bot 단계로 이동 |
| v6 | 2026-09-02 | Vault를 처음부터 재구성. 문서별 역할을 나눠 중복 제거: 브랜드는 [`01_brand.md`](01_brand.md), 퍼널·가격은 [`marketing_plan.md`](../04_marketing/marketing_plan.md), 코스 제작 실행은 [`02_course_creation.md`](../02_product/02_course_creation/02_course_creation.md), 코스 제작 전용 기술은 [`course_tech_stack.md`](../02_product/02_course_creation/course_tech_stack.md)로 분리. eBook을 독립 Phase 2로 승격하고 이후 Phase 번호를 한 칸씩 밀었다 |

---

## 1. 비즈니스 현황 및 자산

### 1-1. 보유 자산
- **TikTok 팔로워**: 약 23,000명 (영어권 글로벌)
- **Instagram 팔로워**: 약 100명
- **YouTube 구독자**: 약 800명
- **도메인**: koreanwithji.com (Cloudflare 보유)
- **이메일 리스트**: 약 1,400명 (AI prompt lead magnet으로 수집)
- **검증된 Lead Magnet**: 한국어 문장 분석 AI prompt (현재도 이메일 유입 중)
- **1:1 강의 자료**: PPT + lesson script 25개 레슨 분량
- **외부 참고자료**: howtostudykorean.com 전체 유닛과 레슨, Amira 세션, 교재 6종, Curriculum Map
- **소셜미디어 숏폼 아카이브**: 본인 채널에서 운영했던 한국어 콘텐츠 (현재 약 2년간 업로드 중단 상태)

### 1-2. 코스 자산 현황 (2026-09-03 기준)
- **커리큘럼 확정 완료**: 16개 레벨(VSL, Intro, Hangul, Numbers, Level 1~12), 레슨 폴더 196개
- **Raw 자료 주입 완료**: `02_product/01_raw` 하위 .md 1,747개
- **Ji 직접 작성 Draft**: `01_Ji_draft` 트랙에 97개. 완성도는 레슨마다 다르다
- 레슨별 상세 현황은 [`02_product/01_raw/01_raw.md`](../02_product/01_raw/01_raw.md)와 `02_course_creation/00_curriculum_and_index`의 index xlsx가 단일 출처

---

## 2. 단계별 로드맵 (코스 완성이 모든 것의 기반)

### Phase 1: 코스 완성 (최우선, 현재 단계)
**왜 가장 먼저인가**: 완성된 강의 콘텐츠가 모든 콘텐츠 Repurposing의 축이다. 숏폼, 롱폼, 블로그, eBook, 뉴스레터, 카피가 전부 강의에서 파생된다. 이게 없으면 마케팅도 못 하고 사이트도 비어 있다.

**실행 계획 단일 출처**: [`02_product/02_course_creation/02_course_creation.md`](../02_product/02_course_creation/02_course_creation.md)

**필요 기술 단일 출처**: [`02_product/02_course_creation/course_tech_stack.md`](../02_product/02_course_creation/course_tech_stack.md)

---

### Phase 2: eBook 제작
- 완성된 강의 대본을 Claude로 eBook 재구성
- 권당 분리 출시($12~15), 번들 할인
- 강의 플랫폼의 Digital Downloads로 판매. 코스 유료 구매를 유도하는 미끼상품.
- 작업 폴더는 Phase 2 진입 시점에 만든다. 지금은 만들지 않는다

---

### Phase 3: koreanwithji.com 구축
**왜 이 순서인가**: 강의가 완성돼야 랜딩 페이지에 넣을 것이 생기고, eBook도 강의에서 나온다.

- **3-1. 빌더 결정**: 아래 §3-2 요건 기준으로 직접 비교
- **3-2. 사이트 구축**: 심플한 구조 + 제대로 된 디자인. 브랜드 컬러는 푸른색 계열(파란색, 남색, 하늘색). 메인 페이지 + 유료강의 Landing(VSL embed + 결제 embed) + Hidden 광고 랜딩 구조
- **3-3. Affiliate 프로그램 가입**: Kimchi Reader, SRS Flashcard 앱(Anki, Memrise), Amazon Affiliate(교과서, 한글 키보드, 키보드 스티커, K-pop merch 등을 Resources 페이지에)
- **3-4. Lead Magnet 다양화**: 기존 AI 문장 분석 prompt + 6000 단어 workbook PDF + 발음 가이드(오디오+PDF) + 한글 30일 챌린지 이메일 시리즈
- **3-5. 결제와 Digital Downloads embedding**: 강의 결제와 eBook 구매 모두 koreanwithji.com 안에서 처리되게 (결제 처리는 강의 플랫폼 백엔드)

**필요 역량**: 빌더가 vibe coding 도구면 코드 검수와 수정. Python 비중은 낮지만 프로그래밍 언어가 어떻게 작동하는지 개념은 알아야 한다. SEO와 AEO 기초(코드보다 콘텐츠 작업).

---

### Phase 4: 마케팅 본격화
**상세 계획 단일 출처**: [`04_marketing/marketing_plan.md`](../04_marketing/marketing_plan.md)

- **4-1. 소셜미디어 재활성**: 완성된 강의 스크립트 기반 콘텐츠 무한 생산. 영상 편집 자동화 필수. YouTube 롱폼용 Agent(SEO Title/Description + Thumbnail). TikTok/Meta/YouTube API로 스케줄링 자동화. Build in Public 콘텐츠는 유료강의 Teaser 역할
- **4-2. Skool community 개설**: 무료 공개분 선정(기본은 Intro + Hangul + Numbers, Level 1 일부는 검토 중). Skool API + RAG Agent 연결(24/7 답변 Bot). Obsidian Wiki가 base data
- **4-3. Funnel 완성**: 이메일 시퀀스, 구간별 Movement Trigger, Manychat Instagram 자동응답, 블로그 SEO와 AEO
- **4-4. 결정 필요**: Skool 무료 강의를 YouTube에도 롱폼으로 올릴지. 올린다면 차이를 어떻게 둘지(예: YouTube는 일부, Skool은 풀버전 + 워크북 + AI Bot 접근)

**필요 역량**: LangChain RAG(벡터 스토어, embeddings, retrieval), 소셜 API, Skool API, Webhook + Telegram/WhatsApp API, 이메일 도구 API

---

### Phase 5: 운영 안정화와 고도화
- AI 한국어 첨삭
- 학습 데이터 기반 개인화 추천
- 비즈니스 모델 확장 (하이브리드 + Anchor Pricing)
- CS 챗봇 (환불, 문의 자동 응대)
- Affiliate program 운영
- 광고 캠페인 (Paid ads + Hidden Landing 활용)

---

## 3. 사업 전체 기술 스택

> 코스 제작 전용 스택(Obsidian LLM Wiki, 영상 제작 자동화)은 여기 없다. [`02_course_creation/course_tech_stack.md`](../02_product/02_course_creation/course_tech_stack.md)가 단일 출처다.
> tech 자체를 공부하거나 참고 문서를 찾을 때는 [`03_tech/03_tech.md`](../03_tech/03_tech.md)를 본다.

### 3-1. 채널별 도구

| 레이어 | 도구 | 결정 상태 | 비고 |
|---|---|---|---|
| 메인 사이트 (koreanwithji.com) | 미정 | TBD | 요건은 아래 3-2 |
| 커뮤니티 | Skool (Hobby plan) | 확정 | 월 $9 운영자 비용 |
| 강의 플랫폼 | Teachable (유력) | 잠정 | Thinkific 등 대안 검토 가능. eBook Digital Downloads도 같은 플랫폼 |
| 결제 | 강의 플랫폼 자체 결제 시스템 사용 (koreanwithji.com에 결제 embed) | 확정 방향 | 강의 플랫폼이 처리, 사이트에 embed |
| 이메일 마케팅 | 미정 | TBD | ConvertKit / MailerLite / Beehiiv / Loops 비교 필요 |
| Instagram 자동응답 | Manychat | 유력 | 댓글에서 DM으로 자동화 |
| 강의 Draft 작성 | Obsidian LLM Wiki | 확정 | 상세는 [`course_tech_stack.md`](../02_product/02_course_creation/course_tech_stack.md) |
| 영상 합성 자동화 | HeyGen + 모션 그래픽 도구 + Replicate | 확정 방향 | 도구 후보와 미정 항목은 [`course_tech_stack.md`](../02_product/02_course_creation/course_tech_stack.md) |
| Skool AI Bot | LLM API + LangChain RAG | 확정 방향 | Phase 4 진입 시. Obsidian Wiki가 base data |
| 도메인 | Cloudflare | 확정 | koreanwithji.com |
| 분석 | Google Analytics | 확정 방향 | 무료 |
| Human-in-the-loop | Telegram 또는 WhatsApp | 잠정 | AI Bot 답변 컨펌용 |

### 3-2. 메인 사이트 빌더 요건

후보는 아래를 **모두** 만족해야 한다.

1. **Multimodal 프롬프트 지원**: 손그림 UI 스케치 첨부 가능
2. **Vibe coding 지원**: Claude Code 등 AI 코딩 에이전트와 호환
3. **Drag & Drop 빌더 동시 지원**: vibe coding 결과를 시각적으로 후처리
4. **외부 결제 위젯 embedding 지원**: 강의 결제와 Digital Downloads 위젯 삽입
5. **Hidden 페이지 지원**: 메뉴 노출 없이 URL 직접 접근 가능한 광고용 랜딩
6. **백엔드 관리 용이**: 관리가 기술적으로 복잡하지 않고 보안 취약점이 없어야 함
7. **반응형 UI 지원**: 모바일용 UI 지원이 되어야 함.
8. **챗봇 지원**: Site Navigation, 환불 등 지원하는 Agent Chatbot 기능이 있어야 함.

**후보군**: Webflow + Webflow AI / Framer + Framer AI / WordPress + Claude Code + Bricks·Elementor / Lovable·v0·Bolt

---

## 4. Phase별 AI Agent 설계

| Agent | 역할 | Phase | 도구 |
|---|---|---|---|
| 강의 Draft 생성 | Obsidian Wiki 기반 레슨별 Draft 작성 | Phase 1 (핵심) | Obsidian + Claude Code |
| 영상 합성 자동화 | 한글 모션 그래픽 + voiceover | Phase 1 (핵심) | HeyGen + Remotion(or HeyFrames) + Replicate + Python |
| eBook 생성 | 완성 스크립트를 eBook으로 재구성 | Phase 2 | Obsidian Wiki 기반 |
| 콘텐츠 Repurposing | 강의를 숏폼·롱폼·블로그 멀티포맷으로 | Phase 4 | Obsidian Wiki, LangChain |
| YouTube Title/Thumbnail | SEO 최적화 Title + Description | Phase 4 | Obsidian Wiki, LangChain |
| 소셜 스케줄링 Bot | TikTok/Meta/YouTube 자동 포스팅 및 포스팅 스케쥴링 | Phase 4 | Python + API |
| Skool AI Bot (RAG) | 24/7 학생 질문 답변 | Phase 4 | Obsidian Wiki, LangChain |
| 이메일 시퀀스 | 개인화 이메일 작성 | Phase 4 | LangChain |
| CS 챗봇 | 환불, 문의 자동 응대 | Phase 5 | TBD |
| AI 첨삭 | 학생 작문 자동 첨삭 | Phase 5 | TBD |
| 개인화 추천 | 학습 데이터 기반 추천 | Phase 5 | TBD |

### 4-1. Skool AI Bot 구조 (Phase 4 핵심)

```
학생 질문 (Skool 포럼)
    ↓
Python Bot이 Skool API로 수신
    ↓
LangChain RAG로 강의 자료 검색 (Obsidian Wiki .md가 base data)
    ↓
LLM API로 Ji 스타일 답변 생성
    ↓
Ji에게 검토 요청 (Telegram 또는 WhatsApp)
    ↓
Ji 컨펌 후 Skool 포럼에 자동 답글
```

**RAG를 쓰는 이유**: 자료 업데이트가 잦아 fine-tuning은 비용과 시간이 비싸다. RAG는 vector store만 갱신하면 즉시 반영된다. Phase 1에서 Obsidian Wiki로 이미 정제된 자료를 넣기 때문에 RAG 품질도 높아진다.

---

## 5. Ji가 사업을 위해 알아야 하는 것

### 5-1. 학습 우선순위 판단 기준

Python이나 AI 학습 플랜을 짤 때 이 순서를 기준으로 삼는다.

1. **Phase 1(코스 완성)에 직접 쓰이는 능력 = 최우선**
   - Obsidian Wiki 운영, Claude API와 Structured output, Remotion, TTS, 배치 처리, HeyGen API
   - Context Engineering, Harness Engineering
   - **LangChain은 Phase 1에 불필요. Phase 4 시점에 배운다**
2. **Phase 4(마케팅)에 쓰이는 능력 = 그 다음**
   - LangChain RAG와 Agent, Skool API, 소셜미디어 API, 이메일 도구 API

### 5-2. 구체적으로 배워야 하는 것
- Obsidian + LLM Wiki 설정 및 운영 (Phase 1 핵심)
- Claude Code 심화: CLAUDE.md, Memory, Skills, MCP, Agent 설계 (참고자료는 `03_tech/`)
- Remotion 사용법 (영상 모션 그래픽)
- HeyGen API 또는 UI
- Manychat, TikTok/Meta/YouTube API (Phase 4)

---

## 6. 미정 사항 (결정 우선순위)

### Phase 1 진행 중 결정
1. 비즈니스 모델과 가격 정책 (정가, 얼리버드, 환불)
2. Course 가격 (월 $48 선에서 월별·6개월·1년 플랜 설정), eBook 가격($12~15 안에서 확정)
3. Skool 무료 공개 범위 (Intro + Hangul + Numbers + Level 1 일부?)

### Phase 3 진입 전
4. 메인 사이트 빌더 선택
5. 이메일 마케팅 도구 선택
6. 강의 운영 플랫폼 최종 선택 (낮은 결제 수수료, Affiliate Program 지원 필수)

### Phase 4 진입 전
7. Skool 무료 강의를 YouTube에도 올릴지, 올린다면 차별화 방식
8. Manychat 키워드 설계
9. SEO와 AEO 콘텐츠 전략

> 코스 제작 과정 내부의 결정 사항(생성 방식, 영상 도구 등)은 여기 없다. [`02_course_creation.md`](../02_product/02_course_creation/02_course_creation.md)가 관리한다.

---

## 7. 핵심 원칙

1. **코스가 모든 것의 축**: 강의 콘텐츠 완성이 모든 Repurposing의 원천이다. Phase 1 최우선.
2. **역할은 명확하되 단일일 필요는 없다**: 한 채널이 여러 역할을 가져도 된다. 단 사용자가 헷갈리면 안 된다.
3. **이메일이 모든 채널의 공통 ID**: 진입 경로, 단계, 행동 이력을 전부 이메일로 추적한다.
4. **사용자 이동에는 반드시 명분**: SIP 원칙 (Specific, Immediate, Personal).
5. **Skool은 무료 유지**: 유료로 가면 funnel이 깨진다.
6. **Draft 작성 도구는 Obsidian LLM Wiki**: LangChain 학습 곡선 없이 착수 가능하고 품질도 더 높다 (종합력 + brand voice 일관성).
7. **LangChain은 Phase 4에서 배운다**: Skool Bot의 실시간 vector search에 필요하다.
8. **메인 사이트는 §3-2의 6요건을 충족하는 빌더로**.
9. **영상 모션 그래픽은 Remotion으로**: MoviePy, Pillow, CV2 학습은 불필요. Python은 API 호출과 배치 오케스트레이션만 담당한다.
10. **Human-in-the-loop 유지**: AI Bot 답변은 Ji 컨펌 후 발신한다 (브랜드 톤 보호).
11. **Build in public**: Phase 1 진행 자체를 콘텐츠화하면 Phase 3~4 진입 시 청중이 이미 워밍업돼 있다.
