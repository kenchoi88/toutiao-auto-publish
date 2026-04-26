"""
从头条号后台导出的 xls（标题+阅读量+链接）逐篇抓 m.toutiao.com SSR 页的
标题 / 摘要（description）/ 封面大图，合并成 JSON + Markdown 素材。

用法：
    python 抓取素材.py <xls路径> <作者名>

输出：
    素材/<作者名>/文章.json         结构化数据（xls数据 + 抓取摘要）
    素材/<作者名>/文章清单.md       人类可读，按阅读量排序
    素材/<作者名>/按时间.md         按发布时间排序
"""
import os, re, sys, json, time, io
import xlrd
import requests

UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1"
HEADERS = {"User-Agent": UA, "Referer": "https://m.toutiao.com/"}
REQ_TIMEOUT = 15
SLEEP = 0.8

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def parse_xls(path):
    wb = xlrd.open_workbook(path)
    sh = wb.sheet_by_index(0)
    header = [str(x) for x in sh.row_values(0)]
    articles = []
    for r in range(1, sh.nrows):
        row = sh.row_values(r)
        url = str(row[6]).strip()
        m = re.search(r"/item/(\d+)", url)
        if not m:
            continue
        articles.append({
            "gid": m.group(1),
            "title": str(row[0]).strip(),
            "read": int(row[1]) if row[1] else 0,
            "comment": int(row[2]) if row[2] else 0,
            "domain": str(row[3]).strip(),
            "author": str(row[4]).strip(),
            "publish_time": str(row[5]).strip(),
            "url": url,
            "cover": str(row[7]).strip() if len(row) > 7 else "",
        })
    return articles


def fetch_summary(gid):
    url = f"https://m.toutiao.com/a{gid}/"
    r = requests.get(url, headers=HEADERS, timeout=REQ_TIMEOUT)
    if r.status_code != 200:
        return {"status": r.status_code}
    html = r.text
    def grab(pattern):
        m = re.search(pattern, html)
        return m.group(1).strip() if m else ""
    return {
        "status": 200,
        "title_full": grab(r'<title>([^<]{3,200})</title>'),
        "desc_meta": grab(r'<meta\s+name="description"\s+content="([^"]{0,800})"'),
        "desc_og": grab(r'<meta\s+property="og:description"\s+content="([^"]{0,800})"'),
        "og_image": grab(r'<meta\s+property="og:image"\s+content="([^"]+)"'),
        "size": len(html),
    }


def main():
    if len(sys.argv) < 3:
        print("用法: python 抓取素材.py <xls路径> <作者名>", file=sys.stderr)
        sys.exit(1)
    xls_path = os.path.expanduser(sys.argv[1])
    author_slug = sys.argv[2]

    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(here, "素材", author_slug)
    os.makedirs(out_dir, exist_ok=True)

    articles = parse_xls(xls_path)
    print(f"xls 解析到 {len(articles)} 篇。开始抓摘要……")

    ok, fail = 0, 0
    for i, a in enumerate(articles, 1):
        try:
            s = fetch_summary(a["gid"])
            a["fetched"] = s
            if s.get("status") == 200 and (s.get("desc_og") or s.get("desc_meta")):
                ok += 1
                tag = "✓"
            else:
                fail += 1
                tag = "✗"
            print(f"  [{i:02d}/{len(articles)}] {tag} {a['title'][:30]}")
        except Exception as e:
            fail += 1
            a["fetched"] = {"status": -1, "error": str(e)}
            print(f"  [{i:02d}/{len(articles)}] ✗ ERR {e}")
        time.sleep(SLEEP)

    # 保存 JSON
    json_path = os.path.join(out_dir, "文章.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    # 可读 Markdown：按阅读量倒序
    by_read = sorted(articles, key=lambda x: -x["read"])
    lines = [f"# {author_slug} · 文章清单（按阅读量）", f"共 {len(articles)} 篇  抓取成功 {ok}  失败 {fail}", ""]
    for a in by_read:
        desc = a.get("fetched", {}).get("desc_og") or a.get("fetched", {}).get("desc_meta") or ""
        lines.append(f"## [{a['read']:,}] {a['title']}")
        lines.append(f"- 发布: {a['publish_time']}  · 评论: {a['comment']}  · 链接: {a['url']}")
        if desc:
            lines.append(f"- 摘要: {desc}")
        lines.append("")
    md_read = os.path.join(out_dir, "文章清单.md")
    with open(md_read, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    # 按时间倒序
    by_time = sorted(articles, key=lambda x: x["publish_time"], reverse=True)
    lines = [f"# {author_slug} · 文章清单（按时间）", ""]
    for a in by_time:
        desc = a.get("fetched", {}).get("desc_og") or a.get("fetched", {}).get("desc_meta") or ""
        lines.append(f"## {a['publish_time']} · [{a['read']:,}] {a['title']}")
        if desc:
            lines.append(f"> {desc}")
        lines.append(f"- {a['url']}")
        lines.append("")
    md_time = os.path.join(out_dir, "按时间.md")
    with open(md_time, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print()
    print(f"✓ 完成。成功 {ok} / 失败 {fail}")
    print(f"  JSON: {json_path}")
    print(f"  MD:   {md_read}")
    print(f"  MD:   {md_time}")


if __name__ == "__main__":
    main()
