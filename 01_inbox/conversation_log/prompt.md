09-14
1. 커리큘럼맵에 Draft보유여부 칼럼 추가 완료

2. Ji Draft에도 Ref_No 칼럼 추가 완료

3. 02_course_creation 내부 폴더 구조 변경
 - 01_lesson_spec 및 하부 폴더 트리 신설에 따른 index 업데이트
  > topic_copy, raw, shaped 단계 작업 할 폴더 신설
 - 02_concept폴더 신설
  > 여기에 concept_index.xlsx 만들예정
 - brainstorm.md 4-2
 - Ji 레슨주제 → topic_copy

4. course_plan 문서정비 D-3 조치완료




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
10. `work_plan.md`를 `_archive`로 이동 (Ji 직접)
11. Koreanwithji 유튜브 md 변환 + 파이프라인 경로 정비 (위 To do)

## Q1. RAW_DIGEST를 spec_done에서 남길지 지울지

**결론: 남긴다. 너무 길어지면 그때 뗀다.**

- **정하는 것**: `topic_raw`에서 raw에서 뽑아온 원문 발췌를, 필드를 다 채운 뒤에도 spec 안에 계속 둘 것인가.
- **남기면**: 검수할 때 "이 teaching point가 어디서 나왔나"를 바로 옆에서 대조한다. Draft 쓸 때 예문 원본을 raw 폴더에서 다시 안 찾는다.
- **지우면**: spec이 짧아진다. 대신 근거를 다시 보려면 레슨당 중앙값 123KB짜리 raw를 다시 뒤져야 한다.
- **결정적인 이유**: 조준 발췌는 판단이 들어간 작업이라 **재현이 안 된다.** 지우면 그 판단이 사라지고, 나중에 필요해지면 사람이 처음부터 다시 한다.
- **치르는 값**: spec 1장이 2~3배 두꺼워진다. 발췌를 문서 맨 아래에 두면 위쪽 필드만 읽는 건 그대로 된다.
- **비유**: 요리 끝났다고 장 봐온 영수증을 버리는 것과 같다. 당장은 깔끔한데 "이 재료 어디서 샀지" 할 때 못 찾는다.
- **되돌릴 수 있는 방향이다**: 남겼다가 길면 떼면 된다. 지웠다가 되살리려면 발췌를 다시 해야 한다.