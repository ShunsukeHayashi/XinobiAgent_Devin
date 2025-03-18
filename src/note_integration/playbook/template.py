"""
Playbook template for note.com integration system.
"""
import json
import os
from typing import Dict, List, Any, Optional
from jinja2 import Template

PLAYBOOK_TEMPLATE = """
◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢
# note.com自動投稿プレイブック

## 手順

{% for step in procedures %}
{{ loop.index }}. **{{ step.title }}**

   - {{ step.description }}

{% endfor %}

## アドバイスとポインター

{% for advice in advice_pointers %}
- {{ advice }}
{% endfor %}

## 禁止事項

{% for forbidden_action in forbidden_actions %}
- ⚠️ **{{ forbidden_action }}**
{% endfor %}

## ユーザー意図の解釈

◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢

**ユーザー入力:**

```
{{ user_input }}
```

◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢

### 抽象化された意図
- 元の意図: {{ original_intent }}
- 要望または必要性の意図: {{ want_or_need_intent }}

### ゴール

{% for goal in fixed_goals %}
- ✅ **{{ goal }}**
{% endfor %}

## タスク分解

{% for task in tasks %}
- [タスク {{ loop.index }}] {{ task }}
{% endfor %}

## エージェント実行スタック

{% for task in agent_tasks %}
{{ loop.index }}. タスク: **{{ task.name }}**
   - 担当エージェント: {{ task.agent }}
   - 説明: {{ task.description }}
   - 期待される結果: {{ task.outcome }}
{% endfor %}

## 環境と初期化チェック

- オペレーティングシステム: **{{ system_information.operating_system }}**
- デフォルトシェル: **{{ system_information.default_shell }}**
- ホームディレクトリ: **{{ system_information.home_directory }}**
- 現在の作業ディレクトリ: **{{ system_information.current_working_directory }}**

## 継続的実行とテスト

- ユニットテスト: {{ testing.unit_testing }}
- 全体テスト: {{ testing.overall_testing }}
- 継続的実行: {{ continuous_execution }}

## Git使用法
- コミットメッセージ: **AIが実行した内容**

◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢
"""

DEFAULT_PLAYBOOK_DATA = {
    "procedures": [
        {
            "title": "システム初期化",
            "description": "note.com統合システムを初期化し、必要な環境変数を設定します。"
        },
        {
            "title": "SEO分析",
            "description": "指定されたジャンル・テーマに基づいてSEO分析を実行します。"
        },
        {
            "title": "記事生成",
            "description": "SEO分析結果に基づいて10,000文字の記事を生成します。"
        },
        {
            "title": "記事投稿",
            "description": "生成された記事をnote.comに投稿します。"
        },
        {
            "title": "結果報告",
            "description": "投稿結果とURLを報告します。"
        }
    ],
    "advice_pointers": [
        "記事のテーマは具体的に指定してください。",
        "SEO分析には時間がかかる場合があります。",
        "記事生成には約5分かかります。",
        "投稿後、記事が公開されるまで数分かかる場合があります。",
        "モックモードでテストする場合は、USE_MOCK=Trueを設定してください。"
    ],
    "forbidden_actions": [
        "note.comの利用規約に違反するコンテンツを投稿すること。",
        "APIリクエストを過度に送信すること（レート制限に注意）。",
        "他のユーザーの記事を無断でコピーすること。",
        "センシティブな情報を含む記事を投稿すること。"
    ],
    "user_input": "",
    "original_intent": "note.comに10000字の記事を自動投稿する",
    "want_or_need_intent": "SEO分析に基づいた競合に勝てる記事を自動生成し、note.comに投稿したい",
    "fixed_goals": [
        "ユーザーが指定したジャンル・テーマに基づき、note.comのSEO競合分析を実施。",
        "競合記事を超えるSEOスコアと品質を持つ記事を毎回自動で生成（約10,000文字）。",
        "note.comの非公式エンドポイントを使用して記事を自動投稿。",
        "投稿の公開範囲・タグ・カテゴリーを最適化し、自動設定。"
    ],
    "tasks": [
        "システム初期化と環境変数の設定",
        "指定されたジャンル・テーマに基づくSEO分析",
        "SEO分析結果に基づく記事生成",
        "生成された記事のnote.comへの投稿",
        "投稿結果とURLの報告"
    ],
    "agent_tasks": [
        {
            "name": "システム初期化",
            "agent": "初期化エージェント",
            "description": "システムの初期化と環境変数の設定を行います。",
            "outcome": "システムが正常に初期化され、APIとの接続が確立されます。"
        },
        {
            "name": "SEO分析",
            "agent": "SEO分析エージェント",
            "description": "指定されたジャンル・テーマに基づいてSEO分析を実行します。",
            "outcome": "競合記事の分析結果と最適なキーワード・構造が特定されます。"
        },
        {
            "name": "記事生成",
            "agent": "コンテンツ生成エージェント",
            "description": "SEO分析結果に基づいて10,000文字の記事を生成します。",
            "outcome": "SEO最適化された高品質な10,000文字の記事が生成されます。"
        },
        {
            "name": "記事投稿",
            "agent": "投稿エージェント",
            "description": "生成された記事をnote.comに投稿します。",
            "outcome": "記事がnote.comに正常に投稿され、公開されます。"
        }
    ],
    "system_information": {
        "operating_system": "Linux",
        "default_shell": "bash",
        "home_directory": "/home/ubuntu",
        "current_working_directory": "/home/ubuntu/repos/XinobiAgent_Devin"
    },
    "testing": {
        "unit_testing": "実装済み",
        "overall_testing": "実装済み"
    },
    "continuous_execution": "実装済み"
}

def generate_playbook(data: Optional[Dict[str, Any]] = None) -> str:
    """
    Generate a playbook from the template and data.
    
    Args:
        data: Dictionary containing playbook data. If None, default data is used.
        
    Returns:
        str: Generated playbook
    """
    if data is None:
        data = DEFAULT_PLAYBOOK_DATA
    
    template = Template(PLAYBOOK_TEMPLATE)
    return template.render(**data)

def save_playbook(playbook: str, filepath: str) -> None:
    """
    Save the playbook to a file.
    
    Args:
        playbook: Playbook content
        filepath: Path to save the playbook
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(playbook)

def load_playbook_data(filepath: str) -> Dict[str, Any]:
    """
    Load playbook data from a JSON file.
    
    Args:
        filepath: Path to the JSON file
        
    Returns:
        Dict[str, Any]: Playbook data
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

if __name__ == "__main__":
    # Generate default playbook
    playbook = generate_playbook()
    print(playbook)
