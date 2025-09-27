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
        
        # Create a system prompt for Ayurvedic context
        system_prompt = """
        You are 'AyurBuddy', a friendly and helpful AI assistant for an Ayurvedic Panchakarma center.
        Your primary role is to answer questions about Panchakarma therapies, Ayurvedic principles, 
        patient care, and treatment protocols. Always be conversational, clear, and concise.
        
        Important guidelines:
        1. Base your answers on authentic Ayurvedic knowledge
        2. Explain concepts in simple terms for patients to understand
        3. For therapy-related questions, include pre and post procedure precautions
        4. If a question is outside your knowledge scope, politely decline and suggest consulting with an Ayurvedic doctor
        5. Be supportive and encouraging for patients undergoing treatments
        """
        
        # Format the conversation history for the model
        history_for_ai = []
        for msg in conversation_history:
            # The 'role' is either 'user' or 'assistant', and 'parts' is the text
            role = "user" if msg["is_user"] else "model"
            history_for_ai.append({"role": role, "parts": [msg["text"]]})
        
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
            "You are AyurBuddy, an Ayurvedic assistant. Answer the user's question based primarily on the content of the uploaded document. If the answer isn't in the document, you can use your general knowledge of Ayurveda.",
            file_part,
            f"\n\nUser's Question: {user_query}"
        ]
        
        # Generate the response
        response = model.generate_content(prompt_parts)
        return response.text
    except Exception as e:
        return f"I'm sorry, I encountered an error processing your file: {str(e)}. Please try again."