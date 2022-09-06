from flask import Flask,render_template,jsonify,make_response,abort,request
import peewee
import json

# 初期設定
app = Flask(__name__)

# SQLiteDBの生成
db= peewee.SqliteDatabase("data.db")

################################################################################
# データモデルクラス
class DataModel(peewee.Model):
    city = peewee.TextField()
    now = peewee.IntegerField(null=True,default=0)
    pre = peewee.IntegerField(null=True,default=0)
    updown = peewee.FloatField(null=True,default=0.0)
    area = peewee.FloatField(null=True,default=0.0)
    dense = peewee.FloatField(null=True,default=0.0)

    class Meta:
        database = db
################################################################################

# テーブルの作成
db.create_tables([DataModel])

# API実装
# データ取得API→Chart.jsで参照するのに使う
@app.route('/getData/', methods=['GET'])
def get_Ventilations():
    datalist = DataModel.select().order_by(DataModel.city)
    # グラフ描画用データセットを準備する。
    labels = []
    dataset = {
            'data':[]
            }
    # データを読み込んで、グラフ用に編集しながら追加していく。
    for v in datalist:
        labels.append(v.city)
        dataset['data'].append(v.now)

    # JSON形式で戻り値を返すために整形
    result = {
            "labels":labels,
            "datasets":[dataset]}
    return make_response(jsonify(result))

# 登録API
@app.route('/addData/', methods=['POST'])
def addData():
    # POSTされたJSONデータからキーを元にデータ取得
    print(request.json)
    jsonData = json.loads(request.json)
    print(jsonData)

    # 既存データは一度削除する。
    DataModel.delete().where(DataModel.city==jsonData["city"]).execute()
    # 登録用データを構築
    v = DataModel(city=jsonData["city"],
                now=jsonData["now"],
                pre=jsonData["pre"],
                area=jsonData["area"],
                dense=jsonData["dense"])

    # データを保存
    v.save()
    return "ok"

#####################################################################
# ページ遷移
# 初期ページ
@app.route('/')
def index():
    # トップページを表示
    return render_template('index.html')

@app.route('/table')
def table():
    # トップページを表示
    data = DataModel.select().order_by(DataModel.city)
    return render_template('table.html',data=data)



####################################################################

# サービス起動
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
