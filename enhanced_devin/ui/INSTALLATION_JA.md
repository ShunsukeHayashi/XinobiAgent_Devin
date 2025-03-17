# Enhanced Devin UI インストールガイド

このガイドでは、Enhanced Devin UIのインストールとセットアップ方法を説明します。

## 前提条件

Enhanced Devin UIをインストールする前に、以下が必要です：

- Python 3.8以上
- pip（Pythonパッケージインストーラー）
- Git（リポジトリのクローン用）

## インストール手順

### 1. リポジトリのクローン

```bash
git clone https://github.com/ShunsukeHayashi/XinobiAgent_Devin.git
cd XinobiAgent_Devin
```

### 2. 依存関係のインストール

```bash
pip install gradio==5.21.0 aiohttp matplotlib numpy psutil
```

### 3. 環境のセットアップ

```bash
# オプション：仮想環境の作成
python -m venv venv
source venv/bin/activate  # Windowsの場合：venv\Scripts\activate
```

### 4. APIキーの設定（オプション）

UIまたは環境変数でAPIキーを設定できます：

```bash
export DEVIN_API_KEY=your_api_key_here
```

Windowsの場合：

```bash
set DEVIN_API_KEY=your_api_key_here
```

## UIの実行

UIを実行するには、次のコマンドを使用します：

```bash
python run_simple_gradio_ui.py
```

どこからでもアクセスできる公開URLを作成するには：

```bash
python run_simple_gradio_ui.py --share
```

## コマンドラインオプション

UIは以下のコマンドラインオプションをサポートしています：

- `--api-key`: Devin APIのAPIキー（`DEVIN_API_KEY`環境変数でも設定可能）
- `--port`: UIを実行するポート（デフォルト：7860）
- `--host`: UIを実行するホスト（デフォルト：0.0.0.0）
- `--share`: Gradioの共有機能を使用して公開URLを作成
- `--debug`: デバッグモードを有効にする

## インストールの確認

インストールが成功したことを確認するには：

1. `--debug`オプションを付けてUIを実行します：
   ```bash
   python run_simple_gradio_ui.py --debug
   ```
2. ウェブブラウザを開き、`http://localhost:7860`にアクセスします
3. Enhanced Devin UIが表示されるはずです

## トラブルシューティング

### 問題：依存関係の不足

依存関係の不足に関するエラーが発生した場合は、手動でインストールしてみてください：

```bash
pip install gradio==5.21.0
pip install aiohttp
pip install matplotlib
pip install numpy
pip install psutil
```

### 問題：ポートが既に使用中

ポートが既に使用中の場合は、別のポートを試してください：

```bash
python run_simple_gradio_ui.py --port 8080
```

### 問題：権限拒否

権限の問題が発生した場合は、sudo（Linux/Mac）でコマンドを実行してみてください：

```bash
sudo python run_simple_gradio_ui.py
```

またはコマンドプロンプトを管理者として実行してください（Windows）。

## 結論

Enhanced Devin UIのインストールが完了しました。これでEnhanced Devinシステムと対話するために使用できます。
