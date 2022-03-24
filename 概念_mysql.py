import os
import pandas as pd
import pymysql

con = pymysql.connect(host='localhost',
                      user='root',
                      password='ss99bu88',
                      database='金融小组',
                      charset='utf8')
cursor = con.cursor()  # 创建游标

df = pd.read_csv("C:/Users/13115925968/OneDrive/桌面/同花顺/all_data.csv", encoding="gb18030")
df = pd.DataFrame(df, columns=("概念名称", "链接"))
df = df.dropna(axis=0)
dic = {}
for i in range(1, len(df) + 1):
    dic[df["链接"].loc[i][-7:-1]] = df["概念名称"].loc[i]

for i in os.listdir("C:/Users/13115925968/OneDrive/桌面/同花顺/单个概念"):
    name = dic[i[:6]]
    try:
        cursor.execute('create table {}(名称 varchar(20), 链接 varchar(50), '
                       '概念代码 varchar(10), 代码 varchar(10))'.format(name))
        con.commit()
    except pymysql.DatabaseError as e:
        con.rollback()
        print(e)
    data = pd.read_csv("C:/Users/13115925968/OneDrive/桌面/同花顺/单个概念/{}".format(i), encoding="utf-8")
    data = pd.DataFrame(data, columns=("名称", "链接"))
    data = data.dropna(axis=0)
    data = data.reset_index(drop=True)
    data["概念代码"] = i[:6]
    for j in range(len(data)):
        data["代码"] = data["链接"].loc[j][-7:-1]
        try:
            cursor.execute('insert into {}(名称,链接,概念代码,代码) values(%s,%s,%s,%s)'.format(name), list(data.loc[j]))
            con.commit()
        except pymysql.DatabaseError as e:
            con.rollback()
            print(e)
