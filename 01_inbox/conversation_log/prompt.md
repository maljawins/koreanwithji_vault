09-15

1. 00_curriculum_and_index.md 신설

2. 01_lesson_spec.md 신설

위에 폴더명과 동일한 파일명으로 .md 만들었어.
- 01_lesson_spec 내 각 단계별 subfolder에는 에는 커리큘럼맵과 동일하게 레벨-레슨 별로 폴더트리를 만들예정
- 지금은 topic_copy 단계: 44개 레슨을 01_topic_copy 폴더 내 VSL, Hangul, Numbers, Level 1, Level 2 폴더 신설



4. 02_course_creation 내부 폴더 구조 변경
 - 01_lesson_spec 및 하부 폴더 트리 신설에 따른 index 업데이트
  > 01_topic_copy, 02_topic_raw, 03_topic_shaped 폴더 신설
  > spec_done 이전 각 단계별로 맞는 폴더로 작업 진행
 - 02_concept 폴더 신설
  > topic_shaped과 병행 / 여기에 concept_index.xlsx 만들예정
  > brainstorm.md 4-2 참조

5. 현재 상태로 새로운 git repo에다가 백업 완료

6.  RAW_DIGEST를 spec_done 단계에서 남길지 지울지 결정해야 한다는데 이게 무슨 말인지 설명해줘
 - 정확하게 RAW_DIGEST가 뭔지 그리고 어떤 형태로 남기려고 하는지 남겨야 하는지 VS 남기면 안 되는지 설명 및 비교해줘

7. 조치사항 반영해서 conversation_log 업데이트하고 각 지침 업데이트해줘.

7. 

Later

내 Koreanwithji 유튜브 채널에 있는 영상 md변환
 - korean_yt_md_guide.md 업데이트
 - korean_yt_md_pipeline.py 업데이트

---

## 다음 할 일 (260907 정리)

**A. Ji가 먼저 정할 것 (4건, 각 1분)**
1. RAW_DIGEST를 spec_done 단계에서 남길지 지울지 → template 확정에 필요
 - 남긴다. 하지만 애초에 topic_raw단계에서 transcript는 제외하고 가져온다. (추후 lesson design 디테일 손볼 때 필요할 때만 조회하여 "발췌"한다.)

2. 

**B. STEP 1 착수 (파일럿 44개 레슨: Hangul 6 + Numbers 7 + L1 21 + L2 10)**
5. lesson_spec template 확정 (필드 10개 + status 4단계)
6. `topic_copy` — V7 4번 컬럼을 레슨당 spec 1장으로 펴는 스크립트 작성·실행. 판단 없음, 검수 불필요
7. `topic_raw` — 조준 발췌. 발췌문 문자열 대조 검증 포함
8. `topic_shaped` — V7과 발췌 대조해 TEACHING_POINTS 확정. **Ji 검수 지점**
9. `spec_done` — concept_index.xlsx 작성 후 나머지 필드 표준명으로 채움

**C. 뒤로 미룬 것**

