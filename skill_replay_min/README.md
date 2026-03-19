# Replay Min Skill

A minimal reusable skill package to reproduce `encrypted` generation and replay the `gettaskbyTypeCursor` request.

## Files

- `SKILL.md`: Skill instructions and usage.
- `replay_min.py`: Minimal runnable script.
- `requirements.txt`: Python dependencies.

## Quick Start

```bash
pip install -r requirements.txt
python replay_min.py
```

## What It Reproduces

- AES-128-ECB + PKCS7
- JSON payload: `{\"verify\":\"zzyq\",\"c_time\":\"...\"}`
- Ciphertext output: uppercase hex
- POST `application/x-www-form-urlencoded` to:
  - `https://www.yqtech.ltd:8802/gettaskbyTypeCursor`
