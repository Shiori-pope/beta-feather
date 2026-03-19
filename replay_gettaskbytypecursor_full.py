#!/usr/bin/env python3
"""Fully reproduce encrypted generation and request replay for gettaskbyTypeCursor.

Install deps first:
    pip install requests pycryptodome

Example:
    python replay_gettaskbytypecursor_full.py \
        --length 9999999 \
        --type 0 \
        --radio-group radio4 radio40 radio41 radio42 radio43
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pprint import pprint
from typing import Any

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def js_new_date_iso() -> str:
    """Return an ISO8601 UTC string compatible with JS new Date JSON output."""
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def encrypt_hex_upper(
    verify_value: str,
    c_time: str,
    key: str,
) -> tuple[str, str]:
    """Replicate mini-program encrypted generation.

    JS equivalent:
        AES.encrypt(JSON.stringify({verify:"zzyq", c_time:new Date}), KEY,
                    {iv: IV, mode: ECB, padding: Pkcs7})
            .ciphertext.toString().toUpperCase()
    """
    payload_obj = {
        "verify": verify_value,
        "c_time": c_time,
    }
    payload_json = json.dumps(payload_obj, separators=(",", ":"), ensure_ascii=False)

    cipher = AES.new(key.encode("utf-8"), AES.MODE_ECB)
    encrypted_bytes = cipher.encrypt(pad(payload_json.encode("utf-8"), AES.block_size))
    encrypted_hex_upper = encrypted_bytes.hex().upper()

    return payload_json, encrypted_hex_upper


def parse_response_to_python_obj(resp: requests.Response) -> Any:
    """Parse response into Python object when possible."""
    try:
        return resp.json()
    except Exception:
        text = resp.text.strip()
        if not text:
            return ""
        try:
            return json.loads(text)
        except Exception:
            return text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Replay gettaskbyTypeCursor with fully reproduced encrypted")
    parser.add_argument("--base-url", default="https://www.yqtech.ltd:8802", help="API root URL")
    parser.add_argument("--path", default="gettaskbyTypeCursor", help="API path")

    parser.add_argument("--length", type=int, default=9999999)
    parser.add_argument("--type", type=int, default=0)
    parser.add_argument(
        "--radio-group",
        nargs="+",
        default=["radio4", "radio40", "radio41", "radio42", "radio43"],
        help="Values for radioGroup[]",
    )

    parser.add_argument("--verify-value", default="zzyq")
    parser.add_argument("--c-time", default="", help="If empty, auto-generate JS-style UTC ISO string")
    parser.add_argument("--key", default="1234512345123456")
    parser.add_argument("--iv", default="1234512345123456", help="Kept for parity (ECB does not use iv)")

    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--insecure", action="store_true", help="Disable TLS verification")
    return parser


def main() -> None:
    args = build_parser().parse_args()

    if len(args.key.encode("utf-8")) != 16:
        raise ValueError("AES key must be exactly 16 bytes for AES-128")

    c_time = args.c_time or js_new_date_iso()

    payload_json, encrypted = encrypt_hex_upper(
        verify_value=args.verify_value,
        c_time=c_time,
        key=args.key,
    )

    url = args.base_url.rstrip("/") + "/" + args.path.lstrip("/")
    form_data = {
        "length": str(args.length),
        "radioGroup": args.radio_group,
        "type": str(args.type),
        "encrypted": encrypted,
        "c_time": c_time,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
    }

    print("=" * 80)
    print("[1] Encrypted Generation")
    print("payload_json:", payload_json)
    print("encrypted:", encrypted)
    print("encrypted_len:", len(encrypted))
    print("=" * 80)
    print("[2] Request")
    print("url:", url)
    print("headers:")
    pprint(headers)
    print("form_data:")
    pprint(form_data)

    verify_tls = not args.insecure
    if args.insecure:
        requests.packages.urllib3.disable_warnings()  # type: ignore[attr-defined]

    try:
        resp = requests.post(
            url,
            data=form_data,
            headers=headers,
            timeout=args.timeout,
            verify=verify_tls,
        )
    except requests.exceptions.SSLError:
        print("TLS verify failed; retry once with verify=False ...")
        requests.packages.urllib3.disable_warnings()  # type: ignore[attr-defined]
        resp = requests.post(
            url,
            data=form_data,
            headers=headers,
            timeout=args.timeout,
            verify=False,
        )

    parsed = parse_response_to_python_obj(resp)

    print("=" * 80)
    print("[3] Response")
    print("status_code:", resp.status_code)
    print("resp_headers:")
    pprint(dict(resp.headers))
    print("resp_body_parsed:")
    pprint(parsed, width=120, sort_dicts=False)


if __name__ == "__main__":
    main()
