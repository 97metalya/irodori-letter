import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. 基本設定 ---
st.set_page_config(page_title="irodori-letter", page_icon="✉️")

# APIキーの読み込み
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーをSecretsに設定してください。")

st.title("✉️ いろどりレター")
st.write("今日のごはんを写真に撮るか、フォルダから選んでください。")

# --- 2. 写真の入力 ---
img_file = st.file_uploader("写真を選んでください", type=['jpg', 'jpeg', 'png'])

if img_file is not None:
    image = Image.open(img_file)
    st.image(image, caption='今日のごはん', width=400) # 古い書き方を避けた指定
    
    if st.button("AIにお便りをお願いする"):
        with st.spinner('AIが考え中です...'):
            try:
                # 404エラー対策：最も標準的なモデル名に変更
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = "あなたは優しい食生活アドバイザーです。この写真の食事に点数をつけ、140文字程度で褒めて励ましてください。"
                
                # AIにお願いする
                response = model.generate_content([prompt, image])
                
                if response.text:
                    st.success("お返事が届きました！")
                    st.write(response.text)
                
            except Exception as e:
                # エラーの詳細をそのまま出す（診断用）
                st.error(f"エラーが発生しました: {e}")
                
                # 診断：このキーで使えるモデルを画面に表示してみる
                st.info("診断中：あなたのAPIキーで使用可能なモデルを表示します...")
                try:
                    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                    st.write(models)
                except:
                    st.write("モデル一覧も取得できません。APIキーが無効な可能性があります。")
