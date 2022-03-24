import pandas as pd
import pymysql

con = pymysql.connect(host='localhost',
                      user='root',
                      password='ss99bu88',
                      database='金融小组',
                      charset='utf8')
cursor = con.cursor()  # 创建游标
df = pd.read_csv("C:/Users/13115925968/OneDrive/桌面/同花顺/all_data.csv", encoding="gb18030")
df = pd.DataFrame(df, columns=("日期", "概念名称", "驱动时间", "成分股数量", "链接"))
df = df.dropna(axis=0)

for i in range(1, len(df)+1):
    df["代码"] = df["链接"].loc[i][-7:-1]
    try:
        cursor.execute("insert into 概念(日期,概念名称,驱动时间,成分股数量,链接,代码) values(%s,%s,%s,%s,%s,%s)", list(df.loc[i]))
        con.commit()
    except pymysql.DatabaseError as e:
        con.rollback()
        print(e)
