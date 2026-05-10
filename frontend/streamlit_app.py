import streamlit as st
import requests
import os
from pathlib import Path
import time

# Page configuration
st.set_page_config(
    page_title="AI Research Paper Simplifier",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced custom styling with modern design
st.markdown("""
    <style>
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Main content styling */
    .main-header {
        font-size: 3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    
    .main-subtitle {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    
    /* Section headers with gradient underline */
    .section-header {
        font-size: 1.4rem;
        color: #2d3748;
        font-weight: 700;
        margin-top: 0rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
    }
    
    /* Modern info box */
    .info-box {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        padding: 1.5rem;
        border-radius: 0.75rem;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    /* Success message */
    .success-box {
        background: linear-gradient(135deg, #10b98115 0%, #059669-15 100%);
        padding: 1.5rem;
        border-radius: 0.75rem;
        border-left: 5px solid #10b981;
        margin: 1rem 0;
    }
    
    /* Card styling */
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        border: 1px solid #e5e7eb;
        transition: all 0.3s ease;
        margin-bottom: 1rem;
        color: black;
    }
    
    .card:hover {
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
        border-color: #667eea;
    }
    
    /* File list styling */
    .file-item {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.75rem;
        border-left: 4px solid #667eea;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
    }
    
    /* Text input styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 0.5rem;
        border: 2px solid #667eea !important;
        transition: all 0.3s ease;
        background-color: #1a1a2e !important;
        color: white !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Sidebar enhancement */
    [data-testid="stSidebar"] {
        background: black;
    }
    
    .sidebar-header {
        font-size: 1.2rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Statistics display */
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 800;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
    }
    
    /* Loading spinner enhancement */
    .spinner-text {
        color: #667eea;
        font-weight: 600;
    }
    
    /* Divider styling */
    .divider {
        border: none;
        border-top: 2px solid #e5e7eb;
        margin: 2rem 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #9ca3af;
        margin-top: 3rem;
        padding-top: 2rem;
        border-top: 1px solid #e5e7eb;
        font-size: 0.9rem;
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 0.25rem;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    
    /* Answer section styling - FULL WIDTH BELOW */
    .answer-section {
        background: white;
        width: 100%;
        padding: 2rem;
        border-radius: 0.75rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        border-left: 5px solid #667eea;
        color: black;
        margin-top: 2rem;
    }
    
    /* Error message enhancement */
    .error-box {
        background: linear-gradient(135deg, #fee2e215 0%, #fecaca15 100%);
        padding: 1.5rem;
        border-radius: 0.75rem;
        border-left: 5px solid #ef4444;
        margin: 1rem 0;
    }
    
    /* Select box styling */
    .stSelectbox > div > div {
        border-radius: 0.5rem;
        border: 2px solid #667eea !important;
        background-color: #1a1a2e !important;
    }
    
    /* Fix textarea container */
    .stTextArea {
        margin-bottom: 1rem;
    }
    
    .stTextArea > div > div > textarea {
        min-height: 120px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
UPLOAD_ENDPOINT = f"{API_BASE_URL}/api/upload/"
QUERY_ENDPOINT = f"{API_BASE_URL}/api/query/"

# Initialize session state
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = {}
if "current_file_id" not in st.session_state:
    st.session_state.current_file_id = None
if "query_history" not in st.session_state:
    st.session_state.query_history = []
if "current_answer" not in st.session_state:
    st.session_state.current_answer = None

# Main header with enhanced styling
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="main-header">📚 Research Paper Simplifier</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-subtitle">Transform complex research into simple insights powered by AI</div>', unsafe_allow_html=True)

with col2:
    if st.session_state.uploaded_files:
        st.markdown(f'<div class="badge" style="margin-top: 2rem;">📄 {len(st.session_state.uploaded_files)} Paper{"s" if len(st.session_state.uploaded_files) != 1 else ""}</div>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
✨ <strong>Welcome!</strong> Upload any research paper and ask AI to explain complex concepts in simple terms. Perfect for students and researchers.
</div>
""", unsafe_allow_html=True)

# Sidebar with enhanced styling
with st.sidebar:
    st.markdown('<div class="sidebar-header">⚙️ Settings & Debug</div>', unsafe_allow_html=True)
    
    # API Configuration
    with st.expander("🔗 API Configuration", expanded=False):
        api_url = st.text_input("API Base URL", value=API_BASE_URL, key="api_url_input")
        if api_url != API_BASE_URL:
            API_BASE_URL = api_url
            UPLOAD_ENDPOINT = f"{API_BASE_URL}/api/upload/"
            QUERY_ENDPOINT = f"{API_BASE_URL}/api/query/"
    
    st.divider()
    
    # Debug section
    st.markdown('<div class="sidebar-header">🔍 Debug Tools</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏥 Server Status", use_container_width=True):
            try:
                health_response = requests.get(f"{API_BASE_URL}/health", timeout=5)
                if health_response.status_code == 200:
                    st.success("✅ Server is running")
                else:
                    st.error(f"❌ Server error: {health_response.status_code}")
            except Exception as e:
                st.error(f"❌ Cannot reach server")
    
    with col2:
        if st.button("📊 Documents", use_container_width=True):
            try:
                docs_response = requests.get(f"{API_BASE_URL}/api/query/documents", timeout=5)
                if docs_response.status_code == 200:
                    docs_data = docs_response.json()
                    st.info(f"✅ Chain: {docs_data.get('chain_ready', False)}")
                else:
                    st.error(f"❌ Error: {docs_response.status_code}")
            except Exception as e:
                st.error(f"❌ Error connecting")
    
    st.divider()
    
    # Papers list with enhanced styling
    st.markdown('<div class="sidebar-header">📚 Your Papers</div>', unsafe_allow_html=True)
    
    if st.session_state.uploaded_files:
        for idx, (file_id, file_info) in enumerate(st.session_state.uploaded_files.items()):
            with st.container():
                col1, col2 = st.columns([4, 1])
                with col1:
                    is_selected = st.session_state.current_file_id == file_id
                    button_label = f"✓ {file_info['name']}" if is_selected else f"📄 {file_info['name']}"
                    if st.button(button_label, key=f"btn_{file_id}", use_container_width=True):
                        st.session_state.current_file_id = file_id
                        st.rerun()
                with col2:
                    if st.button("✕", key=f"del_{file_id}", help="Remove"):
                        del st.session_state.uploaded_files[file_id]
                        if st.session_state.current_file_id == file_id:
                            st.session_state.current_file_id = None
                        st.rerun()
    else:
        st.caption("👆 No papers uploaded yet")

# Main content area
st.divider()

col1, col2 = st.columns([1, 1], gap="large")

# Left column: Upload section
with col1:
    st.markdown('<div class="section-header">📤 Upload & Process</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type="pdf",
        key="pdf_uploader",
        help="Select a research paper PDF file"
    )
    
    if uploaded_file is not None:
        # File preview card
        with st.container():
            st.markdown(f"""
            <div class="card">
            <strong>📎 Selected File:</strong> {uploaded_file.name}
            <br><small>Size: {uploaded_file.size / 1024:.1f} KB</small>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("🚀 Upload & Process", use_container_width=True, type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                status_text.text("📤 Uploading file...")
                progress_bar.progress(20)
                
                # Upload file to API
                files = {"file": (uploaded_file.name, uploaded_file.getbuffer(), "application/pdf")}
                response = requests.post(UPLOAD_ENDPOINT, files=files, timeout=300)
                
                progress_bar.progress(50)
                
                if response.status_code == 200:
                    result = response.json()
                    file_id = result.get("file_id", uploaded_file.name)
                    
                    progress_bar.progress(80)
                    
                    # Store in session state
                    st.session_state.uploaded_files[file_id] = {
                        "name": uploaded_file.name,
                        "pages": result.get("pages", 0),
                        "chunks": result.get("chunks", 0),
                        "status": result.get("status", "unknown")
                    }
                    st.session_state.current_file_id = file_id
                    
                    progress_bar.progress(100)
                    status_text.empty()
                    
                    # Success message with stats
                    st.markdown("""
                    <div class="success-box">
                    ✅ <strong>Paper processed successfully!</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f'<div class="stat-box"><div class="stat-value">{result.get("pages", "N/A")}</div><div class="stat-label">Pages</div></div>', unsafe_allow_html=True)
                    with col2:
                        st.markdown(f'<div class="stat-box"><div class="stat-value">{result.get("chunks", "N/A")}</div><div class="stat-label">Chunks</div></div>', unsafe_allow_html=True)
                    with col3:
                        status_badge = result.get("status", "unknown").upper()
                        st.markdown(f'<div class="stat-box"><div class="stat-label">Status</div><div class="stat-value" style="font-size: 1.2rem;">{status_badge}</div></div>', unsafe_allow_html=True)
                    
                    st.rerun()
                else:
                    st.markdown("""
                    <div class="error-box">
                    ❌ <strong>Upload failed!</strong> Please try again.
                    </div>
                    """, unsafe_allow_html=True)
                    
            except requests.exceptions.Timeout:
                st.markdown("""
                <div class="error-box">
                ⏱️ <strong>Upload timeout!</strong> The PDF is too large or processing is slow. Try a smaller file.
                </div>
                """, unsafe_allow_html=True)
            except requests.exceptions.ConnectionError:
                st.markdown(f"""
                <div class="error-box">
                ❌ <strong>Cannot connect to API!</strong> Make sure the server is running.
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"""
                <div class="error-box">
                ❌ <strong>Error:</strong> {str(e)}
                </div>
                """, unsafe_allow_html=True)
            finally:
                progress_bar.empty()
                status_text.empty()

# Right column: Query section
with col2:
    st.markdown('<div class="section-header">🤖 Ask Questions</div>', unsafe_allow_html=True)
    
    if st.session_state.uploaded_files:
        # Select which paper to query
        selected_file = st.selectbox(
            "Select a paper",
            options=list(st.session_state.uploaded_files.keys()),
            format_func=lambda x: f"📄 {st.session_state.uploaded_files[x]['name']}",
            key="file_selector"
        )
        st.session_state.current_file_id = selected_file
        
        st.divider()
        
        # Question input with helper text
        st.caption("💡 Ask anything about the paper:")
        question = st.text_area(
            "Your question:",
            placeholder="e.g., What are the main contributions? How does the methodology work?",
            height=120,
            key="question_input",
            label_visibility="collapsed"
        )
        
        # Quick questions
        col_q1, col_q2 = st.columns(2)
        with col_q1:
            if st.button("🎯 Main Ideas", use_container_width=True):
                st.session_state.quick_question = "What are the main contributions and ideas of this paper?"
        with col_q2:
            if st.button("🔬 How It Works", use_container_width=True):
                st.session_state.quick_question = "Explain the methodology and how the authors approached this problem."
        
        # Use quick question if set
        if "quick_question" in st.session_state:
            question = st.session_state.quick_question
            del st.session_state.quick_question
        
        if st.button("📬 Get Answer", use_container_width=True, type="primary"):
            if not question.strip():
                st.warning("⚠️ Please enter a question")
            else:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    status_text.text("🤔 Analyzing paper...")
                    progress_bar.progress(30)
                    
                    # Query the API
                    payload = {
                        "question": question,
                        "file_id": st.session_state.current_file_id
                    }
                    response = requests.post(QUERY_ENDPOINT, json=payload, timeout=300)
                    
                    progress_bar.progress(70)
                    
                    if response.status_code == 200:
                        result = response.json()
                        progress_bar.progress(100)
                        status_text.empty()
                        progress_bar.empty()
                        
                        # Store answer in session state to display below
                        st.session_state.current_answer = result
                        
                        # Add to history
                        st.session_state.query_history.append({
                            "question": question,
                            "timestamp": time.time()
                        })
                        
                        st.rerun()
                        
                    else:
                        st.markdown("""
                        <div class="error-box">
                        ❌ <strong>Query failed!</strong> Please try again.
                        </div>
                        """, unsafe_allow_html=True)
                        
                except requests.exceptions.Timeout:
                    st.markdown("""
                    <div class="error-box">
                    ⏱️ <strong>Query timeout!</strong> The API is taking too long. Try again.
                    </div>
                    """, unsafe_allow_html=True)
                except requests.exceptions.ConnectionError:
                    st.markdown("""
                    <div class="error-box">
                    ❌ <strong>Cannot connect to API!</strong> Make sure the server is running.
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f"""
                    <div class="error-box">
                    ❌ <strong>Error:</strong> {str(e)}
                    </div>
                    """, unsafe_allow_html=True)
                finally:
                    progress_bar.empty()
                    status_text.empty()
    else:
        st.markdown("""
        <div class="info-box">
        👈 <strong>Upload a paper first!</strong> Once you upload a PDF, you can ask questions about it.
        </div>
        """, unsafe_allow_html=True)

# ANSWER SECTION - FULL WIDTH BELOW COLUMNS
if st.session_state.current_answer:
    st.divider()
    st.markdown('<div class="section-header">📖 Answer</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="answer-section">', unsafe_allow_html=True)
    
    result = st.session_state.current_answer
    
    st.markdown("### 📖 Simple Explanation")
    st.write(result.get("simple_explanation", "No explanation available"))
    
    # Technical details
    if result.get("technical_details"):
        with st.expander("🔬 Technical Details", expanded=False):
            st.write(result.get("technical_details"))
    
    # Methodology
    if result.get("methodology"):
        with st.expander("🔧 Methodology", expanded=False):
            st.write(result.get("methodology"))
    
    # Equations
    if result.get("equations"):
        with st.expander("📐 Mathematical Details", expanded=False):
            st.write(result.get("equations"))
    
    # Key points
    if result.get("key_points"):
        with st.expander("✨ Key Points", expanded=False):
            for point in result.get("key_points", []):
                st.write(f"• {point}")
    
    # Citations
    if result.get("citations"):
        with st.expander("📚 Citations", expanded=False):
            for citation in result.get("citations", []):
                st.write(f"• {citation}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Clear button
    if st.button("🗑️ Clear Answer", use_container_width=True):
        st.session_state.current_answer = None
        st.rerun()

# Footer
st.markdown("""
<div class="footer">
<strong>📚 AI Research Paper Simplifier</strong><br>
Making complex research accessible to everyone<br>
<small>Powered by RAG & AI | Built for Students & Researchers</small>
</div>
""", unsafe_allow_html=True)