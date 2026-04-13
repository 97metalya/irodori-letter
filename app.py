import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- 1. 基本設定（ここが重要です） ---
st.set_page_config(page_title="irodori-letter", page_icon="✉️", layout="centered")

# APIキーの読み込み（Secretsから取得）
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーが設定されていません。Manage app > Settings > Secrets を確認してください。")

# --- 2. デザイン（見た目を整えます） ---
st.markdown("""
    <style>
    .main { background-color: #fffaf0; }
    h1 { color: #d2691e; text-align: center; }
    .stButton>button { 
        width: 100%; height: 3.5em; font-size: 1.1rem !important; 
        background-color: #ff8c00; color: white; border-radius: 12px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("✉️ いろどりレター")
st.write("今日のごはんを写真に撮るか、フォルダから選んでください。")

# --- 3. 写真の入力（インカメラ対策としてタブを分けました） ---
tab1, tab2 = st.tabs(["📸 その場で撮影", "📁 写真から選ぶ"])

img_file = None

with tab1:
    # ブラウザによっては自撮り側になるため、切り替えボタンを使ってください
    img_file_cam = st.camera_input("カメラを起動します")
    if img_file_cam:
        img_file = img_file_cam

with tab2:
    img_file_up = st.file_uploader("スマホの写真フォルダから選ぶ", type=['jpg', 'jpeg', 'png'])
    if img_file_up:
        img_file = img_file_up

# --- 4. AIによる判定処理 ---
if img_file is not None:
    image = Image.open(img_file)
    st.image(image, caption='今日のごはん', use_container_width=True)
    
    # 判定ボタン
    if st.button("AIにお便りをお願いする"):
        with st.spinner('AIがじっくりお返事を書いています...'):
            try:
                # 404エラー対策のため、モデル名を正式なフルパスで指定します
                model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
                
                prompt = """
                あなたは優しくて写真に詳しい食生活アドバイザーです。
                送られた食事の写真を分析し、以下の形式で日本語で回答してください。
                
                1. 今日の点数（100点満点）
                2. 栄養バランス（タンパク質、脂質、糖質、野菜、果物の過不足をざっくりと）
                3. 優しい褒め言葉（盛り付けや色合いを褒める）
                4. アドバイス（「もう一色足すならこれ」という提案）
                
                シニアの方が読みやすいよう、難しい用語は使わず140文字程度の優しい口調で。
                """
                
                # AIに送信
                response = model.generate_content([prompt, image])
                
                if response:
                    st.success("お返事が届きました！")
                    st.markdown("---")
                    st.markdown(f"### 📋 AI判定結果")
                    st.write(response.text)
                
            except Exception as e:
                # エラーの詳細を表示（解決のヒントになります）
                st.error(f"エラーが発生しました: {e}")
                st.info("※APIキーの再発行や、requirements.txt の更新が必要な場合があります。")
