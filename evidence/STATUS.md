# 검증 상태

확인일: 2026년 11월 23일 · 한국 시간

| 항목 | 확인 결과 |
|---|---|
| ThingSpeak 로그인 | 브라우저에서 로그인 상태 확인 |
| 기존 채널 | `hi`, ID `3565315` |
| 기존 필드 | Field 1 `가변저항값`, Field 2 `LED 상태값` 활성 상태 확인 |
| ThingHTTP | 요청 `238493` 생성. 연결 저장 시 HTTP 503 반복 발생, 저장 미완료 |
| IFTTT | 로그인 완료 |
| Applet 생성 및 활성화 | `ThingSpeak 가변저항 700 초과 알림`, ID `uEeqPN2f`, Connected 확인 |
| 저장된 Applet 내용 | `Thingspeak_Alert` 이벤트와 한국어 알림 문구 재확인 |
| Webhook 직접 호출 | 성공 응답, IFTTT Trigger ran / Action ran 확인 · 19:40 KST |
| 대체 React 조건 저장 | `Pot_Over_700_Fallback`, ID `139875`, 활성 상태 |
| 대체 MATLAB Analysis | `IFTTT_Alert_Fallback`, ID `431384`, 코드 저장 확인 |
| API 데이터 기록 | 500·700·900 저장 성공 · entry ID 20·21·22 |
| API 저장 재확인 | 공개 채널 feed에서 값과 entry ID 재조회 완료 |
| 대체 자동 실행 | 19:52, 19:55 KST에 IFTTT 트리거 및 Notifications 액션 실행 확인 |
| 반복 실행 방지 | 700에서 실행 없음, 950에서 추가 실행 없음, 500 이후 900에서 재실행 확인 |
| IFTTT 총 실행 | 직접 1회 + 대체 경로 자동 2회 = 3회 |
| 휴대폰 알림 수신 | 19:55 KST 자동 시험 알림 도착을 사용자 확인. 휴대폰 캡처는 미첨부 |
| 시험 도구 미리보기 | 통과 · 네트워크 요청 없음 |
| 시험 도구 응답 처리 | 모의 응답으로 정상·실패 판정 확인 |
| 시험 도구 실행 흐름 | 모의 요청으로 6회 기록, 간격, 키 없는 로그 확인 |

실제 API 기록은 한국 시간 19:31:12, 19:31:49, 19:32:20에 브라우저에서 API Request URL로 수행했습니다. 키를 제외한 기록은 [live-channel-writes.json](live-channel-writes.json)에 있습니다. React 등록 전 기록이므로 알림 연동 성공을 뜻하지 않습니다.

대체 경로의 실제 기록은 [live-fallback-writes.json](live-fallback-writes.json)에 있습니다. entry 23~28의 값은 500, 700, 900, 950, 500, 900입니다. [fallback-activity.json](fallback-activity.json)은 IFTTT 실행 이력을 정리한 기록입니다.

원래 과제 경로의 ThingHTTP 저장은 HTTP 503으로 미완료입니다. 대체 경로는 서버의 자동 실행 2회와 마지막 실행의 휴대폰 수신을 확인했습니다. 현재 React는 대체 MATLAB Analysis를 실행하며, 마지막 시험값은 900입니다.

공개 GitHub 자료: https://github.com/GODONGYEN/thingspeak-ifttt-notification
