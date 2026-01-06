import streamlit as st
import easyocr
from PIL import Image
import numpy as np
from groq import Groq

# --- 1. PAGE CONFIGURATION (Must be first) ---
st.set_page_config(page_title="Lyro Docs", layout="centered")

# --- 2. STEALTH DESIGN & CUSTOM COLORS ---
st.markdown("""
    <style>
    /* Hide Streamlit default UI elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main Background - Pitch Black */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }

    /* Target Text Area - Matrix Green Style */
    .stTextArea textarea {
        background-color: #0a0a0a !important;
        color: #00FF41 !important;
        border: 1px solid #333333 !important;
        font-family: 'Courier New', monospace;
    }

    /* Buttons - Tactical Grey/Green */
    .stButton>button {
        width: 100%;
        border-radius: 2px;
        border: 1px solid #4CAF50;
        background-color: #000000;
        color: #4CAF50;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #4CAF50;
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INITIALIZE ENGINES ---
# IMPORTANT: Replace the key below with your actual Groq API Key
# Replace the old client line with this secure one:
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
reader = easyocr.Reader(['en']) 

# --- 4. INTERFACE ---
st.title("📂 Lyro Docs")
st.write("Professional Data Extraction System")

# Document Upload
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    
    # Action Button
    if st.button("EXECUTE ANALYSIS"):
        with st.spinner("Lyro is scanning..."):
            # Step A: OCR Extraction (The Eyes)
            image_np = np.array(image)
            raw_results = reader.readtext(image_np, detail=0)
            full_text = " ".join(raw_results)
            
            st.subheader("Raw Data Stream")
            st.text_area("OCR Output", full_text, height=150)

            # Step B: AI Logic (The Brain)
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are Lyro Docs, a professional data assistant. Extract key info and provide clear instructions."
                        },
                        {
                            "role": "user",
                            "content": f"Extract Name, Date, ID numbers, and key instructions from this text: {full_text}",
                        }
                    ],
                    model="llama-3.3-70b-versatile",
                )
                
                analysis = chat_completion.choices[0].message.content
                st.subheader("Lyro Analysis Report")
                st.markdown(analysis)
                
            except Exception as e:
                st.error("API Key missing or invalid. Please check your Groq console.")