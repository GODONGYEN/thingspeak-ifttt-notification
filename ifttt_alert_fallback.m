% ThingHTTP 저장 장애 시 사용할 대체안: React -> MATLAB Analysis -> IFTTT
% 과제의 ThingHTTP 방식과 다릅니다. 현재 계정에서 저장/실행한 코드는 아닙니다.
% 개인 키는 ThingSpeak의 비공개 MATLAB Analysis 편집기에만 입력하세요.

eventName = 'Thingspeak_Alert';
webhookKey = 'REPLACE_WITH_PRIVATE_IFTTT_KEY';

if strcmp(webhookKey, 'REPLACE_WITH_PRIVATE_IFTTT_KEY')
    error('IFTTT:MissingKey', '비공개 편집기에서 본인 IFTTT 키를 입력하세요.');
end

webhookUrl = ['https://maker.ifttt.com/trigger/' eventName '/with/key/' webhookKey];
try
    response = webread(webhookUrl, weboptions('Timeout', 20));
catch
    % 예외 메시지에 개인 Webhook URL이 노출되지 않도록 새 메시지를 사용합니다.
    error('IFTTT:RequestFailed', 'IFTTT 요청 실패. 계정과 Webhook 연결을 확인하세요.');
end
disp(response);
