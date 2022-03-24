import pandas as pd
import pymysql

con = pymysql.connect(host='localhost',
                      user='root',
                      password='ss99bu88',
                      database='金融小组',
                      charset='utf8')
cursor = con.cursor()  # 创建游标

data = pd.read_csv("C:/Users/13115925968/OneDrive/桌面/同花顺/单个概念/301620.csv", encoding="utf-8")
data = pd.DataFrame(data, columns=("名称", "链接"))
data = data.dropna(axis=0)
data = data.reset_index(drop=True)
data["概念代码"] = "301620"
for j in range(len(data)):
    data["代码"] = data["链接"].loc[j][-7:-1]
    try:
        cursor.execute('insert into 工业业(名称,链接,概念代码,代码) values(%s,%s,%s,%s)', list(data.loc[j]))
        con.commit()
    except pymysql.DatabaseError as e:
        con.rollback()
        print(e)
