#!/usr/bin/env python3
"""Preview or write the six assignment values. No third-party dependencies."""

import argparse
import getpass
import json
from pathlib import Path
import sys
import time
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent


def write_value(api_key, value, expected_channel):
    # Keep the key out of the URL, shell history, output, and evidence file.
    payload = urlencode({"api_key": api_key, "field1": value}).encode("ascii")
    request = Request(
        "https://api.thingspeak.com/update.json",
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        raise RuntimeError(f"HTTP {error.code}: 채널 기록 실패") from None
    except (URLError, TimeoutError, OSError):
        raise RuntimeError("통신 실패: 채널 기록 여부를 웹에서 확인하세요. 자동 재시도하지 않습니다.") from None
    except (ValueError, UnicodeError):
        raise RuntimeError("응답을 해석할 수 없습니다. 채널 기록을 웹에서 확인하세요.") from None

    if not isinstance(result, dict):
        raise RuntimeError("채널 기록 실패(0 또는 예상하지 못한 응답). 키와 기록 간격을 확인하세요.")
    if result.get("channel_id") != expected_channel:
        raise RuntimeError("응답 채널 ID가 다릅니다. 다른 채널에 1건 기록되었을 수 있으므로 키를 확인하세요.")
    entry_id = result.get("entry_id")
    if not isinstance(entry_id, int) or isinstance(entry_id, bool) or entry_id <= 0:
        raise RuntimeError("양의 entry_id가 없습니다. 채널 기록을 확인하세요.")
    if str(result.get("field1")) != str(value):
        raise RuntimeError("응답의 Field 1이 요청값과 다릅니다. 채널을 확인하세요.")
    return {
        "channel_id": expected_channel,
        "entry_id": entry_id,
        "field1": value,
        "created_at": result.get("created_at"),
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
    }


def save_log(path, records, completed, error=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "scope": "채널 기록 결과만 확인. IFTTT 실행 및 휴대폰 알림은 별도 확인 필요.",
        "completed": completed,
        "writes": records,
    }
    if error:
        report["error"] = error
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description="ThingSpeak 알림 과제용 API 입력 시험")
    parser.add_argument("--execute", action="store_true", help="계획 대신 실제 채널에 값을 기록")
    args = parser.parse_args(argv)
    config = json.loads((ROOT / "settings.example.json").read_text(encoding="utf-8"))
    values = config["test_values"]
    channel = config["channel_id"]
    threshold = config["threshold"]
    interval = max(20, config["write_interval_seconds"])
    previous = None
    print(f"채널 {channel} / Field 1 > {threshold} / 기록 간격 {interval}초")
    for value in values:
        current = value > threshold
        trigger = current and previous is False
        print(f"  field1={value}: {'실행 대상' if trigger else '추가 실행 없음'} (예상)")
        previous = current
    if not args.execute:
        print("미리보기 완료: 네트워크 요청 없음. 실제 실행은 --execute를 사용하세요.")
        return 0

    print("위 채널에 6건을 실제로 추가합니다. 해당 채널의 Write API Key만 입력하세요.")
    key = getpass.getpass("Write API Key (숨김 입력, 취소는 Ctrl+C): ").strip()
    if not key:
        parser.error("Write API Key가 비어 있습니다.")
    records = []
    # A new log per run avoids replacing earlier evidence.
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    log_path = ROOT / "evidence" / f"channel-writes-{stamp}.json"
    try:
        for index, value in enumerate(values):
            if index:
                time.sleep(interval)
            record = write_value(key, value, channel)
            records.append(record)
            save_log(log_path, records, False)
            print(f"기록 성공: field1={value}, entry_id={record['entry_id']}", flush=True)
    except (RuntimeError, KeyboardInterrupt) as error:
        message = str(error) if isinstance(error, RuntimeError) else "사용자 중단"
        save_log(log_path, records, False, message)
        print(f"중단: {message}\n로그: {log_path}", file=sys.stderr)
        return 1
    save_log(log_path, records, True)
    print(f"6건 기록 완료. IFTTT 실행 이력과 휴대폰 알림을 확인하세요.\n로그: {log_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\n사용자 중단", file=sys.stderr)
        raise SystemExit(130)
