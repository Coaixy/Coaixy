"""Keep GitHub's responsive artwork and accessible project links in sync."""

from html import escape
from pathlib import Path
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SANS = "-apple-system, BlinkMacSystemFont, 'PingFang SC', 'Noto Sans CJK SC', sans-serif"
SERIF = "Georgia, 'Times New Roman', serif"
PALETTES = {
    "light": {"bg": "#faf9f5", "ink": "#252523", "body": "#48463f", "muted": "#78736a", "line": "#e6dfd8", "accent": "#8b4513", "soft": "#efe9de"},
    "dark": {"bg": "#181715", "ink": "#faf9f5", "body": "#d8d3ca", "muted": "#aaa298", "line": "#3d3832", "accent": "#d6a47a", "soft": "#27231e"},
}
PROJECTS = [
    {"slug": "liuren", "name": "liuren-ts-lib", "owner": "look-fate", "tag": "排盘算法 / TypeScript", "desc": "基于 tyme4ts 的大六壬排盘库，提供结构化结果与调用接口。", "url": "https://github.com/look-fate/liuren-ts-lib"},
    {"slug": "skills", "name": "xuanxue-skill", "owner": "Coaixy", "tag": "Agent / 术数工具", "desc": "面向 Agent 的术数 Skill 集合，整理使用框架与参考资料。", "url": "https://github.com/Coaixy/xuanxue-skill"},
    {"slug": "benchmark", "name": "fate_benchmark", "owner": "look-fate", "tag": "模型评测 / Python", "desc": "基于 BaziQA 的模型评测流程，记录回答、评分与分项统计。", "url": "https://github.com/look-fate/fate_benchmark"},
    {"slug": "books", "name": "TCM-Ancient-Books", "owner": "Coaixy", "tag": "文献整理 / 知识检索", "desc": "中医古籍 OCR 文本的专题整理与检索预处理。", "url": "https://github.com/Coaixy/TCM-Ancient-Books"},
]


def text(x, y, value, size, color, weight=400, serif=False, anchor="start", spacing=0):
    family = SERIF if serif else SANS
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="{escape(family, quote=True)}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" letter-spacing="{spacing}">{escape(value)}</text>'


def lines(value, max_units):
    result, line, used = [], "", 0
    for char in value:
        units = 1 if unicodedata.east_asian_width(char) in "WF" else 0.56
        if used + units > max_units and line:
            result.append(line)
            line, used = "", 0
        line += char
        used += units
    if line:
        result.append(line)
    return result


def rect(x, y, width, height, fill, radius=0, stroke=None):
    border = f' stroke="{stroke}"' if stroke else ""
    return f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" fill="{fill}"{border}/>'


def rule(x1, y, x2, color):
    return f'<path d="M{x1} {y}H{x2}" stroke="{color}"/>'


def arrow(x, y, color, scale=1):
    return f'<path d="M{x} {y+16*scale}l{16*scale} {-16*scale}m{-14*scale} 0h{14*scale}v{14*scale}" fill="none" stroke="{color}" stroke-width="{2*scale}" stroke-linecap="round" stroke-linejoin="round"/>'


def document(width, height, title, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title>{body}</svg>\n'


def hero(p, mobile):
    w, h, pad = (600, 454, 32) if mobile else (1200, 412, 52)
    body = rect(0, 0, w, h, p["bg"], 16)
    body += text(pad, 48, "小奕 / LOOKFATE", 18, p["accent"], spacing=2)
    body += text(pad-3, 146, "Coaixy", 94 if mobile else 98, p["ink"], serif=True, spacing=-3)
    if mobile:
        body += text(pad, 211, "以代码承载术数，", 34, p["ink"])
        body += text(pad, 258, "以开源连接同行。", 34, p["ink"])
        body += text(pad, 316, "传统术数的程序化实现", 28, p["body"])
        body += text(pad, 355, "与 AI Agent 应用", 28, p["body"])
        body += rule(pad, 391, w-pad, p["line"])
        body += text(pad, 428, "排盘算法 · 知识检索 · 模型评测", 24, p["muted"])
    else:
        body += text(pad, 213, "以代码承载术数，以开源连接同行。", 38, p["ink"])
        body += text(pad, 272, "关注传统术数的程序化实现与 AI Agent 应用。", 28, p["body"])
        body += text(pad, 315, "把规则写成代码，让模型使用工具，让结果可以被检查。", 26, p["muted"])
        body += rule(pad, 350, w-pad, p["line"])
        body += text(pad, 387, "排盘算法   /   知识检索   /   模型评测", 22, p["muted"])
        body += f'<g transform="translate(1030 145)"><circle r="91" fill="none" stroke="{p["line"]}"/><circle r="112" fill="none" stroke="{p["line"]}" stroke-dasharray="2 10"/><path d="M-42-43H42M-42-25H-8M8-25H42M-42-7H42M-42 11H-8M8 11H42M-42 29H-8M8 29H42M-42 47H42" fill="none" stroke="{p["accent"]}" stroke-width="6" stroke-linecap="round"/><circle cy="-112" r="4" fill="{p["accent"]}"/></g>'
    return w, h, body


def current(p, mobile):
    w, h, pad = (600, 320, 32) if mobile else (1200, 250, 52)
    body = rect(0, 0, w, h, "#211d19", 16)
    body += text(pad, 44, "01 / 正在构建", 20, "#d6a47a", spacing=1)
    body += text(pad-2, 115, "FateClaw", 60 if mobile else 64, "#faf9f5", serif=True, spacing=-1)
    badge_x = 357 if mobile else 370
    body += rect(badge_x, 78, 104, 36, "#3b3025", 18)
    body += text(badge_x+52, 103, "开发中", 20, "#e4bc91", anchor="middle")
    if mobile:
        body += text(pad, 176, "东方术数排盘与 AI 解读应用。", 28, "#eee6dc")
        body += text(pad, 223, "探索工具、知识与 Agent 的协作。", 28, "#c5b9ac")
        body += rule(pad, 258, w-pad, "#493d32")
        body += text(pad, 295, "排盘工具  /  知识检索  /  Agent 交互", 23, "#c5b9ac")
    else:
        body += text(pad, 172, "东方术数排盘与 AI 解读应用。", 30, "#eee6dc")
        body += text(pad, 216, "探索把排盘工具、知识检索与 Agent 交互连接起来。", 26, "#c5b9ac")
        for x, label in [(830, "排盘工具"), (1000, "Agent 交互")]:
            body += rect(x, 66, 148, 116, "#2c251f", 12, "#493d32")
            body += text(x+74, 134, label, 23, "#e4bc91", anchor="middle")
    return w, h, body


def project_heading(p, mobile):
    w, h, pad = (600, 100, 32) if mobile else (1200, 96, 52)
    body = text(pad, 34, "02 / OPEN WORK", 18, p["accent"], spacing=1)
    body += text(pad, 80, "公开作品", 34, p["ink"])
    body += text(w-pad, 78, "查看项目 ↗", 22, p["muted"], anchor="end")
    return w, h, body


def project(p, mobile, item, number):
    w, pad = (600, 32) if mobile else (1200, 52)
    wrapped = lines(item["desc"], 17 if mobile else 41)
    h = 158 + len(wrapped)*39 if mobile else 190
    body = rect(0, 0, w, h, p["bg"], 14, p["line"])
    if mobile:
        body += text(pad, 39, f"{number:02}", 20, p["accent"])
        body += text(w-pad, 39, item["tag"], 22, p["muted"], anchor="end")
        body += text(pad, 91, item["name"], 34, p["ink"], weight=500)
        for index, line in enumerate(wrapped):
            body += text(pad, 139+index*39, line, 29, p["body"])
        body += text(pad, h-24, item["owner"], 20, p["muted"])
        body += arrow(w-pad-22, h-44, p["accent"], 1.25)
    else:
        body += text(pad, 48, f"{number:02}", 19, p["accent"])
        body += text(pad+64, 58, item["name"], 36, p["ink"], weight=500)
        body += text(w-pad, 52, item["tag"], 22, p["accent"], anchor="end")
        for index, line in enumerate(wrapped):
            body += text(pad+64, 109+index*36, line, 28, p["body"])
        body += text(pad+64, 163, item["owner"], 20, p["muted"])
        body += arrow(w-pad-24, 135, p["accent"], 1.4)
    return w, h, body


def collaboration(p, mobile):
    w, h, pad = (600, 598, 32) if mobile else (1200, 398, 52)
    body = rect(0, 0, w, h, "#8b4513", 16)
    body += text(pad, 46, "03 / 一起做点什么", 20, "#ebcda9", spacing=1)
    body += text(pad, 112, "从一个具体问题开始。", 38 if mobile else 48, "#fff9f1")
    items = [("规则核对", "规则出处、盘例与流派差异"), ("开发接入", "算法、示例与 Agent 工具接入"), ("测试评测", "问题复现、测试案例与评测方法")]
    for index, (title, detail) in enumerate(items):
        x = pad if mobile else pad+index*370
        y = 181+index*96 if mobile else 183
        body += text(x, y, title, 30 if mobile else 28, "#fff9f1", weight=500)
        body += text(x, y+40, detail, 26 if mobile else 22, "#ebcda9")
    line_y = 459 if mobile else 260
    body += rule(pad, line_y, w-pad, "#ac7143")
    body += text(pad, line_y+44, "来信聊聊目标、已有进展与合作想法。", 26, "#fff9f1")
    body += text(pad, h-36, "coaixy@outlook.com", 28, "#fff9f1")
    body += arrow(w-pad-24, h-61, "#fff9f1", 1.4)
    return w, h, body


def footer(p, mobile):
    w, h, pad = (600, 90, 32) if mobile else (1200, 82, 52)
    body = rule(pad, 1, w-pad, p["line"])
    body += text(pad, 52, "LOOKFATE / COAIXY", 20, p["muted"], spacing=1)
    body += text(w-pad, 52, "个人网站 ↗", 23, p["accent"], anchor="end")
    return w, h, body


PANELS = [
    ("hero", "小奕 Coaixy，主理 LookFate。关注传统术数的程序化实现与 AI Agent 应用，排盘算法、知识检索与模型评测。点击查看 LookFate。", "https://github.com/look-fate", hero),
    ("current", "正在开发 FateClaw：东方术数排盘与 AI 解读应用，探索把排盘工具、知识检索与 Agent 交互连接起来。", None, current),
    ("projects", "公开作品：以下项目卡片均可点击查看仓库。", None, project_heading),
]
for index, item in enumerate(PROJECTS, start=1):
    PANELS.append(("project-"+item["slug"], item["name"]+"："+item["desc"]+" 点击查看项目。", item["url"], lambda p, m, item=item, index=index: project(p, m, item, index)))
PANELS += [
    ("collaboration", "欢迎一起核对术数规则、开发软件与 Agent、完善测试评测。具体问题请在对应仓库提交 Issue；跨项目合作请邮件说明目标、已有进展与合作想法。联系 coaixy@outlook.com。", "mailto:coaixy@outlook.com", collaboration),
    ("footer", "LookFate / Coaixy。点击访问个人网站。", "https://www.letfate.com", footer),
]


def picture(name, alt, url):
    parts = ["<p>"]
    if url:
        parts.append(f'  <a href="{escape(url, quote=True)}">')
    parts += [
        "    <picture>",
        f'      <source media="(max-width: 767px) and (prefers-color-scheme: dark)" srcset="assets/{name}-dark-mobile.svg">',
        f'      <source media="(max-width: 767px)" srcset="assets/{name}-light-mobile.svg">',
        f'      <source media="(prefers-color-scheme: dark)" srcset="assets/{name}-dark.svg">',
        f'      <img src="assets/{name}-light.svg" alt="{escape(alt, quote=True)}" width="100%">',
        "    </picture>",
    ]
    if url:
        parts.append("  </a>")
    parts.append("</p>")
    return "\n".join(parts)


def main():
    ASSETS.mkdir(exist_ok=True)
    for name, alt, _, renderer in PANELS:
        for theme, palette in PALETTES.items():
            for mobile in [False, True]:
                w, h, body = renderer(palette, mobile)
                suffix = "-mobile" if mobile else ""
                (ASSETS/f"{name}-{theme}{suffix}.svg").write_text(document(w, h, alt, body), encoding="utf-8")
    (ROOT/"README.md").write_text("\n\n".join(picture(name, alt, url) for name, alt, url, _ in PANELS)+"\n", encoding="utf-8")


if __name__ == "__main__":
    main()
