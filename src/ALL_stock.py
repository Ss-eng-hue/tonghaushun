import os
import pandas as pd
import pymysql

con = pymysql.connect(host='localhost',
                      user='root',
                      password='ss99bu88',
                      database='金融小组',
                      charset='utf8')
cursor = con.cursor()  # 创建游标

n = 1
for i in os.listdir("C:/Users/13115925968/OneDrive/桌面/基金/"):
    df = pd.read_csv("C:/Users/13115925968/OneDrive/桌面/基金/{}".format(i))
    df = pd.DataFrame(df, columns=(
        "ts_code", "trade_date", "open", "high", "low", "close", "pre_close", "change", "pct_chg", "vol", "amount"))
    for j in range(len(df)):
        try:
            cursor.execute("insert into 概念股(ts_code,trade_date,ope_n,high,low,clos_e,pre_close,chang_e,pct_chg,vol,"
                           "amount) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", list(df.loc[j]))
            con.commit()
        except pymysql.DatabaseError as e:
            con.rollback()
            print(e)
    print("\r当前进度: {:.2f}%".format(n * 100 / 4734), end="")
    n = n + 1
