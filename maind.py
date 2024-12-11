import os
import pandas as pd

# ディレクトリのパス
input_dir = './files/'
output_file = './list.csv'

# CSVファイルを読み込む
csv_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]

# データフレームのリスト
df_list = []

# 各CSVファイルを読み込んでリストに追加
for file in csv_files:
    df = pd.read_csv(os.path.join(input_dir, file))
    df_list.append(df)

# データフレームを結合
merged_df = pd.concat(df_list)

# メアドで重複を削除（メールアドレスのカラム名を使用）
merged_df.drop_duplicates(subset='メールアドレス\n※ことらに連携したメールアドレスを入力してください。\n画面右上の人マーク→各種設定→ことらの設定→メールアドレス', keep='first', inplace=True)

# カラム名を表示して確認
print("Columns in merged DataFrame:", merged_df.columns)

# カラムの順序を指定（実際のカラム名に合わせて修正）
column_order = [
    'タイムスタンプ',
    'みんなの銀行の招待コード「YdIsoizR」を入力しましたか？\nコードの入力で、みんなの銀行から500円がもらえます。',
    '名前(フルネーム)\n※プレゼント目的でのみ使用させていただきます。',
    'メールアドレス\n※ことらに連携したメールアドレスを入力してください。\n画面右上の人マーク→各種設定→ことらの設定→メールアドレス'
]

# カラムの順序を適用
merged_df = merged_df[column_order]

# 結果をCSVファイルに出力
merged_df.to_csv(output_file, index=False)
