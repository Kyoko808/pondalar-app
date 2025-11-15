import streamlit as st
import requests
import os
import json

# ============================
#   UI 設定（テーマカラーなど）
# ============================
st.set_page_config(
    page_title="Pondalar v0.1",
    page_icon="🌿",
    layout="wide"
)

# カスタムCSS（プレゼン映えのミント×沼グリーン）
st.markdown("""
<style>
body {
    background-color: #f1f7f5;
    font-family: "Hiragino Sans", "Noto Sans JP", sans-serif;
}

.header-box {
    background: linear-gradient(90deg, #a8dbc8, #6fb89c);
    padding: 20px 30px;
    border-radius: 12px;
    margin-bottom: 20px;
    color: white;
}

.pondalar-title {
    font-size: 32px;
    font-weight: 700;
    margin: 0;
}

.pondalar-sub {
    font-size: 16px;
    opacity: 0.9;
}

.card {
    background: white;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

.card img {
    width: 100%;
    border-radius: 8px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ============================
#   ヘッダー
# ============================
st.markdown("""
<div class="header-box">
  <div class="pondalar-title">🌿 Pondalar — AI 湿地ナビゲーター</div>
  <div class="pondalar-sub">比企丘陵の自然・文化を学び、探究し、創作につなげるAIパートナー</div>
</div>
""", unsafe_allow_html=True)

# ============================
#       タブ UI
# ============================
tab1, tab2, tab3 = st.tabs(["💬 Pondalar と話す", "🔍 キーワード検索", "🛡 安全検索（教育利用可）"])


# ============================================
#   ⛅ Japan Search API 検索（共通関数）
# ============================================
def search_api(keyword, safe_only=False):
    base = "https://jpsearch.go.jp/api/item/search/jps-cross?"
    params = f"keyword={keyword}&size=30"

    # 安全検索 → 教育利用可(CCBY/CC0/PDM/incr_edu 等)
    if safe_only:
        rights = ["ccby", "cc0", "pdm", "incr_edu", "ccbysa"]
        for r in rights:
            params += f"&f-rights={r}"

    url = base + params
    try:
        res = requests.get(url, timeout=10)
        data = res.json()
    except Exception as e:
        st.error(f"Japan Search API の呼び出しでエラーが発生しました: {e}")
        return []

    items = []
    for d in data.get("list", []):
        c = d.get("common", {})
        items.append({
            "title": c.get("title"),
            "provider": c.get("provider"),
            "rights": c.get("contentsRightsType"),
            "link": c.get("linkUrl"),
            "thumb": c.get("thumbnail", "")
        })

    return items


# ============================================
#   🟢 タブ1：Pondalar と話す（AIチャット）
# ============================================
with tab1:
    st.write("Pondalar に話しかけてみてください。検索や探究のヒントを返します。")

    user_text = st.text_input("あなたのメッセージ")

    if st.button("送信"):
        if not user_text.strip():
            st.warning("メッセージを入力してください。")
        else:
            st.markdown(f"**あなた：** {user_text}")

            api_key = st.secrets.get("OPENAI_API_KEY")
            if not api_key:
                st.error("OpenAI APIキーが設定されていません。（Streamlit の Secrets に OPENAI_API_KEY を登録してください）")
            else:
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}",
                }

                payload = {
                    "model": "gpt-4o-mini",
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "あなたは『Pondalar』というAI湿地ナビゲーターです。"
                                "比企丘陵の谷津沼や湿地文化に関心を持つ学習者・創作者をやさしく支援します。"
                                "一人称は「わたし」、語尾は丁寧な「〜です／〜ます」。"
                                "探究の問いを深める質問を返したり、Japan Search API で調べるためのキーワードを提案したりします。"
                            ),
                        },
                        {
                            "role": "user",
                            "content": user_text,
                        },
                    ],
                }

                try:
                    res = requests.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers=headers,
                        data=json.dumps(payload),
                        timeout=30,
                    )
                    data = res.json()
                except Exception as e:
                    st.error(f"OpenAI API 呼び出しでエラーが発生しました: {e}")
                    data = {}

                # 返却形式ごとに安全に取り出す
                pondalar_reply = None

                # 1) 通常の chat.completions 形式
                if isinstance(data, dict) and "choices" in data:
                    try:
                        pondalar_reply = data["choices"][0]["message"]["content"]
                    except Exception:
                        pondalar_reply = None

                # 2) エラー形式
                if not pondalar_reply and isinstance(data, dict) and "error" in data:
                    msg = data["error"].get("message", "不明なエラー")
                    pondalar_reply = f"OpenAI API からエラーが返されました：{msg}"

                # 3) それでも取れなければデバッグ表示
                if not pondalar_reply:
                    pondalar_reply = (
                        "すみません、うまく返答を生成できませんでした。"
                        "しばらく時間をおいてから再度お試しください。"
                    )

                st.markdown(f"**Pondalar：** {pondalar_reply}")


# ============================================
#   🔍 タブ2：通常検索
# ============================================
with tab2:
    st.write("Japan Search API でキーワード検索します。")

    keyword = st.text_input("検索キーワードを入力", "湿地", key="kw_normal")

    if st.button("検索する 🔍"):
        results = search_api(keyword)
        st.write(f"**検索結果：{len(results)} 件**")

        col1, col2 = st.columns(2)
        for i, item in enumerate(results):
            col = col1 if i % 2 == 0 else col2
            with col:
                st.markdown("<div class='card'>", unsafe_allow_html=True)

                if item["thumb"]:
                    st.image(item["thumb"])
                else:
                    st.image("https://via.placeholder.com/300x200?text=No+Image")

                st.markdown(f"**タイトル：** {item['title']}")
                st.markdown(f"**提供機関：** {item['provider']}")
                st.markdown(f"**権利種別：** {item['rights']}")
                if item["link"]:
                    st.markdown(f"[出典ページを開く]({item['link']})")

                st.markdown("</div>", unsafe_allow_html=True)


# ============================================
#   🛡 タブ3：安全検索（教育利用可）
# ============================================
with tab3:
    st.write("ccby / cc0 / pdm / incr_edu など、教育利用可能な素材に限定して検索します。")

    keyword_safe = st.text_input("検索キーワードを入力", "湿地", key="kw_safe")

    if st.button("安全検索する 🛡"):
        results = search_api(keyword_safe, safe_only=True)
        st.write(f"**教育利用可の検索結果：{len(results)} 件**")

        if not results:
            st.info("このキーワードでは教育利用可能な素材が見つかりませんでした。キーワードを変えてみてください。")

        col1, col2 = st.columns(2)
        for i, item in enumerate(results):
            col = col1 if i % 2 == 0 else col2
            with col:
                st.markdown("<div class='card'>", unsafe_allow_html=True)

                if item["thumb"]:
                    st.image(item["thumb"])
                else:
                    st.image("https://via.placeholder.com/300x200?text=No+Image")

                st.markdown(f"**タイトル：** {item['title']}")
                st.markdown(f"**提供機関：** {item['provider']}")
                st.markdown(f"**権利種別：** {item['rights']}")
                if item["link"]:
                    st.markdown(f"[出典ページを開く]({item['link']})")

                st.markdown("</div>", unsafe_allow_html=True)


