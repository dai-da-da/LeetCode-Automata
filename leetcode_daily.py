import requests
import datetime
import asyncio
import sys
import os
from playwright.async_api import async_playwright

async def run_task():
    print("🚀 开始抓取 LeetCode 每日一题...")
    
    # 1. 抓取数据
    gql_url = "https://leetcode.cn/graphql"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", 
        "Content-Type": "application/json", 
        "Accept-Language": "zh-CN"
    }
    
    try:
        slug_query = {"query": "query { todayRecord { question { questionTitleSlug } } }"}
        slug_res = requests.post(gql_url, json=slug_query, headers=headers).json()
        slug = slug_res['data']['todayRecord'][0]['question']['questionTitleSlug']
        
        detail_query = {
            "query": "query q($s:String!){question(titleSlug:$s){questionFrontendId translatedTitle translatedContent difficulty}}", 
            "variables": {"s": slug}
        }
        res = requests.post(gql_url, json=detail_query, headers=headers).json()['data']['question']
    except Exception as e: 
        print(f"❌ 数据抓取错误: {e}")
        sys.exit(1)

    # 2. 文件夹与路径逻辑 (北京时间 UTC+8)
    tz_bj = datetime.timezone(datetime.timedelta(hours=8))
    today = datetime.datetime.now(tz_bj).strftime("%Y-%m-%d")
    year = today[:4]
    month = today[5:7]
    
    folder_path = os.path.join(year, month, today)
    os.makedirs(folder_path, exist_ok=True)

    pdf_name, img_name, md_name = f"{today}.pdf", f"{today}.png", f"{today}.md"
    pdf_path = os.path.join(folder_path, pdf_name)
    img_path = os.path.join(folder_path, img_name)
    md_path = os.path.join(folder_path, md_name)
    
    # 3. 使用 Playwright 生成文档
    print(f"📄 正在生成文档至目录: {folder_path}/ ...")
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        style = """<style>
            body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans CJK SC",sans-serif;padding:30px;line-height:1.6;color:#1a1a1a;background:white;}
            h1{font-size:22px;margin-bottom:8px;font-weight:600;color:#000;border-bottom:1px solid #ddd;padding-bottom:8px;}
            .meta{font-size:13px;color:#666;margin-bottom:20px;}
            pre{background:#f8f8f8;padding:12px;border-radius:4px;border:1px solid #eee;overflow-x:auto;font-size:13px;}
            code{font-family:Menlo,Monaco,Consolas,monospace;font-size:13px;background:#f3f3f3;padding:2px 4px;border-radius:3px;}
            img{max-width:100%;height:auto;margin:10px 0;}
            table{border-collapse:collapse;width:100%;margin:15px 0;font-size:14px;}
            th,td{border:1px solid #eee;padding:10px;text-align:left;}
            th{background:#fafafa;font-weight:600;}
        </style>"""
        
        html_content = f"<html><head><meta charset='UTF-8'>{style}</head><body><h1>{res['questionFrontendId']}. {res['translatedTitle']}</h1><div class='meta'>难度: <b>{res['difficulty']}</b></div><div>{res['translatedContent']}</div></body></html>"
        
        await page.set_content(html_content)
        await asyncio.sleep(2)
        await page.pdf(path=pdf_path, format="A4", margin={"top":"1.2cm","bottom":"1.2cm","left":"1.2cm","right":"1.2cm"})
        await page.screenshot(path=img_path, full_page=True)
        await browser.close()

    # 4. 生成 Markdown 笔记模板
    md_tpl = f"""# [{res['questionFrontendId']}. {res['translatedTitle']}](https://leetcode.cn/problems/{slug}/)

**{today}**

**题面难度：{res['difficulty']}** [查看PDF题面](./{img_name})

---

## 


---

## 代码实现 (C++)
```cpp

```

- 时间复杂度: $O()$
- 空间复杂度: $O()$

---
"""
    if not os.path.exists(md_path):
        with open(md_path, "w", encoding="utf-8") as f: 
            f.write(md_tpl)

    # 5. 更新 README.md (阅后即焚，转为纯净目录模式)
    print("📝 正在更新 README.md...")
    readme_path = "README.md"
    
    records = {}
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # 仅抓取之前的题目表格行，彻底无视原本的项目介绍文字
                if line.startswith("|") and "日期" not in line and ":---" not in line:
                    parts = line.split("|")
                    if len(parts) > 2:
                        date_key = parts[1].strip()
                        records[date_key] = line.replace("\\", "/")

    url_folder_path = f"{year}/{month}/{today}"
    new_entry = f"| {today} | [{res['questionFrontendId']}. {res['translatedTitle']}](./{url_folder_path}/{md_name}) | {res['difficulty']} | [PDF](./{url_folder_path}/{pdf_name}) |"
    records[today] = new_entry

    sorted_dates = sorted(records.keys(), reverse=True)

    # 直接覆盖整个文件，生成纯净版题库目录
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("# 📚 LeetCode 每日一题自动归档\n\n")
        
        current_year = ""
        current_month = ""
        
        for d in sorted_dates:
            y, m, _ = d.split("-")
            
            if y != current_year:
                current_year = y
                f.write(f"## {current_year}年\n\n")
                current_month = "" 
                
            if m != current_month:
                current_month = m
                f.write(f"### {current_month}月\n\n")
                f.write("| 日期 | 题目 | 难度 | 附件 |\n")
                f.write("| :--- | :--- | :--- | :--- |\n")
                
            f.write(records[d] + "\n")
            
    print("🎉 任务完成！ README.md 已切换为纯净目录。")

if __name__ == "__main__":
    asyncio.run(run_task())