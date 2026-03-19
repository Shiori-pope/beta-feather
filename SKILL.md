# Replay Min Request Skill

## Purpose

Use this skill when you need to quickly reproduce the mini-program `encrypted` parameter and replay the `gettaskbyTypeCursor` API request in Python.

## Inputs

- `length` (default: `9999999`)
- `type` (default: `0`)
- `radioGroup` (default: `radio4 radio40 radio41 radio42 radio43`)
- `c_time` (auto-generated UTC ISO string if omitted)

## Algorithm

1. Build payload object: `{"verify":"zzyq","c_time":"<ISO time>"}`
2. JSON stringify with compact separators.
3. Encrypt with AES-128-ECB and PKCS7 padding.
4. Convert ciphertext to uppercase hex as `encrypted`.
5. Submit form POST to `https://www.yqtech.ltd:8802/gettaskbyTypeCursor`.

## Script

Run `replay_min.py` in this folder.

## Dependencies

- `requests`
- `pycryptodome`
