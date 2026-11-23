# 검증 상태

확인일: 2026년 11월 23일 · 한국 시간

| 항목 | 확인 결과 |
|---|---|
| ThingSpeak 로그인 | 브라우저에서 로그인 상태 확인 |
| 기존 채널 | `hi`, ID `3565315` |
| 기존 필드 | Field 1 `가변저항값`, Field 2 `LED 상태값` 활성 상태 확인 |
| ThingHTTP | New ThingHTTP로 요청 `238493` 생성, 편집 화면 준비. URL 연결 및 저장 전 |
| IFTTT | 로그인 완료 |
| Applet 생성 및 활성화 | `ThingSpeak 가변저항 700 초과 알림`, ID `uEeqPN2f`, Connected 확인 |
| 저장된 Applet 내용 | `Thingspeak_Alert` 이벤트와 한국어 알림 문구 재확인 |
| React 조건 저장 | 미완료 |
| API 데이터 기록 | 500·700·900 저장 성공 · entry ID 20·21·22 |
| API 저장 재확인 | 공개 채널 feed에서 값과 entry ID 재조회 완료 |
| 휴대폰 알림 수신 | 미확인 |
| 시험 도구 미리보기 | 통과 · 네트워크 요청 없음 |
| 시험 도구 응답 처리 | 모의 응답으로 정상·실패 판정 확인 |
| 시험 도구 실행 흐름 | 모의 요청으로 6회 기록, 간격, 키 없는 로그 확인 |

실제 API 기록은 한국 시간 19:31:12, 19:31:49, 19:32:20에 브라우저에서 API Request URL로 수행했습니다. 키를 제외한 기록은 [live-channel-writes.json](live-channel-writes.json)에 있습니다. React 등록 전 기록이므로 알림 연동 성공을 뜻하지 않습니다.

모의 시험은 스크립트 동작 확인입니다. ThingHTTP 연결과 React를 저장한 뒤 전체 시험을 다시 진행합니다.

공개 GitHub 자료: https://github.com/GODONGYEN/thingspeak-ifttt-notification
