# 제출 댓글 초안

현재 확인된 결과를 기준으로 작성한 댓글 초안입니다. 아직 과제 게시글에 제출하지 않았습니다.

```text
ThingSpeak와 IFTTT를 이용한 모바일 알림 실습 자료입니다.

GitHub: https://github.com/GODONGYEN/thingspeak-ifttt-notification

IFTTT Applet 생성과 활성화를 완료하고, Webhook 직접 호출로
Webhooks 트리거와 Notifications 액션의 정상 실행을 확인했습니다.
ThingSpeak 채널에는 500·700·900을 기록하고 entry ID 20·21·22를 확인했습니다.

ThingHTTP 연결 저장은 HTTP 503 오류로 완료하지 못했습니다.
대신 React → MATLAB Analysis(webread) → IFTTT 경로를 구성했습니다.
500·700·900·950·500·900을 차례로 입력하고, 900 진입 시 자동 실행 2회와
950에서 중복 실행이 없는 것을 IFTTT 실행 이력으로 확인했습니다.
설정, 시험 결과, 오류와 대체 연동 증빙을 GitHub에 정리했습니다.
마지막 자동 시험 알림이 휴대폰에 도착한 것도 확인했습니다.
원래 과제의 ThingHTTP 경로는 저장 오류로 미완료이며, 대체 경로의 결과와 구분해 기록했습니다.
```

휴대폰 수신은 사용자 확인을 바탕으로 기록했습니다. 휴대폰 화면 캡처를 추가하려면 다른 알림이나 개인정보를 가린 뒤 첨부합니다.
