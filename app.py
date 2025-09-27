# app.py
import streamlit as st
from firebase_service import log_conversation
from gemini_service import get_campus_response, get_gemini_response_with_file, translate_text, summarize_text

# Page configuration
st.set_page_config(
    page_title="CampusBuddy - Multilingual Campus Assistant",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 2rem;
    }
    .language-selector {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .quick-actions {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #3b82f6;
    }
    .feature-buttons {
        display: flex;
        gap: 0.5rem;
        margin-top: 1rem;
        flex-wrap: wrap;
    }
    .feature-btn {
        background: #e0e7ff;
        color: #3730a3;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .feature-btn:hover {
        background: #c7d2fe;
        transform: translateY(-2px);
    }
    .chat-container {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

if 'user_language' not in st.session_state:
    st.session_state.user_language = 'en'

if 'last_response' not in st.session_state:
    st.session_state.last_response = ""

# Language options
languages = {
    'en': 'English',
    'hi': 'हिन्दी (Hindi)',
    'mr': 'मराठी (Marathi)'
}

# Main content area
st.markdown("<h1 class='main-header'>🎓 CampusBuddy</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Your multilingual campus assistant for fees, scholarships, timetables, and more!</p>", unsafe_allow_html=True)

# Language selector
st.markdown('<div class="language-selector">', unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])
with col1:
    selected_lang = st.selectbox(
        "Choose your preferred language / अपनी पसंदीदा भाषा चुनें / आपली पसंतीची भाषा निवडा:",
        options=list(languages.keys()),
        format_func=lambda x: languages[x],
        key='lang_selector'
    )
    st.session_state.user_language = selected_lang
with col2:
    st.markdown("### 🌐")
st.markdown('</div>', unsafe_allow_html=True)

# Quick action buttons
st.markdown('<div class="quick-actions">', unsafe_allow_html=True)
st.markdown("### 🚀 Quick Actions / त्वरित कार्य / जलद क्रिया")
st.markdown("Click any button to ask about common campus topics / सामान्य कैंपस विषयों के बारे में पूछने के लिए कोई भी बटन क्लिक करें:")
feature_buttons = st.columns(4)

quick_queries = {
    "Fee Deadlines": ["What are the upcoming fee deadlines?", "आगामी शुल्क की समय-सीमाएं क्या हैं?", "आगामी फी निर्धारित कालावधी काय आहेत?"],
    "Scholarships": ["Tell me about available scholarships", "उपलब्ध छात्रवृत्तियों के बारे में बताएं", "उपलब्ध शिष्यवृत्तींबद्दल सांगा"],
    "Timetable": ["Check timetable changes", "समय-सारणी में बदलाव देखें", "वेळापत्रकातील बदल तपासा"],
    "Library": ["Library hours and services", "पुस्तकालय समय और सेवाएं", "ग्रंथालय वेळ आणि सेवा"]
}

if feature_buttons[0].button("💰 Fee Deadlines", key="fees", use_container_width=True):
    st.session_state.pending_query = quick_queries["Fee Deadlines"][list(languages.keys()).index(st.session_state.user_language)]

if feature_buttons[1].button("🏆 Scholarships", key="scholarships", use_container_width=True):
    st.session_state.pending_query = quick_queries["Scholarships"][list(languages.keys()).index(st.session_state.user_language)]

if feature_buttons[2].button("📅 Timetable", key="timetable", use_container_width=True):
    st.session_state.pending_query = quick_queries["Timetable"][list(languages.keys()).index(st.session_state.user_language)]

if feature_buttons[3].button("📚 Library", key="library", use_container_width=True):
    st.session_state.pending_query = quick_queries["Library"][list(languages.keys()).index(st.session_state.user_language)]

st.markdown('</div>', unsafe_allow_html=True)

# File upload for multimodal queries
uploaded_file = st.file_uploader("Upload a document or image (circular, timetable, form, etc.) / दस्तावेज़ या छवि अपलोड करें / कागदपत्र किंवा प्रतिमा अपलोड करा:",
                                 type=['pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg'])

# Chat interface
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for message in st.session_state.conversation_history:
    with st.chat_message("user" if message["is_user"] else "assistant"):
        st.markdown(message["text"])
st.markdown('</div>', unsafe_allow_html=True)

# User input
user_query = st.chat_input("Ask about fees, scholarships, timetable, or any campus query... / शुल्क, छात्रवृत्ति, समय-सारणी के बारे में पूछें... / फी, शिष्यवृत्ती, वेळापत्रकाबद्दल विचारा...")

# Handle pending quick query
if 'pending_query' in st.session_state and st.session_state.pending_query:
    user_query = st.session_state.pending_query
    st.session_state.pending_query = None

if user_query:
    # Add user message to history
    st.session_state.conversation_history.append({"is_user": True, "text": user_query})

    with st.chat_message("user"):
        st.markdown(user_query)

    # Get response from CampusBuddy
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking... / सोच रहा हूं... / विचार करत आहे..."):
            if uploaded_file:
                # Get file type
                file_type = uploaded_file.name.split('.')[-1]
                response = get_gemini_response_with_file(user_query, uploaded_file, file_type)
            else:
                response = get_campus_response(user_query, st.session_state.conversation_history, st.session_state.user_language)

            st.markdown(response)
            st.session_state.last_response = response

            # Add assistant response to history
            st.session_state.conversation_history.append({"is_user": False, "text": response})

            # Log conversation
            log_conversation(user_query, "campus_query", response)

    # Clear uploaded file after processing
    if uploaded_file:
        uploaded_file = None

# Feature buttons for translation and summarization
if st.session_state.last_response:
    st.markdown("---")
    st.markdown("### 🛠️ Tools / उपकरण / साधने")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🌐 Translate to English", key="translate_en"):
            if st.session_state.user_language != 'en':
                translated = translate_text(st.session_state.last_response, "English")
                st.session_state.last_response = translated
                # Update the last message in history
                if st.session_state.conversation_history:
                    st.session_state.conversation_history[-1]["text"] = translated
                st.rerun()

    with col2:
        if st.button("🌐 अनुवाद हिंदी में", key="translate_hi"):
            if st.session_state.user_language != 'hi':
                translated = translate_text(st.session_state.last_response, "Hindi")
                st.session_state.last_response = translated
                if st.session_state.conversation_history:
                    st.session_state.conversation_history[-1]["text"] = translated
                st.rerun()

    with col3:
        if st.button("🌐 मराठीत अनुवाद करा", key="translate_mr"):
            if st.session_state.user_language != 'mr':
                translated = translate_text(st.session_state.last_response, "Marathi")
                st.session_state.last_response = translated
                if st.session_state.conversation_history:
                    st.session_state.conversation_history[-1]["text"] = translated
                st.rerun()

    with col4:
        if st.button("📝 Summarize / संक्षिप्त करें / सारांश", key="summarize"):
            summary = summarize_text(st.session_state.last_response)
            st.session_state.last_response = summary
            if st.session_state.conversation_history:
                st.session_state.conversation_history[-1]["text"] = summary
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b;'>
    <strong>CampusBuddy</strong> - Your Multilingual Campus Assistant<br>
    Built with ❤️ for students and staff | 24/7 Support | Multi-language Assistance
</div>
""", unsafe_allow_html=True)