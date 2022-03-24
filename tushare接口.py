# 导入tushare
import tushare as ts
import pandas as pd

data_code = pd.read_csv("C:/Users/13115925968/OneDrive/桌面/tushare_stock_basic_20220305171127.csv", encoding='gbk')
# 初始化pro接口
pro = ts.pro_api('dfe02963c0bfca842f74cffb03c1e46b46c213116f3933fddbcdfa22')
for i in range(len(data_code)):
    # 拉取数据
    try:
        df = pro.daily(**{
            "ts_code": "{}".format(data_code.loc[i][0]),
            "trade_date": "",
            "start_date": 20190305,
            "end_date": 20220305,
            "offset": "",
            "limit": ""
        }, fields=[
            "ts_code",
            "trade_date",
            "open",
            "high",
            "low",
            "close",
            "pre_close",
            "change",
            "pct_chg",
            "vol",
            "amount"
        ])
        df.to_csv("C:/Users/13115925968/OneDrive/桌面/基金/{}.csv".format(data_code.loc[i][0]))
        print("\r当前进度: {:.2f}%".format(i * 100 / len(data_code)), end="")
    except:
        continue
