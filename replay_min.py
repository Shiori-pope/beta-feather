#!/usr/bin/env python3
"""北理贝塔驿站帖子浏览脚本（列表 + 详情）。"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from typing import Any

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

API_ROOT = "https://www.yqtech.ltd:8802"
AES_KEY = "1234512345123456"

TAB_TO_RADIO = {
    "all": ["radio4", "radio40", "radio41", "radio42", "radio43"],
    "tucao": ["radio4", "radio40"],
    "qingsu": ["radio41"],
    "xinyuan": ["radio42"],
    "zhihu": ["radio43"],
}


def js_date_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def gen_encrypted(c_time: str) -> str:
    payload = json.dumps({"verify": "zzyq", "c_time": c_time}, separators=(",", ":"), ensure_ascii=False)
    cipher = AES.new(AES_KEY.encode("utf-8"), AES.MODE_ECB)
    return cipher.encrypt(pad(payload.encode("utf-8"), 16)).hex().upper()


def parse_json_or_text(resp: requests.Response) -> Any:
    try:
        return resp.json()
    except Exception:
        return resp.text


def fetch_list(
    tab: str,
    sort_type: int,
    cursor: int,
    timeout: float,
    verify_tls: bool,
) -> dict[str, Any]:
    c_time = js_date_iso()
    encrypted = gen_encrypted(c_time)
    data = {
        "length": str(cursor),
        "radioGroup": TAB_TO_RADIO[tab],
        "type": str(sort_type),
        "encrypted": encrypted,
        "c_time": c_time,
    }
    resp = requests.post(
        f"{API_ROOT}/gettaskbyTypeCursor",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=timeout,
        verify=verify_tls,
    )
    body = parse_json_or_text(resp)
    if not isinstance(body, dict):
        raise RuntimeError(f"列表接口返回非 JSON: {body}")
    return body


def fetch_detail(post_id: int, timeout: float, verify_tls: bool) -> dict[str, Any]:
    c_time = js_date_iso()
    encrypted = gen_encrypted(c_time)
    params = {
        "pk": str(post_id),
        "encrypted": encrypted,
        "c_time": c_time,
    }
    resp = requests.get(
        f"{API_ROOT}/gettaskbyId",
        params=params,
        headers={"Accept": "application/json"},
        timeout=timeout,
        verify=verify_tls,
    )
    body = parse_json_or_text(resp)
    if not isinstance(body, dict):
        raise RuntimeError(f"详情接口返回非 JSON: {body}")
    return body


def print_list_page(task_list: list[dict[str, Any]], page_no: int) -> None:
    print(f"\n===== 第 {page_no} 页，数量: {len(task_list)} =====")
    for item in task_list:
        post_id = item.get("id", "")
        title = str(item.get("title", "")).replace("\n", " ").strip()
        c_time = item.get("c_time", "")
        radio = item.get("radioGroup", "")
        user = item.get("userName", "")
        like_num = item.get("likeNum", 0)
        comment_num = item.get("commentNum", 0)
        watch_num = item.get("watchNum", 0)
        print(
            f"[{post_id}] {title} | {c_time} | {radio} | {user} | "
            f"like={like_num} comment={comment_num} watch={watch_num}"
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="北理贝塔驿站帖子浏览")
    parser.add_argument("--tab", choices=list(TAB_TO_RADIO.keys()), default="all")
    parser.add_argument("--sort", type=int, default=0, help="0新发 1新回 2最热 3精选")
    parser.add_argument("--pages", type=int, default=1, help="连续请求页数")
    parser.add_argument("--start-cursor", type=int, default=9999999)
    parser.add_argument("--detail-id", type=int, default=0, help="查看指定帖子详情")
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--insecure", action="store_true", help="禁用 TLS 校验")
    parser.add_argument("--raw", action="store_true", help="输出原始 JSON")
    return parser


def main() -> None:
    args = build_parser().parse_args()

    verify_tls = not args.insecure
    if args.insecure:
        requests.packages.urllib3.disable_warnings()  # type: ignore[attr-defined]

    if args.detail_id > 0:
        detail = fetch_detail(args.detail_id, args.timeout, verify_tls)
        print(json.dumps(detail, ensure_ascii=False, indent=2))
        return

    cursor = args.start_cursor
    total = 0
    for page in range(1, args.pages + 1):
        body = fetch_list(args.tab, args.sort, cursor, args.timeout, verify_tls)
        task_list = body.get("taskList", [])
        if not isinstance(task_list, list):
            raise RuntimeError(f"taskList 类型异常: {type(task_list)}")

        if args.raw:
            print(json.dumps(body, ensure_ascii=False, indent=2))
        else:
            print_list_page(task_list, page)

        if not task_list:
            break

        total += len(task_list)
        last_id = task_list[-1].get("id")
        if not isinstance(last_id, int):
            break
        cursor = last_id

    print(f"\n总计获取帖子数: {total}")


if __name__ == "__main__":
    main()
