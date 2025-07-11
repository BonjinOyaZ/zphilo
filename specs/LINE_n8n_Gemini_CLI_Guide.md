# LINE・n8n・Gemini CLI フロー構築ガイド

## ✅ 全体像：どんな流れで繋がる？

```
① LINE → ② n8n → ③ Gemini CLI → ④ OpenAI/Gemini API（対話・分析）→ LINEへ返答
```

---

## 🔧 ステップバイステップ構築法

### 🧩 前提：必要なツール

| ツール           | 役割                               |
|------------------|------------------------------------|
| LINE Developers  | Messaging APIの発行・Webhook設定   |
| n8n              | 自動化ワークフロー構築             |
| Gemini CLI       | ローカル/サーバー上のAI操作        |
| Dify (任意)      | フロント＋RAG向けLLMフレームワーク |
| Supabase         | 長期記憶/RAG DB                     |

---

### ① LINE公式アカウントの構築・Webhook設定

- LINE Developers にログインし、Messaging APIチャネルを作成
- Webhook URLを `https://yourdomain.com/webhook` のように設定（後で n8n に接続）
- チャネルアクセストークンを発行

---

### ② n8nにWebhookを用意する

- n8nにログイン（Cloud でも Docker でもOK）
- Webhookノードを作成し、LINE用のPOSTを受け取れるように設定
  - パス：`/webhook`
  - メソッド：`POST`
- HTTP Requestノードを追加して、Gemini CLIやOpenAIへ渡すテキストを整形

---

### ③ Gemini CLIと連携（2つのやり方）

#### ☑️ A. n8n→Gemini CLIへローカル実行（スクリプト呼び出し）

```bash
gemini chat -m gemini-1.5-pro -i "ユーザーからの質問：{{ $json["message"] }}"
```

- 結果は標準出力から取得して、LINEに返す

#### ☑️ B. Gemini CLI を API サーバーとして常時起動

- `gemini serve` 機能や Node.js で Geminix API のようなラッパーを作成し、n8n から HTTP Request を投げる

---

### ④ Gemini CLI or GPT の応答をLINEへ返信

```json
{
  "replyToken": "{{ $json["replyToken"] }}",
  "messages": [
    {
      "type": "text",
      "text": "{{ $json["gemini_response"] }}"
    }
  ]
}
```

---

## 🌍 海外の事例紹介

1. **Builder.io × n8n × OpenAI**
   - SlackやLINEのリクエストに対し、ChatGPTを通じた分析・コード提案を返す
2. **Gemini CLI × Zapier互換**
   - Gemini CLIをn8nからCLIモードで操作、ファイル・プロンプトを自動管理
3. **台湾のChat2LINE AIエージェント**
   - Google Apps Scriptやn8n経由でGeminiに質問送信し、セキュアに返答

---

## 🧠 応用：哲学RAGやZ-COREとの連携

| 統合ポイント         | 実装のヒント                            |
|----------------------|------------------------------------------|
| 自己哲学データ保存     | SupabaseまたはNotion DB連携              |
| RAGによる知識回答     | Gemini CLIをLangChain経由で拡張          |
| 哲学ズレ検知           | n8n内でログ比較＋Gemini CLIで質問        |
| アバター返信（将来）   | LINE Flex Message＋Ready Player Me活用    |

---

## ✅ まとめ：この連携でできること

- LINEをフロントにして、GeminiやRAGとつながるAIエージェントが完成
- 哲学ベースの対話・判断支援を「ユーザーの伴侶」のようにLINEで提供
- ワークフローもn8nで自動化され、個人にも企業にも展開しやすい

---

## 🔁 Gemini CLIの結果をLINEに返す方法

### フロー概要

```
LINEメッセージ → n8n Webhook → Gemini CLI呼び出し → stdout取得 → HTTP RequestでLINE返信
```

### 実装ステップ

#### ① Gemini CLI を `Execute Command` で呼び出す

```bash
gemini chat -m gemini-1.5-pro -i "{{ $json["events"][0]["message"]["text"] }}"
```

#### ② 実行結果の取得（stdout）

```json
{
  "stdout": "これはGeminiの返答です。",
  "stderr": "",
  "exitCode": 0
}
```

#### ③ LINEへの返信構成

**URL**:
```
https://api.line.me/v2/bot/message/reply
```

**ヘッダー**:
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer {チャネルアクセストークン}"
}
```

**BODY**:
```json
{
  "replyToken": "{{ $json["events"][0]["replyToken"] }}",
  "messages": [
    {
      "type": "text",
      "text": "{{ $node["Execute Command"].json["stdout"] }}"
    }
  ]
}
```

---

## 🧪 補足ポイント

| チェック項目 | 内容 |
|--------------|------|
| Gemini CLI   | PATHに通っていること（`which gemini`で確認） |
| 実行時間     | 長い返答にはn8nのタイムアウトを拡張          |
| 改行処理     | `.trim()` などで整形するのが◎                 |

---

## 📦 サンプルn8nフローJSON付き

実際のn8nフローJSONファイルは以下にあります：

→ [LINE_GeminiCLI_n8n_sample.json](LINE_GeminiCLI_n8n_sample.json)

