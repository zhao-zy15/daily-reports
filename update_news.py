import re

file_path = "/Users/seanzyzhao/WorkBuddy/daily-reports/iran-commodity/report-2026-03-20-1930.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

new_news_section = """        <h2>🌍 最新地缘政治动态 (过去24h)</h2>
        <p><em>以下新闻涵盖最新军事冲突实况与国际社会表态：</em></p>
        
        <h3 style="color: #b91c1c; margin-top: 20px; border-left: 4px solid #b91c1c; padding-left: 10px;">⚔️ 军事冲突与战场动态</h3>
        
        <div class="news-item">
            <strong>【AP News】伊朗报复性打击海湾阿拉伯国家能源设施</strong><br>
            继以色列轰炸波斯湾南帕尔斯（South Pars）天然气田后，伊朗加大了对周边海湾阿拉伯国家能源设施的打击力度。<br>
            <a href="https://apnews.com/live/iran-war-israel-trump-03-20-2026" target="_blank">来源：AP News (2026-03-20)</a>
        </div>
        
        <div class="news-item">
            <strong>【CNN】美以伊战争进入第20天：导弹袭击特拉维夫</strong><br>
            最新实况显示，以色列在特拉维夫居民区上空拦截了多枚伊朗来袭导弹，袭击已造成严重的地面破坏。<br>
            <a href="https://www.cnn.com/2026/03/19/middleeast/us-israel-iran-middle-east-war-day-20-what-we-know-intl-hnk" target="_blank">来源：CNN (2026-03-19)</a>
        </div>
        
        <div class="news-item">
            <strong>【Times of Israel】伊朗发射第6轮导弹，美国发出干预警告</strong><br>
            自午夜起，伊朗已向以色列发射了6轮导弹。美国警告称，若伊朗袭击卡塔尔等地的能源节点，美军将直接出手干预。<br>
            <a href="https://www.timesofisrael.com/liveblog-march-19-2026/" target="_blank">来源：Times of Israel (2026-03-19)</a>
        </div>

        <div class="news-item">
            <strong>【LiveMint】阿联酋迪拜居民收到导弹空袭警报</strong><br>
            随着战火在整个中东蔓延，阿联酋迪拜居民的手机收到了防空警报，警告可能有来自伊朗的导弹威胁。<br>
            <a href="https://www.livemint.com/news/us-news/iran-war-news-live-updates-us-israel-iran-war-middle-east-latest-news-today-19-march-2026-11773877038727.html" target="_blank">来源：LiveMint (2026-03-19)</a>
        </div>

        <div class="news-item">
            <strong>【Fox News】特拉维夫附近遇袭后燃起大火</strong><br>
            视频画面曝光了伊朗导弹袭击以色列特拉维夫附近后的火灾与严重破坏，紧急救援人员正在现场进行搜救。<br>
            <a href="https://www.foxnews.com/world/iran-missile-strike-tel-aviv-aftermath-video" target="_blank">来源：Fox News (2026-03-19)</a>
        </div>

        <div class="news-item">
            <strong>【Independent】美防长称哈尔克岛(Kharg Island)成美军战略核心</strong><br>
            美国防长表示，对伊朗哈尔克岛军事设施的压制性打击，使美国事实上“控制了该国的命运”，该岛是伊朗原油出口咽喉。<br>
            <a href="https://www.independent.co.uk/bulletin/news/iran-war-kharg-island-oil-b2941863.html" target="_blank">来源：Independent (2026-03-19)</a>
        </div>

        <h3 style="color: #1d4ed8; margin-top: 30px; border-left: 4px solid #1d4ed8; padding-left: 10px;">🌐 国际社会与各方表态</h3>

        <div class="news-item">
            <strong>【Independent】英国首相斯塔默与欧洲盟国发表联合声明谴责升级</strong><br>
            英国首相与欧洲各国领导人发表紧急联合声明，对局势升级表达“极度担忧”，呼吁必须立即停止报复性攻击。<br>
            <a href="https://www.independent.co.uk/news/uk/politics/iran-war-starmer-middle-east-joint-statement-b2941867.html" target="_blank">来源：Independent (2026-03-19/20)</a>
        </div>

        <div class="news-item">
            <strong>【ABC News】伊朗战争冲击全球格局，乌克兰和谈被迫暂停</strong><br>
            由于美国的精力被中东战火极大牵制，由美方斡旋的乌克兰和平谈判已被迫搁置，俄罗斯正准备发动新一轮攻势。<br>
            <a href="https://abcnews.com/International/wireStory/war-iran-raises-pressure-ukraine-russia-prepares-new-131243838" target="_blank">来源：ABC News (2026-03-20)</a>
        </div>

        <div class="news-item">
            <strong>【Sky News】波斯湾交火可能对全球经济带来灾难性破坏</strong><br>
            过去24小时内，昂贵的导弹在波斯湾上空频繁交汇，分析警告若能源设施遭到全面破坏，全球经济将面临重创。<br>
            <a href="https://news.sky.com/story/iran-war-last-24-hours-show-a-prolonged-conflict-could-do-calamitous-damage-to-global-economy-13521949" target="_blank">来源：Sky News (2026-03-19)</a>
        </div>

        <div class="news-item">
            <strong>【NPR】美国威胁打击伊朗核心石油资产引发市场恐慌</strong><br>
            分析人士警告，如果美军兑现摧毁哈尔克岛全部石油基础设施的警告，中东战争将指数级扩大，油价会彻底失控。<br>
            <a href="https://www.npr.org/2026/03/19/nx-s1-5750514/trump-iran-war-kharg-island-oil" target="_blank">来源：NPR (2026-03-19)</a>
        </div>

        <div class="news-item">
            <strong>【Rasanah】欧盟与中国紧急评估美以伊战争的溢出效应</strong><br>
            智库报告指出，随着危机不仅席卷中东，更向南高加索地区蔓延，欧盟与中国正紧急应对战火对贸易和地区安全的全面冲击。<br>
            <a href="https://rasanah-iiis.org/english/monitoring-and-translation/reports/the-eu-and-china-confront-the-2026-us-israel-iran-war-diverging-responses-under-the-shadow-of-the-russia-ukraine-conflict/" target="_blank">来源：Rasanah IIIS (2026-03-19)</a>
        </div>

"""

# replace everything between <h2>🌍 最新地缘政治动态 (过去24h)</h2> and <h2>📈 金融市场价格监测</h2>
pattern = re.compile(r'<h2>🌍 最新地缘政治动态 \(过去24h\)</h2>.*?<h2>📈 金融市场价格监测</h2>', re.DOTALL)

new_content = pattern.sub(new_news_section + "        <h2>📈 金融市场价格监测</h2>", content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Updated news section successfully.")
