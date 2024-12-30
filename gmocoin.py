import pandas as pd

# CSVファイルの読み込み（エンコーディングをUTF-8 with BOMに指定）
file_path = input()
data = pd.read_csv(file_path, encoding='utf-8-sig')

# 精算区分が「取引所現物取引」のデータのみを抽出
filtered_data = data[data['精算区分'] == '取引所現物取引']

# 銘柄名ごとにデータを並び替え
sorted_data = filtered_data.sort_values(by='銘柄名')

# 銘柄名のリストを作成
asset_list = sorted_data['銘柄名'].unique().tolist()

# 売買区分ごとに約定数量と約定金額を集計
summary = sorted_data.groupby(['銘柄名', '売買区分']).agg({
    '約定数量': 'sum',
    '約定金額': 'sum'
}).unstack(fill_value=0)

# 各売買区分の集計結果を取得
buy_quantity = summary['約定数量'].get('買', pd.Series(dtype='float64'))
buy_amount = summary['約定金額'].get('買', pd.Series(dtype='float64'))
sell_quantity = summary['約定数量'].get('売', pd.Series(dtype='float64'))
sell_amount = summary['約定金額'].get('売', pd.Series(dtype='float64'))

# 各銘柄について情報を計算
results = []

for asset in asset_list:
    # 買関連数値
    b_quantity = buy_quantity.get(asset, 0)
    b_amount = buy_amount.get(asset, 0)
    # 売関連数値
    s_quantity = sell_quantity.get(asset, 0)
    s_amount = sell_amount.get(asset, 0)

    # 総平均単価の計算
    average_cost = b_amount / b_quantity if b_quantity != 0 else 0
    # 売却原価の計算
    sell_cost = s_quantity * average_cost
    # 手数料除く損益の計算
    profit_loss_excluding_fees = s_amount - sell_cost

    # 結果をリストに追加
    results.append({
        '銘柄名': asset,
        '買_合計数量': b_quantity,
        '買_合計金額': b_amount,
        '売_合計数量': s_quantity,
        '売_合計金額': s_amount,
        '総平均単価': average_cost,
        '売却原価': sell_cost,
        '手数料除く損益': profit_loss_excluding_fees
    })

    # 各変数をコンソールに出力
    print(f"{asset}_買_合計数量: {b_quantity}")
    print(f"{asset}_買_合計金額: {b_amount}")
    print(f"{asset}_売_合計数量: {s_quantity}")
    print(f"{asset}_売_合計金額: {s_amount}")
    print(f"{asset}_総平均単価: {average_cost}")
    print(f"{asset}_売却原価: {sell_cost}")
    print(f"{asset}_手数料除く損益: {profit_loss_excluding_fees}\n")


# 結果をDataFrameに変換してresult.csvに保存
result_df = pd.DataFrame(results)
result_df.to_csv('result_gmo.csv', index=False, encoding='utf-8-sig')