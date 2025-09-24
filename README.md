情報処理安全確保支援士特定講習（METI）PDF 一括取得・結合スクリプト

目的
- 経済産業省（METI）のページ（https://www.meti.go.jp/policy/it_policy/jinzai/tokutei.html）からリンクされている「講習一覧」の PDF に記載された各講習の PDF へのリンクをたどり、各講習 PDF をダウンロードして1つに結合します。手作業で各リンクを開いて内容を確認する手間を省くためのユーティリティです。

準備
1. Python 3.8+ がインストールされていることを確認します。
2. 仮想環境を作成し、依存パッケージをインストールします。

実行方法
```bash
# 仮想環境を作る（任意）
python -m venv .venv
# Bash 環境で有効化（Windows の Git Bash / bash.exe を想定）
source .venv/Scripts/activate
# 依存パッケージをインストール
pip install -r requirements.txt
# スクリプトを実行
python main.py
```

スクリプトの振る舞い（簡単な説明）
- `main.py` はまず METI の一覧 PDF を `ichiran.pdf` としてダウンロードします。
- PDF 中の注釈（リンク）から拡張子が `.pdf` の URL を抽出します。
- 抽出した PDF を `downloads/` ディレクトリに `file_1.pdf`, `file_2.pdf`, ... のように保存します。
- ダウンロードした PDF を順に結合し、ルートに `merged.pdf` として出力します。

注意事項
- 抽出したリンク集合には順序がありません（`set()` を使っているため）。Python 3.7 以降では dict の挿入順序保証がありますが、`set` 自体は順序を保証しません。元の PDF 内の注釈順を維持したい場合は、`main.py` 側で注釈を順に処理するよう実装を変更してください。
