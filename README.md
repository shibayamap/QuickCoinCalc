# QuickCoinCalc
This program reads trading data (in CSV format) from Bitbank or GMO Coin and calculates the average acquisition cost and profit/loss for each asset in spot trading using the weighted average method.

## 機能
取引所からダウンロードしたCSVデータを読み込み、現物取引分について、銘柄ごとに総平均法で平均取得価格と損益を計算します。  
（ビットバンクまたはGMOコイン）

## 使用方法

1. 事前に `pandas` ライブラリをインストールしてください。
   ```bash
   pip install pandas

2. プログラムを実行します。
   実行後に、CSVデータのファイル名を入力してください。
   実行例:
   ```bash
   python gmo.py
   <example.csv>

## 動作確認環境
Python 3.13.1 


## 注意事項
手数料は計算に含まれていないので、実際の損益計算にはご留意ください。  
発生した損害については、一切の責任を負えません。自己責任でご使用ください。
