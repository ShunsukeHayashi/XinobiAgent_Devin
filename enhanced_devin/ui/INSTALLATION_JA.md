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
   pip install gradio matplotlib numpy psutil
   ```

## 設定

1. **APIキーの設定**:
   - オプション1：`DEVIN_API_KEY`環境変数を設定する：
     ```bash
     export DEVIN_API_KEY=your_api_key
     ```
   - オプション2：コマンドライン引数としてAPIキーを渡す：
     ```bash
     python run_enhanced_devin_ui.py --api-key your_api_key
     ```

## UIの実行

1. **公開URLでUIを実行する**:
   ```bash
   python run_enhanced_devin_ui.py
   ```

2. **デバッグモードでUIを実行する**:
   ```bash
   python run_enhanced_devin_ui.py --debug
   ```

3. **特定のポートでUIを実行する**:
   ```bash
   python run_enhanced_devin_ui.py --port 8080
   ```

## トラブルシューティング

1. **ポートが既に使用されている**:
   - 別のポートを試してみてください：
     ```bash
     python run_enhanced_devin_ui.py --port 8080
     ```

2. **APIキーが機能しない**:
   - 正しいAPIキーを設定していることを確認してください
   - APIキーに必要な権限があることを確認してください

3. **UIが読み込まれない**:
   - すべての依存関係がインストールされていることを確認してください
   - デバッグモードで実行して、より詳細なエラーメッセージを確認してください：
     ```bash
     python run_enhanced_devin_ui.py --debug
     ```
