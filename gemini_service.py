# gemini_service.py
import google.generativeai as genai
import streamlit as st
from campus_faq import get_faq_response

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

# Function to translate text between languages
def translate_text(text, target_language, source_language="auto"):
    """
    Translates text from source language to target language using Gemini
    """
    configure_genai()

    try:
        model = genai.GenerativeModel('gemini-2.0-flash')

        prompt = f"""
        Translate the following text to {target_language}.
        Original text: {text}
        Source language: {source_language}

        Provide only the translation, no explanations or additional text.
        """

        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Translation error: {str(e)}"

# Function to summarize text
def summarize_text(text, max_length=200):
    """
    Summarizes the given text to a specified maximum length
    """
    configure_genai()

    try:
        model = genai.GenerativeModel('gemini-2.0-flash')

        prompt = f"""
        Summarize the following text in approximately {max_length} words or less.
        Keep the key information and main points. Make it concise but informative.

        Text to summarize:
        {text}

        Summary:
        """

        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Summarization error: {str(e)}"

# Function to get campus-specific response
def get_campus_response(user_query, conversation_history, user_language="en"):
    """
    Gets response focused on campus-related queries with multilingual support
    """
    configure_genai()

    try:
        # First check if we have a direct FAQ match
        faq_response = get_faq_response(user_query, user_language)
        if faq_response:
            return faq_response

        model = genai.GenerativeModel('gemini-2.0-flash')

        # Campus-specific system prompt
        system_prompt = """
        You are CampusBuddy, a helpful multilingual chatbot for college students and staff.
        You assist with campus-related queries including:
        - Fee deadlines and payment procedures
        - Scholarship applications and requirements
        - Timetable changes and class schedules
        - Exam schedules and results
        - Hostel and accommodation information
        - Library services and resources
        - Administrative procedures
        - Campus events and activities

        Always respond in the user's preferred language when possible.
        Be conversational, clear, and concise.
        If you don't have specific information, suggest contacting relevant campus offices.
        Provide accurate, helpful information based on general campus knowledge.

        Supported languages: English (en), Hindi (hi), Marathi (mr)
        """

        # Format conversation history
        history_for_ai = []
        for msg in conversation_history[-5:]:  # Keep last 5 messages for context
            if msg.get("is_user"):
                history_for_ai.append({"role": "user", "parts": [msg["text"]]})
            else:
                history_for_ai.append({"role": "model", "parts": [msg["text"]]})

        # Start chat session
        chat = model.start_chat(history=history_for_ai)

        # Send query with language context
        full_query = f"{system_prompt}\n\nUser's language preference: {user_language}\n\nUser's question: {user_query}"
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
            "You are CampusBuddy, a helpful campus assistant. Analyze the uploaded content (circular, timetable, form, etc.) and answer the user's question based on what you see or read. Provide detailed and accurate campus-related information.",
            file_part,
            f"\n\nUser's Question: {user_query}"
        ]

        # Generate the response
        response = model.generate_content(prompt_parts)
        return response.text
    except Exception as e:
        return f"I'm sorry, I encountered an error processing your file: {str(e)}. Please try again."