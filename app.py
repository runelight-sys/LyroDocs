import streamlit as st
import easyocr
from PIL import Image
import numpy as np
from groq import Groq
import streamlit as st
# ... other imports ...

# 1. SET THE BROWSER TAB LOGO
st.set_page_config(page_title="Lyro Docs", page_icon="logo.png")

# 2. DISPLAY THE LOGO AT THE TOP OF THE APP
st.image("logo.png", width=200)

# 3. YOUR TITLE
st.title("Lyro Docs")

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
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

@st.cache_resource
def load_reader():
    try:
        # This will download the models once and then stay in memory
        return easyocr.Reader(['en'], gpu=False)
    except Exception:
        return None

reader = load_reader()

if reader is None:
    st.warning("Lyro is still warming up its 'Eyes.' Please wait 30 seconds and refresh.")
    st.stop() # This prevents the rest of the app from crashing

# --- 4. INTERFACE ---
st.title("📂 Lyro Docs")
st.write("Professional Data Extraction System")

# Document Upload
uploaded_file = st.file_uploader("Upload Document", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
 
if uploaded_file is not None:
    # 1. Open the image
    image = Image.open(uploaded_file)
    
    # 2. SHRINK THE IMAGE (The Crash Fix)
    # If the photo is wider than 1000px, we scale it down
    if image.width > 1000:
        scale_factor = 1000 / image.width
        new_size = (int(image.width * scale_factor), int(image.height * scale_factor))
        image = image.resize(new_size)
    
    # 3. Display the optimized image
    st.image(image, caption="Optimizing for Lyro Docs Analysis...", use_container_width=True)
    
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
                
                # These lines below must be pushed in (indented) exactly like the ones above
                st.download_button(
                    label="📥 DOWNLOAD REPORT AS TEXT",
                    data=analysis,
                    file_name="lyro_analysis_report.txt",
                    mime="text/plain"
                )
                
                
                
            except Exception as e:

                st.error("API Key missing or invalid. Please check your Groq console.")











