#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import json
import os
import re
import time
import urllib.error
import urllib.request

urls = {
    "CMD": "https://www.bilibili.com/video/BV1RG41137kJ/",
    "PowerShell": "https://www.bilibili.com/video/BV1Bx411g7gD/",
    "MySQL": "https://www.bilibili.com/video/BV1Kr4y1i7ru/",
    "Lua": "https://www.bilibili.com/video/BV1vf4y1L7Rb/",
    "PHP": "https://www.bilibili.com/video/BV18x411H7qD/",
    "Swift": "https://www.bilibili.com/video/BV1mT4y1C7JZ/",
    "Kotlin": "https://www.bilibili.com/video/BV1kT4y1o7nP/",
    "TypeScript": "https://www.bilibili.com/video/BV1Za4y1r7KE/",
    "Linux": "https://www.bilibili.com/video/BV1n84y1i7td/",
    "Golang": "https://www.bilibili.com/video/BV1ME411Y71o/",
    "Vuejs": "https://www.bilibili.com/video/BV1Zy4y1K7SH/",
    "Python": "https://www.bilibili.com/video/BV1wD4y1o7AS/",
    "Unity(C#)": "https://www.bilibili.com/video/BV1gQ4y1e7SS/",
    "Java": "https://www.bilibili.com/video/BV17F411T7Ao/",
    "C++": "https://www.bilibili.com/video/BV1et411b73Z/",
    "Rust": "https://www.bilibili.com/video/BV1hp4y1k7SV/",
    "C": "https://www.bilibili.com/video/BV1q54y1q79w/",
    "JavaScript": "https://www.bilibili.com/video/BV1Y84y1L7Nn/",
    "Ruby": "https://www.bilibili.com/video/BV1QW411F7rh/",
    "Bash": "https://www.bilibili.com/video/BV1ah411R7W6/",
    "汇编": "https://www.bilibili.com/video/BV1Wu411B72F/",
    "Nim": "https://www.bilibili.com/video/BV1zp4y137zi/",
    "R": "https://www.bilibili.com/video/BV1fh411H7vi/",
    "Perl": "https://www.bilibili.com/video/BV1px411e7gc/",
}


def parse_bvid(url_str: str) -> str:
    """从链接中正则提取 BV 号"""
    match = re.search(r"(BV[a-zA-Z0-9]{10})", str(url_str))
    return match.group(1) if match else ""


def fmt_number(n: int) -> str:
    """数值格式化（万/亿）"""
    if not isinstance(n, (int, float)):
        return "0"
    if n >= 100_000_000:
        return f"{n / 100_000_000:.1f}亿"
    if n >= 10_000:
        return f"{n / 10_000:.1f}万"
    return f"{n:,}"


def fetch_bilibili_data(bvid: str) -> dict:
    """调用 B 站公开 Web API 获取视频详情"""
    api_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.bilibili.com/",
    }
    req = urllib.request.Request(api_url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        if res.get("code") == 0:
            return res.get("data", {})
        raise ValueError(f"B站接口返回异常: code={res.get('code')}, msg={res.get('message')}")


def main():
    rows = []
    total = len(urls)
    print(f"开始批量获取数据（共 {total} 个目标）...\n")

    for idx, (tag, raw_url) in enumerate(urls.items(), start=1):
        bvid = parse_bvid(raw_url)
        if not bvid:
            print(f"[{idx}/{total}] ❌ 解析 BV 号失败: {tag} -> {raw_url}")
            continue

        try:
            data = fetch_bilibili_data(bvid)
            stat = data.get("stat", {})
            title = data.get("title", "未知标题")
            fav = stat.get("favorite", 0)
            view = stat.get("view", 0)
            like = stat.get("like", 0)
            coin = stat.get("coin", 0)
            reply = stat.get("reply", 0)
            danmaku = stat.get("danmaku", 0)

            # 二维紧凑存储: [tag, bvid, title, fav, view, like, coin, reply, danmaku]
            rows.append([tag, bvid, title, fav, view, like, coin, reply, danmaku])
            print(f"[{idx}/{total}] {tag:<10} | 收藏: {fmt_number(fav):>6} | 播放: {fmt_number(view):>6}")
        except Exception as e:
            print(f"[{idx}/{total}] ❌ 抓取失败: {tag} ({bvid}) - {e}")

        time.sleep(0.3)

    new_snapshot = {
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "rows": rows,
    }

    # 1. 兼容读取已有历史数据（自动平滑迁移旧单快照格式）
    history = []
    if os.path.exists("data.json"):
        try:
            with open("data.json", "r", encoding="utf-8") as f:
                old_data = json.load(f)
                if isinstance(old_data, list):
                    history = old_data
                elif isinstance(old_data, dict) and "rows" in old_data:
                    history = [old_data]
        except Exception as e:
            print(f"读取旧数据异常（将重置为新列表）: {e}")

    # 2. 直接无脑追加最新一期快照
    history.append(new_snapshot)

    # 3. 写回 data.json
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

    print(f"\n抓取完成！已追加写入 ./data.json（当前历史快照总数: {len(history)} 期）")


if __name__ == "__main__":
    main()
