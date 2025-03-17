# Enhanced Devin UI スクリーンショット

このドキュメントでは、ユーザーがインターフェースとその機能を理解するのに役立つEnhanced Devin UIのスクリーンショットを提供します。

## メインインターフェース

![メインインターフェース](https://placeholder-for-screenshot-url.com/main_interface.png)

Enhanced Devin UIのメインインターフェースはいくつかのセクションで構成されています：

1. 「Enhanced Devin」というタイトルのヘッダー
2. APIキー入力フィールド
3. セッション管理セクション
4. チャットインターフェース
5. エージェントアクションパネル

## APIキー入力

![APIキー入力](https://placeholder-for-screenshot-url.com/api_key_input.png)

APIキー入力フィールドでは、Devin APIキーを入力できます。デモ目的では、モックAPIクライアントを使用するためにこのフィールドを空のままにしておくことができます。

## セッション管理

![セッション管理](https://placeholder-for-screenshot-url.com/session_management.png)

セッション管理セクションでは、以下のことができます：

1. 名前を入力して「Create Session」をクリックすることで、新しいセッションを作成する
2. 「Active Sessions」ドロップダウンから既存のセッションをロードする
3. 「Refresh」をクリックしてセッションのリストを更新する

## チャットインターフェース

![チャットインターフェース](https://placeholder-for-screenshot-url.com/chat_interface.png)

チャットインターフェースでは、以下のことができます：

1. あなたとエージェントの間のチャット履歴を表示する
2. エージェントにメッセージを送信する
3. エージェントと共有するファイルをアップロードする

## エージェントアクション

![エージェントアクション](https://placeholder-for-screenshot-url.com/agent_actions.png)

エージェントアクションパネルには、メッセージに応答してエージェントが実行したアクションが表示されます。各アクションには以下が含まれます：

- Time：アクションが実行された時間
- Action：エージェントが行ったこと
- Status：アクションが正常に完了したかどうか

## セッションの作成

![セッションの作成](https://placeholder-for-screenshot-url.com/creating_session.png)

セッションを作成するには：

1. 「Session Name」フィールドにセッションの名前を入力します
2. 「Create Session」をクリックします
3. セッションが「Active Sessions」ドロップダウンに表示されます

## メッセージの送信

![メッセージの送信](https://placeholder-for-screenshot-url.com/sending_message.png)

メッセージを送信するには：

1. 「Message」フィールドにメッセージを入力します
2. 「Send Message」をクリックします
3. メッセージがチャット履歴に表示されます
4. エージェントがメッセージで応答します
5. エージェントアクションパネルにエージェントが実行したアクションが表示されます

## ファイルのアップロード

![ファイルのアップロード](https://placeholder-for-screenshot-url.com/uploading_file.png)

ファイルをアップロードするには：

1. 「Upload File」をクリックします
2. コンピュータからファイルを選択します
3. ファイルに関連するメッセージを入力します
4. 「Send Message」をクリックします
5. エージェントがファイルのアップロードを認識します

## 公開URL共有

![公開URL共有](https://placeholder-for-screenshot-url.com/public_url_sharing.png)

UIを他の人と共有するには：

1. `--share`オプションを付けてUIを実行します：
   ```bash
   python run_simple_gradio_ui.py --share
   ```
2. 公開URLが生成され、コンソールに表示されます
3. このURLを他の人と共有して、UIにアクセスできるようにします

## デバッグモード

![デバッグモード](https://placeholder-for-screenshot-url.com/debug_mode.png)

デバッグモードでUIを実行するには：

1. `--debug`オプションを付けてUIを実行します：
   ```bash
   python run_simple_gradio_ui.py --debug
   ```
2. より詳細なログがコンソールに表示されます

## 結論

これらのスクリーンショットは、Enhanced Devin UIのビジュアルガイドを提供します。UIの使用方法の詳細については、README_USAGE_JA.mdを参照してください。
