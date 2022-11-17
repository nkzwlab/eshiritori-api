# ORF 絵しりとり モデル

ORF絵しりとりで使うためのモデル。このレポジトリのコードでは絵を受け取って、書かれた絵に対して推論し、分類結果をクラス名で返す。

※ 全体的に結構雑です。

## 環境設定

### 1.docker-composeのバージョン確認
```
docker-compose -v
```
の出力が `docker-compose version 1.29.2, build 5becea4c` じゃなかったら、docker-composeのバージョンを上げる

参照：https://qiita.com/kottyan/items/c892b525b14f293ab7b3

### 2.docker環境の立ち上げ
```
make init
```
して、docker環境を立ち上げる。

### 3.データセットのダウンロード
```
make run filename=src/dataset.py
```
で、データセットをダウンロードする。（少し時間がかかるはず）


## 動かし方
ファイルを動かしたい場合は、
```
make run filename=src/ファイル名.py
```
で動かす


## データセット

[quickdraw dataset](https://quickdraw.withgoogle.com/data) を使う。
- 手書きのスケッチ 345 クラスから成る、合計5000万枚のデータセット
- [クラス名一覧](https://github.com/googlecreativelab/quickdraw-dataset/blob/master/categories.txt)

## 学習

### データセットのダウンロード
```
python3 src/dataset.py
```

### 学習
- 細かいハイパラ等は全てファイルに直書きしてます。
- wandbと連携しているので、wandbを使いたくない場合はwandbに関わる行を全てコメントアウトしてください
```
python3 src/main.py
```

## 推論

### ファイル構造の設定

- ./
    - weights
        - [word2vec](https://drive.google.com/file/d/1ylxV7rWsSL1qDthTQeOiwZmgXyftDSbz/view?usp=sharing)
            - model.vec
        - [resnet50_best.pth](https://drive.google.com/file/d/1KS2eZnX6IMG4TqUayECx9C3nMWWq6lAR/view?usp=sharing)

### 推論
```
python3 src/inference.py
```

