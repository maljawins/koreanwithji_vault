# Preston Chin | How To Explain Anything To Anyone (The 4MAT Method)

## 확인 필요

검증 실패 결과다. Ji 검수 전 설명 방법의 근거로 사용하지 않는다.

원본: https://youtu.be/YZjWuFVSjjM

- 원본 대조 실패: 관찰 E0000_0001의 본문에 4번째 질문인 'And what if I apply this?'가 포함되어 있고 프레임(V00000038, 19.0초)도 지정되어 있으나, 해당 발화가 등장하는 A00003(17.28~23.10초)이 audio_ids에서 누락되었으며 quote에도 해당 문장이 누락되었습니다.; 관찰 E0000_0001 내용 중 발표자가 프레임워크 이름을 말로 언급하는 부분('구두 발음 Format')은 42.96초의 발화(A00008: 'This framework is called Format.')에서 나오지만, 근거 audio_ids에 A00008이 포함되지 않았고 인용문도 누락되었습니다.

## 변환 응답 원문 (extract_0000.json)

```json
{
  "observations": [
    {
      "kind": "condition",
      "title": "설명 프레임워크의 적용 목적 및 문제 상황 대조",
      "content": "발표자는 프레젠테이션 시 두서없이 횡설수설하거나(rambling) 청중의 주의를 잃는(losing the room) 상황을 방지하고 청중이 집중하여 듣게 만들기 위한 전제로 4단계 프레임워크를 제시한다. 영상에서는 좌절하며 얼굴을 감싸 쥐는 청중의 연출 장면을 교차 편집하여 설명 실패 상황을 시각적으로 대조한다.",
      "basis": "speaker_claim",
      "time": 5.18,
      "audio_ids": [
        "A00001"
      ],
      "quote": "so people actually listen to you. No more rambling, no more losing the room,",
      "frame_ids": [
        "V00000014",
        "V00000015",
        "V00000017",
        "V00000018"
      ]
    },
    {
      "kind": "method",
      "title": "4단계 설명 프레임워크(4MAT)의 질문 시퀀스",
      "content": "발표자는 어떤 대상이든 설명할 수 있는 구조로 4가지 질문에 순서대로 답하는 프레임워크(구두 발음 Format, 화이트보드 표기 4 MAT)를 소개한다. 순서는 1단계 'Why does this matter?'(왜 이것이 중요한가?), 2단계 'What is this?'(이것은 무엇인가?), 3단계 'How do we use it?'(어떻게 활용하는가?), 4단계 'And what if I apply this?'(적용 시 결과는 무엇인가?)로 이어진다. 화면에서는 화이트보드 4분면 필기 및 손가락 제스처, 메모지 그래픽을 통해 순서를 시각화한다.",
      "basis": "speaker_claim",
      "time": 9.8,
      "audio_ids": [
        "A00002"
      ],
      "quote": "just four simple questions you need to answer. Why does this matter? What is this? How do we use it?",
      "frame_ids": [
        "V00000002",
        "V00000004",
        "V00000020",
        "V00000024",
        "V00000025",
        "V00000038"
      ]
    }
  ]
}
```
