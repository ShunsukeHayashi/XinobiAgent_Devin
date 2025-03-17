# Enhanced Devin UI インストールガイド

このガイドでは、Enhanced Devin UIのインストールとセットアップ方法を説明します。

## 前提条件

- Python 3.8以上
- pip（Pythonパッケージマネージャー）

## インストール

1. **リポジトリのクローン**:
   ```bash
   git clone https://github.com/ShunsukeHayashi/XinobiAgent_Devin.git
   cd XinobiAgent_Devin
   ```

2. **依存関係のインストール**:
   ```bash
   pip install gradio aiohttp matplotlib numpy psutil
   ```

## UIの実行

1. **簡易UIの実行**:
   ```bash
   python run_simple_gradio_ui.py
   ```

2. **公開URLで実行**:
   ```bash
   python run_simple_gradio_ui.py --share
   ```

3. **デバッグモードで実行**:
   ```bash
   python run_simple_gradio_ui.py --debug
   ```

4. **特定のポートで実行**:
   ```bash
   python run_simple_gradio_ui.py --port 8080
   ```

## 設定

モックモードでは追加の設定は必要ありません。UIは自動的にモックAPIクライアントを使用します。

## トラブルシューティング

1. **ポートが既に使用されている**:
   - 別のポートを試してみてください：
     ```bash
     python run_simple_gradio_ui.py --port 8080
     ```

2. **UIが読み込まれない**:
   - すべての依存関係がインストールされていることを確認してください
   - デバッグモードで実行して、より詳細なエラーメッセージを確認してください：
     ```bash
     python run_simple_gradio_ui.py --debug
     ```

3. **モジュールが見つからないエラー**:
   - リポジトリのルートディレクトリからスクリプトを実行していることを確認してください
   - すべての依存関係がインストールされていることを確認してください
