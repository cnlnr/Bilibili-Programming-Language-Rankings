#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import json
import time
import bilibili_analyzer as ba

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
    "易语言": "https://www.bilibili.com/video/BV14W411R75Y/",
    "R": "https://www.bilibili.com/video/BV1fh411H7vi/",
    "iApp": "https://www.bilibili.com/video/BV18T4y177YQ/",
    "结绳": "https://www.bilibili.com/video/BV13K411Q7nV/",
    "Perl": "https://www.bilibili.com/video/BV1px411e7gc/",
}


def main():
    rows = []
    total = len(urls)
    print(f"开始批量获取数据（共 {total} 个目标）...\n")

    for idx, (tag, raw_url) in enumerate(urls.items(), start=1):
        bvid = ba.parse_bvid(raw_url)
        if not bvid:
            continue
        try:
            data = ba.fetch(bvid)
            stat = data.get("stat", {})
            title = data.get("title", "未知标题")
            fav = stat.get("favorite", 0)
            view = stat.get("view", 0)
            like = stat.get("like", 0)
            coin = stat.get("coin", 0)
            reply = stat.get("reply", 0)
            danmaku = stat.get("danmaku", 0)

            # 二维紧凑存储结构: [tag, bvid, title, fav, view, like, coin, reply, danmaku]
            rows.append([tag, bvid, title, fav, view, like, coin, reply, danmaku])
            print(f"[{idx}/{total}] {tag:<8} | 收藏: {ba.fmt(fav):>6} | 播放: {ba.fmt(view):>6}")
        except Exception as e:
            print(f"[{idx}/{total}] ❌ 抓取失败: {tag} - {e}")
        time.sleep(0.2)

    payload = {
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "rows": rows,
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print("\n抓取完成！紧凑数据已写入 ./data.json")


if __name__ == "__main__":
    main()
