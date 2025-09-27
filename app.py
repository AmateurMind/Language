# app.py
import streamlit as st
from firebase_service import log_conversation
from gemini_service import get_gemini_response, get_gemini_response_with_file

# Page configuration
st.set_page_config(
    page_title="Language Agnostic Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E8B57;
        text-align: center;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #3CB371;
        text-align: center;
        margin-bottom: 2rem;
    }
    [data-testid="stSidebar"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Main content area
st.markdown("<h1 class='main-header'>Language Agnostic Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Ask me anything! I can help with questions, provide information, and assist in multiple languages.</p>", unsafe_allow_html=True)

# File upload for multimodal queries
uploaded_file = st.file_uploader("Upload a document or image related to your query",
                                type=['pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg'])

# Chat interface
for message in st.session_state.conversation_history:
    with st.chat_message("user" if message["is_user"] else "assistant"):
        st.markdown(message["text"])

# User input
user_query = st.chat_input("Type your question here...")

if user_query:
    # Add user message to history
    st.session_state.conversation_history.append({"is_user": True, "text": user_query})

    with st.chat_message("user"):
        st.markdown(user_query)

    # Get response from Gemini
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if uploaded_file:
                # Get file type
                file_type = uploaded_file.name.split('.')[-1]
                response = get_gemini_response_with_file(user_query, uploaded_file, file_type)
            else:
                response = get_gemini_response(user_query, st.session_state.conversation_history)

            st.markdown(response)

            # Add assistant response to history
            st.session_state.conversation_history.append({"is_user": False, "text": response})

            # Log conversation
            log_conversation(user_query, "general_query", response)

    # Clear uploaded file after processing
    if uploaded_file:
        uploaded_file = None

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #6B8E23;'>Language Agnostic Chatbot</div>", unsafe_allow_html=True)