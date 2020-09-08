import pandas as pd
import requests
import json

# 読込先URL
url='https://www.pref.mie.lg.jp/common/content/000869391.xlsx'

proxies = {
    "http": None,
    "https": None,
}

# 列名の定義
cols = ["city","pre","now","updown","rate","area","dense"]

df=pd.read_excel(url,          # 読込先URL
                sheet_name=1,   # シート番号/名前
                header=3,       # ヘッダ。ここから下の行を読み込む
                skipfooter=2,   # 読み飛ばすフッター行。この場合、最後2行は読み飛ばす
                index_col=0,    # IDとして読み込む列番号
                usecols=[0,1,2,3,4,5,6],   # 読み込む列番号を指定
                names = cols    # 列名の設定
                )

# 1行ごとにJSON化してPOST
for row in df.itertuples():
    jsonData = {
      "city":str(row[0]),
      "pre":row[1],
      "now":row[2],
      'updown':row[3],
      'rate':row[4],
      'area':row[5],
      'dense':row[6]
    }
    print(jsonData)
    response = requests.post('http://127.0.0.1:3000/addData/' , json=json.dumps(jsonData),proxies=proxies)
    print(response)
