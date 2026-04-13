import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- 設定 ---
st.set_page_config(page_title="irodori-letter", page_icon="✉️", layout="centered")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーが設定されていません。")

# --- UIデザイン ---
st.markdown("""
    <style>
    .main { background-color: #fffaf0; }
    h1 { color: #d2691e; text-align: center; }
    .stButton>button { 
        width: 100%; height: 3em; font-size: 1.5rem !important; 
        background-color: #ff8c00; color: white; border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("✉️ いろどりレター")
st.write("今日の食事をパシャリと撮るだけで、AIがお返事を出します。")

img_file = st.camera_input("カメラでごはんを撮る")

if img_file is not None:
    image = Image.open(img_file)
    st.image(image, caption='今日のごはん', use_container_width=True)
    
    with st.spinner('AIが内容を確認しています...'):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = """
            あなたは優しくて写真に詳しい食生活アドバイザーです。
            送られた食事の写真を分析し、以下の形式で日本語で回答してください。
            
            1. 今日の点数（100点満点）
            2. 栄養バランス（タンパク質、脂質、糖質、野菜、果物の過不足をざっくりと）
            3. 優しい褒め言葉（盛り付けや色合いを褒める）
            4. アドバイス（「もう一色足すならこれ」という提案）
            
            シニアの方が読みやすいよう、難しい用語は使わず140文字程度の優しい口調で。
            """
            response = model.generate_content([prompt, image])
            st.success("お返事が届きました！")
            st.markdown(f"### 📋 AI判定結果")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
