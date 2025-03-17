# Canva Slide Generator

このモジュールは、Canva APIを使用してプロンプトからプレゼンテーションスライドを自動生成するシステムを実装しています。

## 概要

Canva Slide Generatorは、テキストプロンプトを入力として受け取り、Canva APIを使用して完全なプレゼンテーションを生成します。このシステムは、XinobiAgentフレームワークのWorking Backwards手法を活用して、目標から逆算して実装されています。

## 機能

- テキストプロンプトからプレゼンテーションスライドを自動生成
- スライドの数、タイトル、デザインタイプをカスタマイズ可能
- Canva APIを使用してプロフェッショナルなデザインを適用
- テキストと画像を適切に配置

## 使用方法

### 環境設定

1. Canva開発者アカウントを作成し、APIキーを取得します
2. 環境変数にAPIキーを設定します：

```bash
export CANVA_API_KEY="your_api_key_here"
```

### 基本的な使用例

```python
import asyncio
from app.examples.canva_slide_generator.slide_generator import generate_slides_from_prompt

async def example():
    result = await generate_slides_from_prompt(
        prompt="AIの最新トレンドについてのビジネスプレゼンテーション",
        num_slides=5,
        title="AI最新動向 2025",
    )
    print(result)

asyncio.run(example())
```

## アーキテクチャ

このシステムは以下のコンポーネントで構成されています：

1. **CanvaAPITool**: Canva APIとの通信を担当するツール
2. **GenericAgent**: Working Backwards手法を使用してタスクを実行するエージェント
3. **SlideGenerator**: 高レベルのインターフェースを提供するモジュール

## 制限事項

- Canva APIの利用には開発者アカウントとAPIキーが必要です
- 一部のAPIエンドポイントはプレビュー段階であり、変更される可能性があります
- 複雑なデザイン要素の自動生成には制限があります

## 今後の展望

- より高度なプロンプト処理機能の追加
- スライドテンプレートのカスタマイズオプションの拡張
- 画像生成AIとの統合によるビジュアル要素の強化

## ライセンス

このプロジェクトはMITライセンスの下で提供されています。
