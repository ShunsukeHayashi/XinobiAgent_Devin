# note.com自動投稿プレイブック

## 概要

このプレイブックは、note.comに10,000文字の記事を自動投稿するためのシステムを実行するためのものです。ユーザーが指定したテーマとジャンルに基づいて、SEO分析を行い、競合に勝てる記事を自動生成し、note.comに投稿します。

## 使用方法

### コマンドライン

```bash
python src/note_integration/playbook/run.py --theme "テーマ" --genre "ジャンル" [--input "追加入力"] [--use-mock]
```

### 対話モード

```bash
python src/note_integration/playbook/run.py
```

対話モードでは、テーマ、ジャンル、追加入力を対話的に入力できます。

### 引数

- `--theme`: 記事のテーマ
- `--genre`: 記事のジャンル
- `--input`: 記事の追加入力（任意）
- `--use-mock`: モックモードを使用する（テスト用）
- `--no-mock`: モックモードを使用しない（本番用）
- `--output`: 結果を保存するファイルパス（デフォルト: results.json）
- `--playbook-output`: プレイブックを保存するファイルパス（デフォルト: playbook.md）

## 環境変数

以下の環境変数を設定する必要があります：

- `NOTE_USERNAME`: note.comのユーザー名
- `NOTE_PASSWORD`: note.comのパスワード
- `OPENAI_API_KEY`: OpenAI APIキー

## 実行例

```bash
# テーマ「Python」、ジャンル「プログラミング」の記事を生成して投稿
python src/note_integration/playbook/run.py --theme "Python" --genre "プログラミング"

# モックモードでテスト
python src/note_integration/playbook/run.py --theme "Python" --genre "プログラミング" --use-mock

# 追加入力を指定
python src/note_integration/playbook/run.py --theme "Python" --genre "プログラミング" --input "初心者向けの内容で、基礎から応用までカバーしてください。"
```

## 出力

実行結果は指定したファイル（デフォルト: results.json）に保存されます。また、プレイブックは指定したファイル（デフォルト: playbook.md）に保存されます。

## プレイブックの構造

プレイブックは以下の構造を持ちます：

- 手順: システム初期化、SEO分析、記事生成、記事投稿、結果報告
- アドバイスとポインター: 実行時の注意点
- 禁止事項: 実行時に禁止されている行為
- ユーザー意図の解釈: ユーザーの入力と意図の解釈
- ゴール: 達成すべき目標
- タスク分解: 実行するタスクの分解
- エージェント実行スタック: 各タスクを実行するエージェントの情報
- 環境と初期化チェック: 実行環境の情報
- 継続的実行とテスト: テストと継続的実行の情報
