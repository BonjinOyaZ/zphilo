# Z-PHILO（哲学バディシステム）フェーズ0：MVP 設計書

## 🎯 プロジェクト目的

Z-PHILOは、ユーザーが自分自身の哲学・ビジョン・行動指針（バリュー）を構造化し、渋沢栄一を模したAI人格とともに日々の判断・成長を支援する“生涯哲学バディ”システムである。フェーズ0（MVP）では「哲学ゼロ地点」から始められる最小限のシステムとして以下を実現する。

## ✅ システム要件（MVP）

### 1. 開発環境

* VS Code（GitHub連携済）
* Miniconda仮想環境名：`zphilo`
* Gemini CLI（v2.5-pro, 認証済）
* GitHubリポジトリ：`https://github.com/BonjinOyaZ/zphilo`
* ローカル環境ベースでn8n, OpenHands連携も想定

### 2. 主要ファイル構成

```
zphilo/
├── zphilo.yaml        # ユーザーの哲学情報（空のテンプレから生成）
├── GEMINI.md          # 渋沢栄一の人格を定義するMarkdown
├── init_zphilo_yaml.py # 初期テンプレ生成スクリプト
├── logs/              # 哲学対話ログを格納
├── inbox/, outbox/    # Geminiへの素材と出力用
├── .env               # APIキー等（非公開）
```

### 3. 機能仕様

| 機能                 | 内容                                                                   |
| ------------------ | -------------------------------------------------------------------- |
| `zphilo.yaml` 自動生成 | `init_zphilo_yaml.py` により空テンプレを生成し、ユーザーの入力を促す                        |
| 行動指針テンプレート         | 10の代表的シチュエーションを初期状態で記述（actionは空）                                     |
| Gemini人格との対話       | **ユーザーが** `gemini chat --input GEMINI.md --input zphilo.yaml` を実行することで、渋沢栄一との壁打ちを開始 |
| 哲学育成モード            | ユーザーがvaluesを埋めていくまで対話形式でサポート                                         |
| ログ記録               | 対話ログを `logs/YYYY-MM-DD.md` に自動保存（次フェーズで自動化）                          |
| n8n連携 (LINE UI)    | LINE UIからの入力はn8nの「Execute Command」ノードを介してGemini CLIを呼び出し、その出力をLINEに返信する形で実現 |

### 4. 行動指針（values）初期テンプレ（空）

```yaml
values:
  - situation: "逆境に直面したとき"
    action: ""
  - situation: "利益と倫理が衝突したとき"
    action: ""
  - situation: "人と意見が食い違ったとき"
    action: ""
  - situation: "怒りを感じたとき"
    action: ""
  - situation: "判断に迷ったとき（優先順位）"
    action: ""
  - situation: "新しい挑戦をするか迷ったとき"
    action: ""
  - situation: "誘惑や甘えに流されそうなとき"
    action: ""
  - situation: "仲間が困っているとき"
    action: ""
  - situation: "自分の実力が足りないと痛感したとき"
    action: ""
  - situation: "誰かに裏切られたり、失望したとき"
    action: ""
```

### 5. 渋沢AI人格機能（GEMINI.md）

* 渋沢栄一の思想・口調を再現
* ユーザーの未記入`values:`に対し、質問しながら育成支援
* 将来的には「反省モード」：行動がvaluesに反している際の内省を促すフィードバックを実装予定

### 6. 今後の展望（フェーズ1以降）

* Geminiとの対話ログの保存と可視化
* 行動指針に基づくフィードバック自動化（反省モード）
* n8nやLINEとの連携による実用導線の確立
* Z哲学の「成長ログ」記録と振り返り支援

---

## 📌 備考

* 哲学は固定ではなく成長するものという前提で設計
* すべてのユーザーが「空の状態」からスタートできることを優先
* 将来的にはJAGIなど他プロジェクトとの連携も視野に入れる
