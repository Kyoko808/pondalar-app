import streamlit as st
import requests
import os

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

    # 安全検索 → 教育利用可(CCBY/CC0/PDM/incr_edu)
    if safe_only:
        rights = ["ccby", "cc0", "pdm", "incr_edu", "ccbysa"]
        for r in rights:
            params += f"&f-rights={r}"

    url = base + params
    res = requests.get(url).json()

    items = []
    for d in res.get("list", []):
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
#   🟢 タブ1：Pondalar と話す（擬似チャット）
# ============================================
with tab1:
    st.write("Pondalar に話しかけてみてください。検索や探究のヒントを返します。")

    user_text = st.text_input("あなたのメッセージ")

    if st.button("送信"):
        if user_text.strip():
            # シンプルな返答の擬似LLM（後で本物のAIに置き換える）
            st.markdown(f"**あなた：** {user_text}")

            pondalar_reply = f"それは面白いですね。`{user_text}` に関連する資料をJapan Search APIから探すこともできますよ。キーワード検索タブで試してみてくださいね🌿"

            st.markdown(f"**Pondalar：** {pondalar_reply}")


# ============================================
#   🔍 タブ2：通常検索
# ============================================
with tab2:
    st.write("Japan Search API でキーワード検索します。")

    keyword = st.text_input("検索キーワードを入力", "湿地")

    if st.button("検索する 🔍"):
        results = search_api(keyword)
        st.write(f"**検索結果：{len(results)} 件**")

        col1, col2 = st.columns(2)
        for i, item in enumerate(results):
            with (col1 if i % 2 == 0 else col2):
                st.markdown("<div class='card'>", unsafe_allow_html=True)

                if item["thumb"]:
                    st.image(item["thumb"])
                else:
                    st.image("https://
