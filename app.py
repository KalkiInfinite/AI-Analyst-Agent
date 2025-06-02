from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from utils.file_parser import parse_file
from utils.chat_agent import chat_with_agent
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Smart Data Analyst Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
            <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Inter', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 95%;
    }
    
    .main-header {
        text-align: center;
        color: #ffffff;
        font-size: 3.5rem;
        font-weight: 400;
        font-family: 'Bebas Neue', cursive;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: 0.05em;
    }
    
    .sub-header {
        text-align: center;
        color: #a0a0a0;
        font-size: 1.2rem;
        margin-bottom: 3rem;
        font-weight: 300;
        font-family: 'Bebas Neue', cursive;
        letter-spacing: 0.05em;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .chat-container {
        margin-bottom: 1.5rem;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.2rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin-left: 20%;
        margin-bottom: 1rem;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
    }
    
    .ai-message {
        background: rgba(255, 255, 255, 0.08);
        color: #e0e0e0;
        padding: 1.2rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin-right: 20%;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    }
    
    .message-label {
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        background: rgba(255, 255, 255, 0.08);
        transform: translateY(-2px);
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #667eea;
        display: block;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #a0a0a0;
        margin-top: 0.25rem;
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 0.75rem 1rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.5rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stFileUploader > div > div {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 2px dashed rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
    }
    
    .section-header {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 400;
        font-family: 'Bebas Neue', cursive;
        margin-bottom: 1.5rem;
        border-bottom: 2px solid rgba(102, 126, 234, 0.3);
        padding-bottom: 0.5rem;
        letter-spacing: 0.05em;
    }
    
    .stSuccess {
        background: rgba(76, 175, 80, 0.1) !important;
        border: 1px solid rgba(76, 175, 80, 0.3) !important;
        border-radius: 12px !important;
        color: #81c784 !important;
    }
    
    .stWarning {
        background: rgba(255, 152, 0, 0.1) !important;
        border: 1px solid rgba(255, 152, 0, 0.3) !important;
        border-radius: 12px !important;
        color: #ffb74d !important;
    }
    
    div[data-testid="stAppViewContainer"] > div:first-child {
        font-family: 'Bebas Neue', cursive !important;
    }
</style>

""", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown('<h1 class="main-header">Smart Data Analyst Agent</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Upload your data and get intelligent insights through natural language queries</p>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose your document",
    type=["pdf", "docx", "txt", "csv", "xlsx", "png", "jpg", "jpeg"],
    help="Supported formats: PDF, DOCX, TXT, CSV, XLSX, PNG, JPG, JPEG"
)

query = st.text_input(
    "Ask a question about your file",
    placeholder="What insights can you provide from this data?",
    help="Type your question here and press Enter"
)

if uploaded_file:
    parsed = parse_file(uploaded_file)
    if isinstance(parsed, pd.DataFrame):
        df, text = parsed, None
    else:
        df, text = None, parsed
    
    st.success(f"File '{uploaded_file.name}' uploaded successfully")
    
    if df is not None:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-header">Data Overview</h3>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div class="metric-card"><span class="metric-value">{df.shape[0]}</span><div class="metric-label">Rows</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><span class="metric-value">{df.shape[1]}</span><div class="metric-label">Columns</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card"><span class="metric-value">{len(df.select_dtypes(include="number").columns)}</span><div class="metric-label">Numeric</div></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="metric-card"><span class="metric-value">{len(df.select_dtypes(include="object").columns)}</span><div class="metric-label">Text</div></div>', unsafe_allow_html=True)
        
        st.markdown("</br>", unsafe_allow_html=True)
        st.dataframe(df.head(), use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    if text:
        with st.expander("View Extracted Text Preview"):
            st.text_area(
                "Text Content",
                text[:1000] + "..." if len(text) > 1000 else text,
                height=200,
                disabled=True
            )
    
    if query:
        with st.spinner("Analyzing your question..."):
            response = chat_with_agent(query, df, text)
        st.session_state.chat_history.append((query, response))
    
    if st.session_state.chat_history:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-header">Conversation</h3>', unsafe_allow_html=True)
        
        for i, (q, r) in enumerate(st.session_state.chat_history):
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            
            st.markdown(f'''
            <div class="user-message">
                <div class="message-label">You</div>
                {q}
            </div>
            ''', unsafe_allow_html=True)
            
            st.markdown(f'''
            <div class="ai-message">
                <div class="message-label">Assistant</div>
                {r}
            </div>
            ''', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        if df is not None and st.session_state.chat_history:
            latest_query = st.session_state.chat_history[-1][0]
            if any(x in latest_query.lower() for x in ['plot', 'graph', 'chart', 'visualize']):
                try:
                    numeric_cols = df.select_dtypes(include='number').columns.tolist()
                    if len(numeric_cols) >= 2:
                        st.markdown('<h4 class="section-header">Generated Visualization</h4>', unsafe_allow_html=True)
                        
                        plt.style.use('dark_background')
                        fig, ax = plt.subplots(figsize=(12, 6))
                        fig.patch.set_facecolor('#1a1a2e')
                        ax.set_facecolor('#1a1a2e')
                        
                        df.plot(x=numeric_cols[0], y=numeric_cols[1], kind='line', ax=ax, color='#667eea', linewidth=2)
                        ax.set_title(f"{numeric_cols[1]} vs {numeric_cols[0]}", color='white', fontsize=14, pad=20)
                        ax.tick_params(colors='white')
                        ax.spines['bottom'].set_color('#667eea')
                        ax.spines['top'].set_color('#667eea')
                        ax.spines['right'].set_color('#667eea')
                        ax.spines['left'].set_color('#667eea')
                        plt.xticks(rotation=45)
                        plt.tight_layout()
                        st.pyplot(fig)
                except:
                    st.warning("Automatic visualization failed. Please refine your question for better results.")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Clear Conversation", type="secondary", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #666; padding: 1rem; font-size: 0.9rem;">'
    'Ask specific questions like "What are the key insights?" or "Create a visualization of the data"'
    '</div>',
    unsafe_allow_html=True
)