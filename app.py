import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. 基本設定 ---
st.set_page_config(page_title="irodori-letter", page_icon="✉️", layout="centered")

# APIキーの読み込み
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーをSecretsに設定してください。")

st.title("✉️ いろどりレター")
st.write("今日のごはんを写真に撮るか、フォルダから選んでください。")

# --- 2. 写真の入力 ---
tab1, tab2 = st.tabs(["📸 その場で撮影", "📁 写真から選ぶ"])

img_file = None
with tab1:
    img_cam = st.camera_input("カメラを起動")
    if img_cam: img_file = img_cam
with tab2:
    img_up = st.file_uploader("写真フォルダから選ぶ", type=['jpg', 'jpeg', 'png'])
    if img_up: img_file = img_up

# --- 3. 判定処理 ---
if img_file is not None:
    image = Image.open(img_file)
    # ログに出ていた修正（width='stretch'）を反映
    st.image(image, caption='今日のごはん', width='stretch')
    
    if st.button("AIにお便りをお願いする"):
        with st.spinner('最新のAIがじっくりお返事を書いています...'):
            try:
                # 【ここを修正！】関根さんのリストにある最新モデルを指定
                model = genai.GenerativeModel('models/gemini-2.5-flash')
                
                prompt = """
                あなたは優しくて写真に詳しい食生活アドバイザーです。
                送られた食事の写真を分析し、以下の形式で日本語で回答してください。
                
                1. 今日の点数（100点満点）
                2. 栄養バランス
                3. 優しい褒め言葉
                4. アドバイス
                
                140文字程度の優しい口調で。
                """
                
                response = model.generate_content([prompt, image])
                
                if response.text:
                    st.success("お返事が届きました！")
                    st.markdown("---")
                    st.write(response.text)
                
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
