import streamlit as st
import requests
import os
import json

import requests
import streamlit as st

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
@@ -79,102 +81,147 @@ def search_api(keyword, safe_only=False):
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


def render_results(results):
    """共通のカード表示。"""
    if not results:
        st.info("検索結果は0件でした。別のキーワードを試してください。")
        return

    col1, col2 = st.columns(2)
    for i, item in enumerate(results):
        with (col1 if i % 2 == 0 else col2):
            st.markdown("<div class='card'>", unsafe_allow_html=True)

            if item["thumb"]:
                st.image(item["thumb"])
            else:
                st.image("https://via.placeholder.com/300x200?text=No+Image")

            st.markdown(f"**タイトル**：{item['title'] or '不明'}")
            st.markdown(f"**提供元**：{item['provider'] or '不明'}")
            st.markdown(f"**権利情報**：{item['rights'] or '記載なし'}")
            if item["link"]:
                st.markdown(f"[詳細を見る]({item['link']})")

            st.markdown("</div>", unsafe_allow_html=True)


# ============================================
#   🟢 タブ1：Pondalar と話す（AIチャット対応）
# ============================================
with tab1:
    st.write("Pondalar に話しかけてみてください。検索や探究のヒントを返します。")

    user_text = st.text_input("あなたのメッセージ")

    if st.button("送信"):
        if user_text.strip():
        if not user_text.strip():
            st.warning("メッセージを入力してください。")
        else:
            st.markdown(f"**あなた：** {user_text}")

            import requests
            import json

            api_key = st.secrets["OPENAI_API_KEY"]

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }

            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "あなたは『Pondalar』というAI湿地ナビゲーターです。"
                            "語尾は丁寧な「〜です／〜ます」。中性的に話します。"
                            "ユーザの探究を促し、ときにJapan Search APIでの検索方法もアドバイスします。"
                        )
                    },
                    {
                        "role": "user",
                        "content": user_text
                    }
                ]
            }

            # --- OpenAI API に送信 ---
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                data=json.dumps(payload)
            ).json()

            # --- 返り値の安全な取り出し ---
            try:
                pondalar_reply = response["choices"][0]["message"]["content"]
            except KeyError:
                # 新形式で返った場合
                pondalar_reply = response.get("output_text", "すみません、返答の解釈に失敗しました。")

            st.markdown(f"**Pondalar：** {pondalar_reply}")
            api_key = st.secrets.get("OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY")

            if not api_key:
                st.error("OpenAI APIキーが設定されていません。Streamlit Secrets か環境変数に OPENAI_API_KEY を設定してください。")
            else:
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}"
                }

                payload = {
                    "model": "gpt-4o-mini",
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "あなたは『Pondalar』というAI湿地ナビゲーターです。"
                                "語尾は丁寧な「〜です／〜ます」。中性的に話します。"
                                "ユーザの探究を促し、ときにJapan Search APIでの検索方法もアドバイスします。"
                            )
                        },
                        {
                            "role": "user",
                            "content": user_text
                        }
                    ]
                }

                try:
                    response = requests.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers=headers,
                        json=payload,
                        timeout=30,
                    )
                    response.raise_for_status()
                    data = response.json()

                    pondalar_reply = "すみません、返答の解釈に失敗しました。"
                    choices = data.get("choices")
                    if choices:
                        message = choices[0].get("message", {})
                        content = message.get("content")
                        if isinstance(content, list):
                            pondalar_reply = "".join(
                                block.get("text", "") for block in content if block.get("type") == "text"
                            ) or pondalar_reply
                        else:
                            pondalar_reply = content or pondalar_reply
                    else:
                        pondalar_reply = data.get("output_text", pondalar_reply)
                except requests.exceptions.RequestException as err:
                    pondalar_reply = f"API呼び出しでエラーが発生しました：{err}"
                except (KeyError, ValueError) as err:
                    pondalar_reply = f"レスポンス解析でエラーが発生しました：{err}"

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
        render_results(results)

# ============================================
#   🛡 タブ3：教育利用向け安全検索
# ============================================
with tab3:
    st.write("教育利用できる権利表記のみを対象に検索します。")

        col1, col2 = st.columns(2)
        for i, item in enumerate(results):
            with (col1 if i % 2 == 0 else col2):
                st.markdown("<div class='card'>", unsafe_allow_html=True)
    safe_keyword = st.text_input("安全検索キーワード", "湿地 (教育用)")

                if item["thumb"]:
                    st.image(item["thumb"])
                else:
                    st.image("https://via.placeholder.com/300x200?text=No+Image")
    if st.button("安全に検索する 🛡"):
        safe_results = search_api(safe_keyword, safe_only=True)
        st.write(f"**検索結果：{len(safe_results)} 件（教育利用可）**")
        render_results(safe_results)
