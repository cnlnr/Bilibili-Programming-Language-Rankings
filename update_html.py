#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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


def build_html(results: list) -> str:
    raw_data_json = json.dumps(results, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bilibili 编程语言教程热度对比</title>
    <style>
        :root {{
            --bg: #0b0f19;
            --card-bg: #151d30;
            --card-sub: #1e2942;
            --text: #f1f5f9;
            --text-dim: #94a3b8;
            --border: #2d3a54;
            --accent: #38bdf8;
            --bar-grad: linear-gradient(90deg, #38bdf8, #818cf8);
        }}
        * {{ box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", sans-serif;
            background: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 32px 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ font-size: 24px; margin-bottom: 6px; font-weight: 700; }}
        .desc {{ color: var(--text-dim); font-size: 14px; margin-bottom: 24px; }}

        /* 表格区域 */
        .section-box {{
            background: var(--card-bg);
            border-radius: 12px;
            border: 1px solid var(--border);
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        }}
        .table-wrap {{ overflow-x: auto; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
            text-align: left;
        }}
        th, td {{
            padding: 12px 14px;
            border-bottom: 1px solid var(--border);
        }}
        th {{
            background: var(--card-sub);
            color: var(--text-dim);
            font-weight: 600;
            cursor: pointer;
            user-select: none;
            transition: 0.2s;
            white-space: nowrap;
        }}
        th:hover {{ color: var(--accent); }}
        th.sort-active {{ color: var(--accent); }}
        th.sort-desc::after {{ content: " ▼"; font-size: 10px; }}
        th.sort-asc::after {{ content: " ▲"; font-size: 10px; }}
        tr:hover td {{ background: rgba(255, 255, 255, 0.03); }}
        .rank-col {{ width: 50px; text-align: center; color: var(--text-dim); }}
        .tag-col {{ color: var(--accent); font-weight: 600; white-space: nowrap; }}
        a {{ color: var(--text); text-decoration: none; }}
        a:hover {{ color: var(--accent); text-decoration: underline; }}

        /* 下方图表区域 */
        .chart-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            flex-wrap: wrap;
            gap: 12px;
        }}
        .chart-title {{ font-size: 18px; font-weight: 600; }}
        .metric-badge {{
            background: var(--card-sub);
            border: 1px solid var(--accent);
            color: var(--accent);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
        }}
        .chart-list {{
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}
        .chart-row {{
            display: grid;
            grid-template-columns: 100px 1fr 100px;
            align-items: center;
            gap: 16px;
            font-size: 13px;
        }}
        .chart-label {{
            font-weight: 600;
            text-align: right;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .chart-bar-bg {{
            background: rgba(255, 255, 255, 0.05);
            height: 22px;
            border-radius: 6px;
            overflow: hidden;
            position: relative;
        }}
        .chart-bar-fill {{
            height: 100%;
            background: var(--bar-grad);
            border-radius: 6px;
            width: 0%;
            transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .chart-val {{
            font-weight: 700;
            color: var(--text);
            font-family: monospace;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Bilibili 编程语言教程排行榜</h1>
        <div class="desc">💡 点击表头切换排序指标，下方热度对比图将自动同步更新并绘制进度条</div>

        <!-- 1. 表格区域 -->
        <div class="section-box">
            <div class="table-wrap">
                <table id="rankTable">
                    <thead>
                        <tr>
                            <th class="rank-col">排名</th>
                            <th>语言/标签</th>
                            <th class="sort-active sort-desc" data-key="favorite">收藏数</th>
                            <th data-key="view">播放量</th>
                            <th data-key="like">点赞数</th>
                            <th data-key="coin">硬币数</th>
                            <th data-key="reply">评论数</th>
                            <th data-key="danmaku">弹幕数</th>
                            <th>视频标题</th>
                        </tr>
                    </thead>
                    <tbody id="tableBody"></tbody>
                </table>
            </div>
        </div>

        <!-- 2. 独立热度对比图区域 -->
        <div class="section-box">
            <div class="chart-header">
                <div class="chart-title">🔥 热度分布对比图</div>
                <div class="metric-badge" id="currentMetricBadge">当前对比指标：收藏数</div>
            </div>
            <div class="chart-list" id="chartList"></div>
        </div>
    </div>

    <script>
        const rawData = {raw_data_json};
        let currentKey = "favorite";
        let isAsc = false;

        const metricNames = {{
            favorite: "收藏数",
            view: "播放量",
            like: "点赞数",
            coin: "硬币数",
            reply: "评论数",
            danmaku: "弹幕数"
        }};

        function fmt(n) {{
            if (n >= 1e8) return (n / 1e8).toFixed(1) + '亿';
            if (n >= 1e4) return (n / 1e4).toFixed(1) + '万';
            return n.toLocaleString();
        }}

        function render() {{
            // 1. 排序数据
            rawData.sort((a, b) => isAsc ? (a[currentKey] - b[currentKey]) : (b[currentKey] - a[currentKey]));

            // 2. 渲染表格
            const tbody = document.getElementById("tableBody");
            tbody.innerHTML = rawData.map((r, idx) => `
                <tr>
                    <td class="rank-col">${{idx + 1}}</td>
                    <td class="tag-col">${{r.tag}}</td>
                    <td>${{fmt(r.favorite)}}</td>
                    <td>${{fmt(r.view)}}</td>
                    <td>${{fmt(r.like)}}</td>
                    <td>${{fmt(r.coin)}}</td>
                    <td>${{fmt(r.reply)}}</td>
                    <td>${{fmt(r.danmaku)}}</td>
                    <td><a href="${{r.url}}" target="_blank" title="${{r.title}}">${{r.title.slice(0, 12) + (r.title.length > 12 ? '...' : '')}}</a></td>
                </tr>
            `).join("");

            // 3. 渲染下方独立图表
            const maxVal = Math.max(...rawData.map(r => r[currentKey]), 1);
            document.getElementById("currentMetricBadge").innerText = `当前对比指标：${{metricNames[currentKey]}} (${{isAsc ? '升序' : '降序'}})`;

            const chartList = document.getElementById("chartList");
            chartList.innerHTML = rawData.map(r => {{
                const pct = ((r[currentKey] / maxVal) * 100).toFixed(1);
                return `
                    <div class="chart-row">
                        <div class="chart-label" title="${{r.tag}}">${{r.tag}}</div>
                        <div class="chart-bar-bg">
                            <div class="chart-bar-fill" style="width: ${{pct}}%"></div>
                        </div>
                        <div class="chart-val">${{fmt(r[currentKey])}}</div>
                    </div>
                `;
            }}).join("");
        }}

        // 表头点击事件绑定
        document.querySelectorAll("th[data-key]").forEach(th => {{
            th.addEventListener("click", () => {{
                const key = th.getAttribute("data-key");
                if (currentKey === key) {{
                    isAsc = !isAsc;
                }} else {{
                    currentKey = key;
                    isAsc = false;
                }}

                document.querySelectorAll("th").forEach(h => h.classList.remove("sort-active", "sort-desc", "sort-asc"));
                th.classList.add("sort-active", isAsc ? "sort-asc" : "sort-desc");

                render();
            }});
        }});

        // 初始化首次渲染
        render();
    </script>
</body>
</html>"""


def main():
    results = []
    total = len(urls)
    print(f"开始批量获取数据（共 {total} 个目标）...\n")

    for idx, (tag, raw_url) in enumerate(urls.items(), start=1):
        bvid = ba.parse_bvid(raw_url)
        if not bvid: continue
        try:
            data = ba.fetch(bvid)
            stat = data.get("stat", {})
            results.append({
                "tag": tag,
                "title": data.get("title", "未知标题"),
                "favorite": stat.get("favorite", 0),
                "view": stat.get("view", 0),
                "like": stat.get("like", 0),
                "coin": stat.get("coin", 0),
                "reply": stat.get("reply", 0),
                "danmaku": stat.get("danmaku", 0),
                "url": f"https://www.bilibili.com/video/{bvid}",
            })
            print(f"[{idx}/{total}]  {tag:<8} | 收藏: {ba.fmt(stat.get('favorite', 0)):>6}")
        except Exception as e:
            print(f"[{idx}/{total}] ❌ 抓取失败: {tag} - {e}")
        time.sleep(0.2)

    # 生成单文件交互式 HTML
    html_filename = "index.html"
    with open(html_filename, "w", encoding="utf-8") as f:
        f.write(build_html(results))

    print(f"\n 全部完成！已生成可交互网页: ./{html_filename}")


if __name__ == "__main__":
    main()
