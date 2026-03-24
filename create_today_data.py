import json
import re

html_path = "/Users/seanzyzhao/WorkBuddy/daily-reports/iran-commodity/report-2026-03-23-1054.html"
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

def extract_array(pattern):
    m = re.search(pattern, content)
    return json.loads(m.group(1))

labels = extract_array(r"labels:\s*(\[[^\]]+\])")
brent_data = extract_array(r"label:\s*'Brent 原油[^']*',\s*data:\s*(\[[^\]]+\])")
wti_data = extract_array(r"label:\s*'WTI 原油[^']*',\s*data:\s*(\[[^\]]+\])")
ng_data = extract_array(r"label:\s*'Natural Gas[^']*',\s*data:\s*(\[[^\]]+\])")
gold_data = extract_array(r"label:\s*'Gold[^']*',\s*data:\s*(\[[^\]]+\])")
silver_data = extract_array(r"label:\s*'Silver[^']*',\s*data:\s*(\[[^\]]+\])")

labels = labels[1:] + ["2026-03-24"]
brent_data = brent_data[1:] + [98.96]
wti_data = wti_data[1:] + [91.19]
ng_data = ng_data[1:] + [2.926]
gold_data = gold_data[1:] + [4429.65]
silver_data = silver_data[1:] + [69.16]

yf_data = {
    "Brent": {"latest": "98.96", "dates": labels, "closes": brent_data},
    "WTI": {"latest": "91.19", "dates": labels, "closes": wti_data},
    "Natural Gas": {"latest": "2.926", "dates": labels, "closes": ng_data},
    "Gold": {"latest": "4429.65", "dates": labels, "closes": gold_data},
    "Silver": {"latest": "69.16", "dates": labels, "closes": silver_data},
    "S&P 500": {"latest": "6581.00"},
    "USD/IRR": {"latest": "1,313,798"},
    "USD/CNY": {"latest": "6.8900"}
}

with open("yf_data.json", "w", encoding="utf-8") as f:
    json.dump(yf_data, f, ensure_ascii=False, indent=4)

news_zh = {
    "focus": [
        {
            "title": "特朗普声称伊朗“想达成协议”以结束冲突",
            "link": "https://apnews.com/live/iran-war-israel-trump-03-23-2026",
            "summary": "美国总统特朗普向记者表示，伊朗方面“希望达成一项协议”，并声称美国特使已与一位“受人尊敬的”伊朗领导人举行了会谈。然而，伊朗方面随后否认了这些说法。这表明双方在外交层面存在信息博弈，但潜在的谈判渠道可能正在试探中。",
            "date": "2026-03-24"
        },
        {
            "title": "特朗普对伊朗发出最后通牒：威胁袭击能源设施",
            "link": "https://abcnews.com/International/live-updates/iran-live-updates-trumps-48-hour-deadline-expire/?id=131316431",
            "summary": "美国总统特朗普在社交媒体上暗示与伊朗的谈判“非常好”，可能达成“全面解决方案”。但同时他发出严厉警告，如果无法达成一致，将瞄准并打击伊朗的能源设施。这种极限施压战术导致国际原油市场在过去24小时内出现剧烈波动。",
            "date": "2026-03-24"
        },
        {
            "title": "伊朗总统强硬回击：战场上见",
            "link": "https://parstoday.ir/zh",
            "summary": "面对美国的军事威胁，伊朗总统及伊斯兰革命最高领袖在新年致辞中发出强烈警告。他们明确表示，对于任何肆无忌惮的挑衅和威胁，伊朗军队将在战场上予以最坚决的回应，绝不妥协。",
            "date": "2026-03-24"
        },
        {
            "title": "中东战争“冲突螺旋”加剧 波及更广泛区域",
            "link": "https://news.un.org/zh/story/2026/03/1141795",
            "summary": "联合国人权理事会最新报告指出，目前的战斗已演化为一场波及全区域的“冲突螺旋”。除了美以对伊朗的打击，还包括伊朗对海湾国家的报复性无人机与导弹袭击，导致中东地区平民伤亡惨重。",
            "date": "2026-03-24"
        }
    ],
    "regional": [
        {
            "title": "美军F-35战机在中东执行任务",
            "link": "https://parstoday.ir/zh",
            "summary": "美军F-35战机在伊朗周边空域巡航，加剧地区紧张态势。"
        },
        {
            "title": "伊朗警告将封锁霍尔木兹海峡",
            "link": "https://nournews.ir/Zh/",
            "summary": "伊朗伊斯兰革命卫队表示，若美国袭击其发电站，伊朗将完全关闭霍尔木兹海峡并打击以色列发电设施。"
        },
        {
            "title": "伊朗对海湾国家发动无人机袭击",
            "link": "https://news.un.org/zh/story/2026/03/1141795",
            "summary": "作为对以色列袭击的报复，伊朗动用无人机对周边支持以色列的海湾设施进行了战术打击。"
        }
    ],
    "global": [
        {
            "title": "美司法部：特朗普对伊动武获宪法授权",
            "link": "https://www.jiemian.com/special/Israeliran/index.html",
            "summary": "美国司法部最新声明称特朗普对伊朗的初步军事行动属于总统职权，但长期冲突需国会批准。"
        },
        {
            "title": "伊朗与阿塞拜疆加速贸易协定谈判",
            "link": "https://irannewsdaily.com/",
            "summary": "在紧张局势下，伊朗试图巩固周边经济联系，与阿塞拜疆高层会晤加速特惠贸易协定的签署。"
        }
    ]
}

with open("news_zh.json", "w", encoding="utf-8") as f:
    json.dump(news_zh, f, ensure_ascii=False, indent=4)
