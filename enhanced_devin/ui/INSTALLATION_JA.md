# Enhanced Devin Gradio UI インストールガイド

このガイドでは、Enhanced Devin Gradio UIのインストールと設定方法について説明します。

## 前提条件

- Python 3.8以上
- pip（Pythonパッケージインストーラー）
- Git（リポジトリのクローン用）

## インストール手順

1. リポジトリをクローンする：

```bash
git clone https://github.com/ShunsukeHayashi/XinobiAgent_Devin.git
cd XinobiAgent_Devin
```

2. 必要な依存関係をインストールする：

```bash
pip install gradio matplotlib numpy psutil
```

3. Devin APIキーを設定する：

```bash
export DEVIN_API_KEY=your_api_key_here
```

または、UI実行時に提供することもできます。

## UIの実行

提供されているスクリプトを使用してUIを実行できます：

```bash
# 実行スクリプトを使用
python enhanced_devin/ui/run_ui.py --share

# ランチャーを使用
python enhanced_devin/ui/launcher.py --share

# テスト統合スクリプトを使用
python enhanced_devin/ui/test_integration.py --share

# 公開URL用スクリプトを使用
python run_gradio_ui_with_public_url.py

# テストスクリプトを使用
python test_run_enhanced_devin_ui.py --share
```

コマンドラインオプション：

- `--api-key`: Devin APIのAPIキー（環境変数`DEVIN_API_KEY`でも設定可能）
- `--port`: UIを実行するポート（デフォルト：7860）
- `--host`: UIを実行するホスト（デフォルト：0.0.0.0）
- `--share`: Gradioの共有機能を使用して公開URLを作成
- `--debug`: デバッグモードを有効にする

## インストールの確認

UIを実行すると、次のような出力が表示されるはずです：

```
Starting Enhanced Devin Gradio UI
Running on local URL:  http://0.0.0.0:7860
Running on public URL: https://xxx-xxx-xxx.gradio.live
```

提供されたURLをWebブラウザで開くことで、UIにアクセスできます。

## トラブルシューティング

問題が発生した場合：

- すべての必要な依存関係をインストールしたことを確認する
- Devin APIキーが正しく設定されていることを確認する
- `--debug`フラグでデバッグモードを有効にする
- エラーメッセージについてコンソール出力を確認する

## 次のステップ

インストール後、UIの使用方法については[使用ガイド](README_USAGE_JA.md)を参照してください。
