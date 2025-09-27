from difflib import restore
import json
from httplib2 import Credentials
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK only once
def get_firestore_client():
    # Check if already initialized
    if not firebase_admin._apps:
        try:
            # Use the service account JSON file
            cred = Credentials.Certificate('serviceAccountKey.json')
            firebase_admin.initialize_app(cred)
            st.sidebar.success("✅ Firebase connected successfully!")
        except Exception as e:
            st.sidebar.error(f"❌ Error initializing Firebase: {e}")
            return None

    return restore.client()

# Function to check Ayurvedic knowledge base in Firestore
def get_ayurvedic_answer(user_query):
    db = get_firestore_client()
    if db is None:
        return None
        
    ayurvedic_ref = db.collection("ayurvedic_knowledge")
    
    try:
        docs = ayurvedic_ref.stream()
        for doc in docs:
            knowledge_data = doc.to_dict()
            # Simple keyword matching logic
            question_keywords = knowledge_data.get("question", "").lower()
            if any(keyword in user_query.lower() for keyword in question_keywords.split()):
                return knowledge_data.get("answer", "Answer not found.")
        return None  # Return None if no match is found
    except Exception as e:
        st.error(f"Error accessing Firestore: {e}")
        return None

# Function to log the conversation to Firestore
def log_conversation(user_query, detected_intent, bot_response):
    db = get_firestore_client()
    if db is None:
        return False
        
    logs_ref = db.collection("conversation_logs")
    
    log_data = {
        "user_query": user_query,
        "detected_intent": detected_intent,
        "bot_response": bot_response,
        "timestamp": restore.SERVER_TIMESTAMP  # Uses the server's time
    }
    
    try:
        logs_ref.add(log_data)
        return True
    except Exception as e:
        st.error(f"Failed to log conversation: {e}")
        return False

# Function to get patient data
def get_patient_data(patient_id):
    db = get_firestore_client()
    if db is None:
        return None
        
    try:
        doc_ref = db.collection("patients").document(patient_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None
    except Exception as e:
        st.error(f"Error accessing patient data: {e}")
        return None

# Function to save therapy schedule
def save_therapy_schedule(patient_id, schedule_data):
    db = get_firestore_client()
    if db is None:
        return False
        
    try:
        doc_ref = db.collection("therapy_schedules").document(patient_id)
        doc_ref.set(schedule_data)
        return True
    except Exception as e:
        st.error(f"Error saving therapy schedule: {e}")
        return False

# Function to get all patients
def get_all_patients():
    db = get_firestore_client()
    if db is None:
        return []
        
    try:
        patients_ref = db.collection("patients")
        docs = patients_ref.stream()
        patients = []
        for doc in docs:
            patient_data = doc.to_dict()
            patient_data["id"] = doc.id
            patients.append(patient_data)
        return patients
    except Exception as e:
        st.error(f"Error accessing patients: {e}")
        return []

# Function to send notification
def send_notification(patient_id, notification_type, message):
    db = get_firestore_client()
    if db is None:
        return False
        
    try:
        notification_data = {
            "patient_id": patient_id,
            "type": notification_type,
            "message": message,
            "timestamp": restore.SERVER_TIMESTAMP,
            "status": "pending"  # This would be processed by a backend service
        }
        
        db.collection("notifications").add(notification_data)
        return True
    except Exception as e:
        st.error(f"Error sending notification: {e}")
        return False