# ThingSpeak와 IFTTT를 이용한 휴대폰 알림

ThingSpeak 채널에 기록한 가변저항값이 **700을 초과할 때** IFTTT 앱으로 알림을 보내는 실습입니다. 채널 데이터 저장, 조건 판단, Webhook 호출, 모바일 알림의 연결 과정을 정리했습니다.

> **진행 상태 · 2026년 11월 23일:** IFTTT Applet을 생성하고 직접 호출로 Webhooks·Notifications 실행을 확인했습니다. 채널에 API Request로 500·700·900을 기록하고 entry ID 20·21·22를 확인했습니다. **ThingHTTP 저장은 HTTP 503 오류로 완료하지 못했습니다.** 원래 경로의 React 연동 및 휴대폰 수신 확인은 진행 중입니다.

## 1. 동작 원리

```mermaid
flowchart LR
  A[API Request로 Field 1 기록] --> B[ThingSpeak 채널]
  B --> C{React: Field 1 > 700}
  C -->|참으로 전환| D[ThingHTTP]
  C -->|거짓| E[추가 동작 없음]
  D --> F[IFTTT Webhooks]
  F --> G[스마트폰 IFTTT 앱 알림]
```

이번 실습은 API URL로 값을 직접 기록하므로 Arduino나 센서를 연결하지 않아도 조건 알림을 시험할 수 있습니다. 직접 입력한 값은 실제 센서 측정값과 구분합니다.

## 2. 실습 대상과 설정안

| 항목 | 값 |
|---|---|
| ThingSpeak 채널 | 기존 채널 `hi` |
| Channel ID | `3565315` |
| Field 1 | `가변저항값` |
| Field 2 | `LED 상태값` · 이번 시험에서는 수정하지 않음 |
| 알림 조건 | Field 1 **> 700** |
| IFTTT Event Name | `Thingspeak_Alert` |
| ThingHTTP 이름 | `IFTTT_Thingspeak_Alert` |
| React 이름 | `Pot_Over_700_Notification` |

기준값 700은 이번 실습용으로 정했습니다. `>` 비교이므로 정확히 700일 때는 알림 조건을 만족하지 않습니다.

## 3. IFTTT Applet 설정

1. [IFTTT](https://ifttt.ai/)에 로그인하고 **Create**에서 Applet을 만듭니다.
2. **If This → Webhooks → Receive a web request**를 선택합니다.
3. Event Name에 `Thingspeak_Alert`를 입력합니다. **Receive a web request with a JSON payload**와 구분합니다.
4. **Then That → Notifications → Send a notification from the IFTTT app**을 선택합니다.
5. 알림 문구를 다음과 같이 지정하고 Applet을 활성화합니다.

```text
ThingSpeak 알림: 가변저항값이 기준값 700을 초과했습니다!
```

실제로 생성한 Applet의 이름은 `ThingSpeak 가변저항 700 초과 알림`, ID는 `uEeqPN2f`입니다. 저장된 이벤트와 알림 문구를 편집 화면에서 다시 확인했습니다.

![저장된 Webhooks 이벤트](evidence/01-ifttt-trigger.jpg)

![저장된 Notifications 알림 문구](evidence/02-ifttt-notification-action.jpg)

![Applet Connected 상태](evidence/03-ifttt-connected.jpg)

휴대폰의 IFTTT 앱에도 같은 계정으로 로그인하고 알림을 허용합니다. Webhooks 서비스의 **Documentation**에서 개인 키와 호출 주소를 확인합니다. 서비스 화면과 이용 가능 범위는 현재 계정에서 확인합니다.

```text
https://maker.ifttt.com/trigger/Thingspeak_Alert/with/key/<IFTTT_WEBHOOK_KEY>
```

이 주소로 직접 호출하면 **조건 검사 없이** Applet 연결만 시험합니다. 응답이 성공이어도 휴대폰에서 알림이 도착했는지 별도로 확인합니다. [IFTTT Webhooks 설명](https://ifttt.ai/maker_webhooks)

2026년 11월 23일 19:40(한국 시간)에 직접 호출했고, 성공 응답과 IFTTT 실행 이력의 `Trigger ran`, `Action ran`을 확인했습니다. [직접 호출 기록](evidence/ifttt-direct-test.json)

![Webhook 직접 호출 성공 응답](evidence/04-webhook-success.jpg)

![IFTTT 직접 호출 실행 이력](evidence/07-ifttt-direct-activity.jpg)

## 4. ThingHTTP 연결

ThingSpeak의 **Apps → ThingHTTP → New ThingHTTP**에서 다음과 같이 설정합니다.

| 항목 | 입력 |
|---|---|
| Name | `IFTTT_Thingspeak_Alert` |
| URL | 위 Webhooks 주소의 키를 본인 키로 치환한 실제 주소 |
| Method | `GET` |
| HTTP Version | `1.1` |
| HTTP Auth Username / Password | 비워 둠 |
| Content Type / Host / Headers / Body / Parse String | 비워 둠 |

**Save ThingHTTP**로 저장합니다. ThingHTTP는 IFTTT 호출을 담당하고, 센서값 비교는 다음 단계의 React가 담당합니다. [ThingHTTP 공식 문서](https://www.mathworks.com/help/thingspeak/thinghttp-app.html)

### 실제 저장 시 발생한 오류

요청 `238493`의 편집 화면에 위 값을 입력했지만 저장 시 `HTTP ERROR 503`이 발생했습니다. 새 편집 화면과 빈 헤더 정리 후에도 같은 오류가 나타났고, 목록에서 이름이 여전히 `Request 238493`인 것을 확인했습니다. 따라서 ThingHTTP 연결 저장 성공으로 표시하지 않았습니다.

![ThingHTTP 저장 시 HTTP 503 오류](evidence/05-thinghttp-503.jpg)

[MathWorks 문답](https://www.mathworks.com/matlabcentral/answers/2185362-thinghttp-save-delete-returns-http-error-503)에는 11월 18일 동일한 저장 오류가 보고되었고, 11월 21일에도 계속된다는 후속 글이 있습니다. 답변에는 MATLAB Analysis의 `webread`를 이용한 대체 방식이 제안되어 있습니다. [상태 페이지](https://status.mathworks.com/)는 확인 당시 정상으로 표시되어, 현재 오류와 전체 서비스 상태를 구분했습니다.

## 5. React 조건 등록

**Apps → React → New React**에서 설정합니다.

| 항목 | 입력 |
|---|---|
| React Name | `Pot_Over_700_Notification` |
| Condition Type | `Numeric` |
| Test Frequency | `On Data Insertion` |
| If channel | `hi (3565315)` |
| Field | `1 (가변저항값)` |
| 비교 | `is greater than` |
| 기준값 | `700` |
| Action | `ThingHTTP` |
| then perform ThingHTTP | `IFTTT_Thingspeak_Alert` |
| Options | `Run action only the first time the condition is met` |

**Save React**로 저장합니다. 이 옵션은 조건이 거짓이었다가 참이 될 때 실행하므로, 900 이후 950을 기록해도 반복 알림을 방지합니다. 이후 500으로 내린 뒤 900으로 올리면 다시 실행 대상이 됩니다. [React 공식 문서](https://www.mathworks.com/help/thingspeak/react-app.html)

## 6. API Request로 값 기록

채널의 **API Keys → API Requests → Write a Channel Feed** 주소에서 `field1`을 변경합니다. 채널의 **Write API Key**를 사용하며, IFTTT 키나 ThingHTTP 키와 구분합니다.

```text
https://api.thingspeak.com/update?api_key=<THINGSPEAK_WRITE_API_KEY>&field1=500
https://api.thingspeak.com/update?api_key=<THINGSPEAK_WRITE_API_KEY>&field1=700
https://api.thingspeak.com/update?api_key=<THINGSPEAK_WRITE_API_KEY>&field1=900
```

요청은 한 번에 하나씩 보내고, 실습에서는 사이에 **20초 이상** 간격을 둡니다. 무료 라이선스의 채널 갱신 최소 간격은 15초이며 계정별 제한을 따릅니다. 응답이 양의 정수이면 새 `entry_id`, `0`이면 기록 실패입니다. `200 OK`만으로 기록 성공을 판단하지 않습니다. [데이터 기록 API](https://www.mathworks.com/help/thingspeak/writedata.html), [API 제한](https://www.mathworks.com/help/thingspeak/channel-control.html)

### 시험 순서와 예상 결과

| 순서 | 입력 Field 1 | 조건 | 예상 추가 알림 | 실제 결과 |
|---|---:|---|---|---|
| 1 | 500 | 거짓 | 없음 · 초기화 | 저장 성공 · entry 20 / 알림 시험 전 |
| 2 | 700 | 거짓 | 없음 · 경계값 | 저장 성공 · entry 21 / 알림 시험 전 |
| 3 | 900 | 참으로 전환 | 1회 실행 대상 | 저장 성공 · entry 22 / 알림 시험 전 |
| 4 | 950 | 참 유지 | 없음 | 미실행 |
| 5 | 500 | 거짓으로 복귀 | 없음 · 재무장 | 미실행 |
| 6 | 900 | 다시 참으로 전환 | 1회 실행 대상 | 미실행 |

실제 API 기록은 2026년 11월 23일 한국 시간 19:31:12, 19:31:49, 19:32:20에 수행했습니다. [기록 결과](evidence/live-channel-writes.json)는 공개 채널의 feed 조회로 재확인했습니다. **이때 React는 아직 등록 전이므로 알림 연동 시험은 아닙니다.** React 저장 후 첫 단계부터 다시 시험합니다.

알림 도착 시간은 서비스나 휴대폰 상태에 따라 달라질 수 있습니다. 입력 시각, 새 entry ID, IFTTT 실행 이력, 휴대폰 알림을 함께 비교합니다.

### 선택 사항 · Python으로 같은 시험 실행

Python 3 표준 라이브러리만 사용하는 [test_channel.py](test_channel.py)를 제공합니다. 기본 실행은 계획을 출력하며 네트워크 요청을 보내지 않습니다.

```sh
python3 test_channel.py
python3 test_channel.py --execute
```

`--execute`는 해당 채널에 위 여섯 값을 실제로 기록합니다. 실행 중 해당 채널의 Write API Key를 숨김 입력하며, 20초 간격으로 기록합니다. 로그는 키를 제외하고 `evidence/channel-writes-실행시각.json`에 저장합니다. 이 로그는 **채널 기록 성공**만 증명하며 모바일 알림 수신 증거는 아닙니다.

## 7. 제출 전 확인할 증빙

- [x] Applet의 Webhooks 이벤트와 Notifications 액션
- [x] Applet 활성 상태
- [ ] ThingHTTP 연결 저장 화면 · 모든 키 가림
- [ ] React의 채널·필드·비교식·실행 옵션
- [x] 500·700·900 기록 결과와 entry ID
- [ ] IFTTT 실행 이력과 휴대폰의 실제 알림
- [ ] 실제 시험 결과로 위 표 갱신
- [x] GitHub 자료 공개
- [ ] 실제 연동 확인 후 과제 게시글에 링크 제출

알림 화면에는 이번 실습 문구와 시각이 보이도록 하고, 참고 링크의 타인 화면을 본인 결과로 사용하지 않습니다. 공개 자료에는 Webhook 키, 채널 Write/Read API Key, ThingHTTP 키를 넣지 않습니다.

## 8. 알림이 오지 않을 때

1. 채널 기록 응답이 `0`이면 Write API Key, 기록 간격, 활성 필드를 확인합니다.
2. 채널에 900이 저장되었는지 확인한 뒤 React의 `> 700`, `On Data Insertion`, 연결된 ThingHTTP를 점검합니다.
3. 첫 전환 옵션을 사용 중이면 500을 기록하고 간격을 둔 뒤 900으로 다시 시험합니다.
4. IFTTT 이벤트의 대소문자, Applet 활성 상태와 실행 이력을 확인합니다.
5. 휴대폰 앱 계정과 OS 알림 허용, 집중 모드 등을 확인합니다.

## 참고 자료

- [사용자가 제공한 실습 예시](https://github.com/boheechoi05/arduino/issues/4)
- [MathWorks의 ThingSpeak와 IFTTT 연동 예제](https://www.mathworks.com/help/thingspeak/use-ifttt-to-send-text-message-notification.html)

참고 예시의 설정 흐름을 바탕으로, 본인 채널의 가변저항 필드와 경계값·반복 알림 시험을 추가했습니다.
