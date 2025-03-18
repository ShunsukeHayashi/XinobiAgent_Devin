"""
Mock data for testing the note.com integration web UI.
"""

# Mock SEO analysis result
MOCK_SEO_ANALYSIS = {
    "top_keywords": {
        "Python": 15,
        "プログラミング": 12,
        "初心者": 10,
        "開発": 8,
        "AI": 7,
        "機械学習": 6,
        "データ分析": 5,
        "ウェブ開発": 4,
        "アプリ開発": 3,
        "自動化": 2
    },
    "most_successful": {
        "most_viewed": "Pythonで始める機械学習入門",
        "most_liked": "初心者でもわかるPython自動化スクリプト"
    },
    "structure": {
        "avg_paragraphs": 12,
        "avg_lists": 3,
        "avg_links": 5,
        "avg_images": 2
    }
}

# Mock article
MOCK_ARTICLE = {
    "title": "Pythonプログラミングの基礎から応用まで",
    "content": """
    <h1>Pythonプログラミングの基礎から応用まで</h1>
    
    <p>Pythonは、初心者にも扱いやすく、かつ高度な処理も可能なプログラミング言語です。この記事では、Pythonの基礎から応用までを解説します。</p>
    
    <h2>1. Pythonの特徴</h2>
    
    <p>Pythonは以下のような特徴を持っています：</p>
    
    <ul>
        <li>シンプルで読みやすい構文</li>
        <li>豊富なライブラリ</li>
        <li>多様な分野での活用</li>
        <li>クロスプラットフォーム対応</li>
    </ul>
    
    <h2>2. 環境構築</h2>
    
    <p>Pythonを始めるには、まず環境を整える必要があります。公式サイトからインストーラーをダウンロードするか、Anacondaなどのディストリビューションを利用するのが一般的です。</p>
    
    <h2>3. 基本構文</h2>
    
    <p>Pythonの基本構文は非常にシンプルです。以下に例を示します：</p>
    
    <pre><code>
    # 変数の宣言と代入
    name = "Python"
    version = 3.9
    
    # 条件分岐
    if version >= 3.6:
        print(f"{name}は最新バージョンです")
    else:
        print(f"{name}はアップデートが必要です")
    
    # ループ
    for i in range(5):
        print(f"カウント: {i}")
    </code></pre>
    
    <h2>4. データ構造</h2>
    
    <p>Pythonには以下のような基本的なデータ構造があります：</p>
    
    <ul>
        <li>リスト（List）: [1, 2, 3, 4, 5]</li>
        <li>タプル（Tuple）: (1, 2, 3)</li>
        <li>辞書（Dictionary）: {"key": "value"}</li>
        <li>集合（Set）: {1, 2, 3}</li>
    </ul>
    
    <h2>5. 関数とモジュール</h2>
    
    <p>関数は再利用可能なコードブロックです：</p>
    
    <pre><code>
    def greet(name):
        return f"こんにちは、{name}さん！"
    
    message = greet("太郎")
    print(message)  # こんにちは、太郎さん！
    </code></pre>
    
    <h2>6. ライブラリの活用</h2>
    
    <p>Pythonの強みは豊富なライブラリにあります：</p>
    
    <ul>
        <li>NumPy: 数値計算</li>
        <li>Pandas: データ分析</li>
        <li>Matplotlib: データ可視化</li>
        <li>TensorFlow/PyTorch: 機械学習</li>
        <li>Django/Flask: Web開発</li>
    </ul>
    
    <h2>7. 実践的なプロジェクト</h2>
    
    <p>以下のようなプロジェクトに取り組むことで、Pythonの理解を深めることができます：</p>
    
    <ul>
        <li>Webスクレイピング</li>
        <li>データ分析ダッシュボード</li>
        <li>機械学習モデルの構築</li>
        <li>自動化スクリプト</li>
        <li>Webアプリケーション</li>
    </ul>
    
    <h2>8. 応用テクニック</h2>
    
    <p>より高度なPythonプログラミングには以下のようなテクニックがあります：</p>
    
    <ul>
        <li>デコレータ</li>
        <li>ジェネレータ</li>
        <li>コンテキストマネージャ</li>
        <li>非同期プログラミング</li>
        <li>メタプログラミング</li>
    </ul>
    
    <h2>9. パフォーマンス最適化</h2>
    
    <p>Pythonプログラムのパフォーマンスを向上させるには：</p>
    
    <ul>
        <li>適切なデータ構造の選択</li>
        <li>アルゴリズムの最適化</li>
        <li>NumPyなどの高速ライブラリの活用</li>
        <li>Cythonによる拡張</li>
        <li>並列処理の導入</li>
    </ul>
    
    <h2>10. まとめ</h2>
    
    <p>Pythonは初心者から上級者まで幅広く使えるプログラミング言語です。基礎をしっかり学び、実践的なプロジェクトに取り組むことで、スキルを向上させることができます。</p>
    """,
    "tags": ["Python", "プログラミング", "初心者", "開発", "チュートリアル"]
}

# Mock article URL
MOCK_ARTICLE_URL = "https://note.com/shunsuke_ai/n/n765a359e920b"
