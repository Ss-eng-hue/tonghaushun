import pandas as pd
from bs4 import BeautifulSoup
from pyppeteer import launch
import asyncio
from loguru import logger

BROWSER_WIDTH = 1920  # 1366
BROWSER_HEIGHT = 1080  # 850

OPTIONS = {
    'headless': False,  # 可以无头
    # 'headless': True,
    'slowMo': 1.3,
    # 'userDataDir': './userdata',
    'args': [
        # f'--window-size={BROWSER_WIDTH},{BROWSER_HEIGHT}'
        '--start-maximized',
        '--enable-automation',
        '--disable-extensions',
        '--hide-scrollbars',
        '--disable-bundled-ppapi-flash',
        '--mute-audio',
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-gpu',
        '--disable-infobars'
    ],
    'dumpio': True
}


async def page_evaluate(page, width=BROWSER_WIDTH, height=BROWSER_HEIGHT):
    # 设置浏览器头部
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/83.0.4103.97 Safari/537.36")
    # 设置浏览器大小
    await page.setViewport({'width': width, 'height': height})
    # 是否启动js，enable设为false，则无渲染效果
    # await page.setJavaScriptEnabled(enabled=True)
    # js注入 防反爬
    await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } 
    });window.screen.width=1366; }''')
    await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {}, };}''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')
    await page.evaluateOnNewDocument("""() => {Object.defineProperty(navigator,'webdriver',{get:() => undefined})}""")
    logger.success("浏览器初始化成功")


# 模拟鼠标点击文本定位
async def click_credentials(page):
    num = 0
    while True:
        try:
            num += 1
            await asyncio.sleep(3)
            click_credentials_js = """()=>{
                var links=document.querySelectorAll("a");
                var lens=links.length;
                var lists=["下一页","Credentials","credentials"];
                for (var i=0;i < lens;i++){
                var tc = links[i].textContent;
                if(lists.indexOf(tc.trim()) != -1){
                    console.log(tc.trim());
                    links[i].click();
                    return true;
                }}}"""
            clickcredentials = await page.evaluate(click_credentials_js)
            if not clickcredentials:
                await page.reload()
                continue
            await asyncio.sleep(3)
            break
        except Exception as e:
            print('clickcredentials:', e)
        if num > 15:
            return


async def main():
    browser = await launch(OPTIONS)
    page = await browser.newPage()
    await page_evaluate(page)
    await page.goto("http://q.10jqka.com.cn/gn/")
    await asyncio.sleep(3)
    page_text = await page.content()  # 获取页面内容
    # 解析页面获取数据
    soup = BeautifulSoup(page_text, 'html.parser')
    table = soup.find('table', attrs={"class": "m-table m-pager-table"})
    data = table.find_all('tr')
    results = []
    for i in data:
        td = i.find_all('td')
        a = i.find_all('a')
        res = []
        for j in td:
            t = j.text.replace("\n", "")
            res.append(t)
        for k in a:
            res.append(k['href'])
        results.append(res)
    # 获取第二页到最后一页的数据
    while True:
        try:
            # 点击进入下一页
            await click_credentials(page)
            await asyncio.sleep(2)
            # 进行其他内容提取操作
            page_text = await page.content()
            soup = BeautifulSoup(page_text, 'html.parser')
            table = soup.find('table', attrs={"class": "m-table m-pager-table"})
            data = table.find_all('tr')
            for i in data:
                td = i.find_all('td')
                a = i.find_all('a')
                res = []
                for j in td:
                    t = j.text.replace("\n", "")
                    res.append(t)
                for k in a:
                    res.append(k['href'])
                results.append(res)

        except Exception as e:
            print(e)
        text = await page.querySelectorAllEval('#m-page > a', 'nodes => nodes.map(node => node.innerText)')
        if "下一页" not in text:
            break
    await browser.close()
    # 数据存储
    # df = pd.DataFrame(results, columns=["序号", "代码", "名称", "现价", "涨跌幅(%)", "涨跌", "涨速(%)", "换手(%)", "量比",
    #                                     "振幅(%)", "成交额", "流通股", "流通市值", "市盈率", "加自选"])
    df = pd.DataFrame(results, columns=["日期", "概念名称", "驱动时间", "龙头股", "成分股数量", "链接", "正文"])
    df.to_csv("C:/Users/13115925968/OneDrive/桌面/同花顺/all_data.csv")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
