import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 設定 ---
st.set_page_config(page_title="irodori-letter", page_icon="✉️", layout="centered")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーが設定されていません。")

st.markdown("""
    <style>
    .main { background-color: #fffaf0; }
    h1 { color: #d2691e; text-align: center; }
    .stButton>button { 
        width: 100%; height: 3.5em; font-size: 1.2rem !important; 
        background-color: #ff8c00; color: white; border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("✉️ いろどりレター")
st.write("今日のごはんを写真に撮るか、フォルダから選んでください。")

tab1, tab2 = st.tabs(["📸 その場で撮影", "📁 写真から選ぶ"])

img_file = None
with tab1:
    img_cam = st.camera_input("カメラを起動")
    if img_cam: img_file = img_cam
with tab2:
    img_up = st.file_uploader("写真フォルダから選ぶ", type=['jpg', 'jpeg', 'png'])
    if img_up: img_file = img_up

if img_file is not None:
    image = Image.open(img_file)
    # ログに出ていた修正（width='stretch'）をここに反映しました
    st.image(image, caption='今日のごはん', width='stretch')
    
    if st.button("AIにお便りをお願いする"):
        with st.spinner('AIがじっくりお返事を書いています...'):
            try:
                # 404エラーを避けるため、最新のモデル名を指定
                model = genai.GenerativeModel('gemini-1.5-flash-latest')
                
                prompt = """
                あなたは優しくて写真に詳しい食生活アドバイザーです。
                送られた食事の写真を分析し、以下の形式で日本語で回答してください。
                1. 今日の点数（100点満点）
                2. 栄養バランス
                3. 優しい褒め言葉
                4. アドバイス
                """
                
                response = model.generate_content([prompt, image])
                
                if response.text:
                    st.success("お返事が届きました！")
                    st.markdown("---")
                    st.write(response.text)
                
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
