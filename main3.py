import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

# ディレクトリのパス
input_dir = './files'

# メールアドレスと名前のカラム名
email_col = 'メールアドレス\n※ことらに連携したメールアドレスを入力してください。\n画面右上の人マーク→各種設定→ことらの設定→メールアドレス'
name_col = '名前(フルネーム)\n※プレゼント目的でのみ使用させていただきます。'

# 既存のCSVファイルを読み込んでメールアドレスと名前のマップを作成
def load_existing_data():
    csv_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]
    email_name_map = {}
    for file in csv_files:
        file_path = os.path.join(input_dir, file)
        try:
            df = pd.read_csv(file_path, encoding='utrf-8')
            if email_col in df.columns and name_col in df.columns:
                for email, name in zip(df[email_col].dropna().str.strip(), df[name_col].dropna()):
                    email_name_map[email] = name
        except Exception as e:
            print(f"Error loading {file}: {e}")
    return email_name_map

# 既存のメールアドレスと名前のマップ
existing_data = load_existing_data()

# ファイル選択処理
def select_file():
    file_path = filedialog.askopenfilename(initialdir="./", title="CSVファイルを選択", filetypes=[("CSVファイル", "*.csv"), ("すべてのファイル", "*.*")])
    if file_path:
        process_file(file_path)

# ファイル処理
def process_file(file_path):
    try:
        selected_df = pd.read_csv(file_path)
        if email_col not in selected_df.columns or name_col not in selected_df.columns:
            messagebox.showerror("エラー", "必要なカラムが見つかりません。")
            return

        selected_emails = set(selected_df[email_col].dropna().str.strip())
        selected_names = dict(zip(selected_df[email_col], selected_df[name_col]))

        # 重複と新規のメールアドレスを区別
        common_emails = selected_emails.intersection(existing_data.keys())
        unique_emails = selected_emails.difference(existing_data.keys())

        common_names = {email: existing_data[email] for email in common_emails}
        unique_names = {email: selected_names[email] for email in unique_emails}

        # 結果を表示
        display_results(common_names, unique_names)
    except Exception as e:
        messagebox.showerror("エラー", f"ファイル処理中にエラーが発生しました: {e}")

# 結果表示
def display_results(common_names, unique_names):
    result_window = tk.Toplevel(root)
    result_window.title("めっちゃ正確な結果")

    style = ttk.Style()
    style.configure("Treeview", rowheight=25)

    # 重複している人の表示
    ttk.Label(result_window, text="すでに応募された人:").pack(pady=5)
    common_tree = ttk.Treeview(result_window, columns=("Email", "Name"), show="headings", height=10)
    common_tree.heading("Email", text="メールアドレス")
    common_tree.heading("Name", text="名前")
    common_tree.column("Email", width=250)
    common_tree.column("Name", width=300)
    common_tree.pack(pady=5)
    for email, name in common_names.items():
        common_tree.insert("", "end", values=(email, name))

    # 初めて応募した人の表示
    ttk.Label(result_window, text="初めて応募した人:").pack(pady=5)
    unique_tree = ttk.Treeview(result_window, columns=("Email", "Name"), show="headings", height=10)
    unique_tree.heading("Email", text="メールアドレス")
    unique_tree.heading("Name", text="名前")
    unique_tree.column("Email", width=250)
    unique_tree.column("Name", width=300)
    unique_tree.pack(pady=5)
    for email, name in unique_names.items():
        unique_tree.insert("", "end", values=(email, name))

# メインウィンドウの設定
root = tk.Tk()
root.title("すごい重複チェッカー")

frame = ttk.Frame(root, padding=20)
frame.pack(fill=tk.BOTH, expand=True)

label = ttk.Label(frame, text="ハイパー重複チェッカー", font=("Helvetica", 16))
label.pack(pady=10)

select_button = ttk.Button(frame, text="CSVファイルを選択", command=select_file)
select_button.pack(pady=10)

root.mainloop()
