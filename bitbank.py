import pandas as pd

# CSVファイルの読み込み（エンコーディングをUTF-8と指定）
file_path = input()
data = pd.read_csv(file_path, encoding='utf-8')

# 現物/信用が「現物」のデータのみを抽出
filtered_data = data[data['現物/信用'] == '現物']

# 通貨ペアごとにデータを並び替え
sorted_data = filtered_data.sort_values(by='通貨ペア')

# 通貨ペアのリストを作成
currency_pairs = sorted_data['通貨ペア'].unique().tolist()

# 各行ごとに約定金額（数量×価格）を計算して新しい列に追加
sorted_data['約定金額'] = sorted_data['数量'] * sorted_data['価格']

# 売/買ごとに合計を計算、売買を行列に集約
summary = sorted_data.groupby(['通貨ペア', '売/買']).agg({
    '数量': 'sum', 
    '約定金額': 'sum'
}).unstack(fill_value=0)

# 各列: (数量, 約定金額) の組合せを取り出す
buy_quantity = summary['数量']['buy']
buy_amount = summary['約定金額']['buy']
sell_quantity = summary['数量']['sell']
sell_amount = summary['約定金額']['sell']

# 各通貨ペアについて結果を計算
results = []

# 計算とコンソール出力
for currency_pair in currency_pairs:
    # 買関連数値
    b_quantity = buy_quantity.get(currency_pair, 0)
    b_amount = buy_amount.get(currency_pair, 0)
    # 売関連数値
    s_quantity = sell_quantity.get(currency_pair, 0)
    s_amount = sell_amount.get(currency_pair, 0)

    # 総平均単価の計算
    average_cost = b_amount / b_quantity if b_quantity != 0 else 0
    # 売却原価の計算
    sell_cost = s_quantity * average_cost
    # 手数料除く損益の計算
    profit_loss_excluding_fees = s_amount - sell_cost

    # 結果をリストに追加
    results.append({
        '通貨ペア': currency_pair,
        '買_合計数量': b_quantity,
        '買_合計金額': b_amount,
        '売_合計数量': s_quantity,
        '売_合計金額': s_amount,
        '総平均単価': average_cost,
        '売却原価': sell_cost,
        '手数料除く損益': profit_loss_excluding_fees
    })

    # コンソールに計算結果を出力
    print(f"{currency_pair}_買_合計数量: {b_quantity}")
    print(f"{currency_pair}_買_合計金額: {b_amount}")
    print(f"{currency_pair}_売_合計数量: {s_quantity}")
    print(f"{currency_pair}_売_合計金額: {s_amount}")
    print(f"{currency_pair}_総平均単価: {average_cost}")
    print(f"{currency_pair}_売却原価: {sell_cost}\n")
    print(f"{currency_pair}_手数料除く損益: {profit_loss_excluding_fees}\n")

# 結果をDataFrameに変換してresult_bb.csvに保存
result_df = pd.DataFrame(results)
result_df.to_csv('result_bb.csv', index=False, encoding='utf-8')