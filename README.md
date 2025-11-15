# pondalar-app
Pondalar は、比企丘陵・谷津沼をテーマにした  
「学習×探究×創作を支援する AI 湿地ナビゲーター」です。

このアプリは Streamlit + OpenAI API + Japan Search API を使用して構築されています。
学習者が気軽に調べ学習・探究テーマづくり・創作アイデアづくりを行えるように設計しています。

---

## 🌿 機能概要

### 1. 💬 Pondalar と話す（AI チャット）
- 探究テーマの相談  
- 湿地・谷津沼の自然文化の案内  
- Japan Search API を使った調査方法の提案  
- 一人称「わたし」、丁寧語、やさしいトーン

### 2. 🔍 キーワード検索（Japan Search API）
- 任意のキーワードで文化資源を検索  
- 出典リンク・提供機関・権利情報を表示  
- サムネイル画像も表示

### 3. 🛡 安全検索（教育利用可）
- ccby / cc0 / pdm / incr_edu / ccbysa のみ抽出  
- 学校・WS・探究授業で「安心して使える素材」だけをフィルタリング

---

## 🚀 セットアップ（開発者向け）

### 1. 必要なもの
- GitHub アカウント  
- Streamlit Community Cloud  
- OpenAI API Key（gpt-4o-mini など）

### 2. Streamlit Secrets に API Key を設定
アプリ管理画面 → “Edit Secrets”

```toml
OPENAI_API_KEY = "sk-xxxx..."

## 開発フローメモ（自分用）

### 1. コードの編集（ブラウザ版 VS Code）

1. ブラウザでリポジトリを開く  
   https://github.com/Kyoko808/pondalar-app

2. キーボードで `.`（ドット）キーを押す  
   → `https://github.dev/...` のブラウザ版 VS Code が開く

3. 左の Explorer から `app.py` を開き、内容を編集する

4. `⌘+S`（Ctrl+S）で保存する

---

### 2. GitHub への commit & push

1. 左端の「Source Control（Y字アイコン）」をクリック
2. `Changes` に `app.py` が表示されていることを確認
3. 上部のメッセージ欄に、例）`Update Pondalar chat` などと入力
4. `Commit` ボタン（または「✓」アイコン）を押す  
   → 初回は「Stage and commit?」と聞かれたら **Yes**
5. 右下に `Sync` / `Push` などが出たらクリック  
   → これで GitHub の `master` ブランチに反映される

---

### 3. Streamlit Cloud への反映

1. Streamlit の管理画面を開く  
   https://share.streamlit.io/

2. `kyoko808 / pondalar-app` のアプリを開く

3. アプリ画面右上または左上にある **`Rerun`** ボタンを押す  
   - 場合によっては `Manage app` → `Rerun` / `Restart` のこともある

4. 数秒待つと新しいコードでアプリが再実行される  
   → タブ1のチャットや検索の挙動を確認する

---

### 4. トラブル時のメモ

- 画面に `OpenAI API からエラーが返されました` と出た場合  
  - `Secrets` に設定した `OPENAI_API_KEY` が正しいか確認する
- Japan Search API のエラーが出た場合  
  - ネットワークや API 側の一時的な問題のことが多いので、少し時間をおいて再度試す


