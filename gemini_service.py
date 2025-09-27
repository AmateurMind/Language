# gemini_service.py
import google.generativeai as genai
import streamlit as st

# Configure the Gemini API
def configure_genai():
    try:
        api_key = st.secrets["gemini_api_key"]
        genai.configure(api_key=api_key)
    except Exception as e:
        st.error(f"Error configuring Gemini: {e}")

# Function to get a response from Gemini (text-only)
def get_gemini_response(user_query, conversation_history):
    configure_genai()
    
    try:
        # Use the correct model name
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Create a system prompt for general assistance
        system_prompt = """
        You are 'Language Agnostic Chatbot', a friendly and helpful AI assistant that can communicate in multiple languages.
        Your primary role is to answer questions, provide information, and assist users in various topics.
        Always be conversational, clear, and concise.

        Important guidelines:
        1. Be helpful and accurate in your responses
        2. Explain concepts in simple terms
        3. If a question is outside your knowledge scope, politely say so
        4. Be supportive and encouraging
        5. Adapt to the user's language if possible
        """
        
        # Format the conversation history for the model
        history_for_ai = []
        for msg in conversation_history:
            # Convert our format to Gemini's expected format
            if "user" in msg and "assistant" in msg:
                history_for_ai.append({"role": "user", "parts": [msg["user"]]})
                history_for_ai.append({"role": "model", "parts": [msg["assistant"]]})
        
        # Start a chat session with the model, providing the system prompt and history
        chat = model.start_chat(history=history_for_ai)
        
        # Send the user's latest query
        full_query = system_prompt + "\n\nUser's question: " + user_query
        response = chat.send_message(full_query)
        return response.text
    except Exception as e:
        return f"I'm sorry, I encountered an error: {str(e)}. Please try again."

# Function to get response with file (multimodal)
def get_gemini_response_with_file(user_query, uploaded_file, file_type):
    """
    Sends a user query and an uploaded file to Gemini for analysis.
    """
    configure_genai()
    
    try:
        # Use the correct model name - gemini-2.0-flash supports multimodal input
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Read the file bytes
        file_bytes = uploaded_file.read()
        
        # Determine MIME type based on file extension
        mime_types = {
            'pdf': 'application/pdf',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'doc': 'application/msword',
            'png': 'image/png',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'txt': 'text/plain'
        }
        
        mime_type = mime_types.get(file_type.lower(), 'application/octet-stream')
        
        # Create the file part
        file_part = {
            "mime_type": mime_type,
            "data": file_bytes
        }

        # Combine the user's question and the file into the prompt
        prompt_parts = [
            "You are a helpful AI assistant. Analyze the uploaded content and answer the user's question based on what you see or read. Provide detailed and accurate information.",
            file_part,
            f"\n\nUser's Question: {user_query}"
        ]
        
        # Generate the response
        response = model.generate_content(prompt_parts)
        return response.text
    except Exception as e:
        return f"I'm sorry, I encountered an error processing your file: {str(e)}. Please try again."