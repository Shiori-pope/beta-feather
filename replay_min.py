#!/usr/bin/env python3
"""Minimal reproduction for gettaskbyTypeCursor encrypted + request."""

import json
from datetime import datetime, timezone

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

BASE_URL = "https://www.yqtech.ltd:8802/gettaskbyTypeCursor"
AES_KEY = "1234512345123456"


def js_date_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def gen_encrypted(c_time: str) -> str:
    payload = json.dumps({"verify": "zzyq", "c_time": c_time}, separators=(",", ":"), ensure_ascii=False)
    cipher = AES.new(AES_KEY.encode("utf-8"), AES.MODE_ECB)
    return cipher.encrypt(pad(payload.encode("utf-8"), 16)).hex().upper()


if __name__ == "__main__":
    c_time = js_date_iso()
    encrypted = gen_encrypted(c_time)

    data = {
        "length": "9999999",
        "radioGroup": ["radio4", "radio40", "radio41", "radio42", "radio43"],
        "type": "0",
        "encrypted": encrypted,
        "c_time": c_time,
    }

    resp = requests.post(
        BASE_URL,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=20,
        verify=False,
    )

    print("status:", resp.status_code)
    try:
        print(json.dumps(resp.json(), ensure_ascii=False, indent=2))
    except Exception:
        print(resp.text)
