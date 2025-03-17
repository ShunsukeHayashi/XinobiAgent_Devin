# Enhanced Devin UI 使用ガイド

このガイドでは、Enhanced Devin UIを使用してEnhanced Devinシステムと対話する方法を説明します。

## 概要

Enhanced Devin UIは、Enhanced Devinシステムと対話するためのウェブベースのインターフェースを提供します。以下のことが可能です：

- セッションの作成と管理
- メッセージの送信とファイルのアップロード
- エージェントの応答とアクションの表示

## インストール

UIを使用する前に、必要な依存関係をインストールする必要があります：

```bash
pip install gradio==5.21.0 aiohttp matplotlib numpy psutil
```

## UIの実行

UIを実行するには、次のコマンドを使用します：

```bash
python run_simple_gradio_ui.py --share
```

コマンドラインオプション：

- `--api-key`: Devin APIのAPIキー（デモの場合はオプション）
- `--port`: UIを実行するポート（デフォルト：7860）
- `--host`: UIを実行するホスト（デフォルト：0.0.0.0）
- `--share`: Gradioの共有機能を使用して公開URLを作成
- `--debug`: デバッグモードを有効にする

## UIの使用方法

### APIキーの設定

1. 「API Key」フィールドにDevin APIキーを入力します
2. 「Set API Key」をクリックします

注：デモ目的では、APIキーなしでUIを使用できます。この場合、モックAPIクライアントが使用されます。

### セッションの管理

1. 「Session Name」フィールドに新しいセッションの名前を入力します
2. 「Create Session」をクリックします
3. 既存のセッションをロードするには、「Active Sessions」ドロップダウンからセッションを選択し、「Load Session」をクリックします
4. セッションのリストを更新するには、「Refresh」をクリックします

### メッセージの送信

1. 「Message」フィールドにメッセージを入力します
2. オプションで、「Upload File」ボタンを使用してファイルをアップロードします
3. 「Send Message」をクリックします

### エージェントアクションの表示

「Agent Actions」パネルには、メッセージに応答してエージェントが実行したアクションが表示されます。各アクションには以下が含まれます：

- Time：アクションが実行された時間
- Action：エージェントが行ったこと
- Status：アクションが正常に完了したかどうか

## 例

### 例1：セッションの作成とメッセージの送信

1. 「Session Name」フィールドに「My First Session」と入力します
2. 「Create Session」をクリックします
3. 「Message」フィールドに「こんにちは、Enhanced Devin！」と入力します
4. 「Send Message」をクリックします
5. チャット履歴でエージェントの応答を確認します

### 例2：公開URLでのUIの使用

1. `--share`オプションを付けてUIを実行します：
   ```bash
   python run_simple_gradio_ui.py --share
   ```
2. コンソールに表示される公開URLをコピーします
3. URLを他の人と共有して、UIにアクセスできるようにします

## トラブルシューティング

### 問題：UIが起動しない

必要な依存関係がすべてインストールされていることを確認してください：

```bash
pip install gradio==5.21.0 aiohttp matplotlib numpy psutil
```

### 問題：UIに接続できない

リモートサーバーでUIを実行している場合は、正しいホストとポートを使用していることを確認してください：

```bash
python run_simple_gradio_ui.py --host 0.0.0.0 --port 7860
```

### 問題：UIが遅い

デバッグモードでUIを実行して、問題がないか確認してください：

```bash
python run_simple_gradio_ui.py --debug
```

## 結論

Enhanced Devin UIは、Enhanced Devinシステムと対話するためのシンプルで直感的な方法を提供します。セッションの作成、メッセージの送信、エージェントの応答とアクションの表示が可能です。
