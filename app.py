# app.py
import streamlit as st
import datetime
import json
from datetime import timedelta
from firebase_service import get_firestore_client, log_conversation
from gemini_service import get_gemini_response, get_gemini_response_with_file

# Page configuration
st.set_page_config(
    page_title="AyurSutra - Panchakarma Management",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
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
        border-bottom: 2px solid #3CB371;
        padding-bottom: 0.5rem;
    }
    .therapy-card {
        background-color: #F0FFF0;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 5px solid #3CB371;
        margin-bottom: 1rem;
    }
    .notification-badge {
        background-color: #FF6B6B;
        color: white;
        border-radius: 50%;
        padding: 0.2rem 0.5rem;
        font-size: 0.8rem;
        margin-left: 0.5rem;
    }
    .progress-bar {
        background-color: #E0E0E0;
        border-radius: 0.5rem;
        height: 1rem;
        margin: 0.5rem 0;
    }
    .progress-fill {
        background-color: #3CB371;
        height: 100%;
        border-radius: 0.5rem;
        text-align: center;
        color: white;
        font-size: 0.8rem;
        line-height: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"
if 'patient_data' not in st.session_state:
    st.session_state.patient_data = {}
if 'therapy_schedule' not in st.session_state:
    st.session_state.therapy_schedule = []

# Firebase initialization
db = get_firestore_client()

# Function to get patient data from Firestore
def get_patient_data(patient_id):
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

# Function to save therapy schedule to Firestore
def save_therapy_schedule(patient_id, schedule_data):
    try:
        doc_ref = db.collection("therapy_schedules").document(patient_id)
        doc_ref.set(schedule_data)
        return True
    except Exception as e:
        st.error(f"Error saving therapy schedule: {e}")
        return False

# Function to get therapy schedule from Firestore
def get_therapy_schedule(patient_id):
    try:
        doc_ref = db.collection("therapy_schedules").document(patient_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None
    except Exception as e:
        st.error(f"Error accessing therapy schedule: {e}")
        return None

# Function to send notifications
def send_notification(patient_id, notification_type, message):
    try:
        # Get patient notification preferences
        patient_data = get_patient_data(patient_id)
        if not patient_data:
            return False
        
        notification_data = {
            "patient_id": patient_id,
            "type": notification_type,
            "message": message,
            "timestamp": datetime.datetime.now(),
            "status": "sent"
        }
        
        # Save notification to Firestore
        db.collection("notifications").add(notification_data)
        
        # Here you would integrate with actual email/SMS services
        # For demo purposes, we'll just show a success message
        st.success(f"Notification sent to patient {patient_id}")
        return True
    except Exception as e:
        st.error(f"Error sending notification: {e}")
        return False

# Navigation sidebar
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #2E8B57;'>AyurSutra</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Navigation options
    page_options = {
        "Dashboard": "📊",
        "Patient Management": "👨‍👩‍👧‍👦",
        "Therapy Scheduling": "📅",
        "Progress Tracking": "📈",
        "Notifications": "🔔",
        "AyurBuddy Assistant": "🤖"
    }
    
    for page, icon in page_options.items():
        if st.button(f"{icon} {page}", use_container_width=True, key=page):
            st.session_state.current_page = page

# Main content area
st.markdown(f"<h1 class='main-header'>AyurSutra - Panchakarma Management</h1>", unsafe_allow_html=True)

# Dashboard Page
if st.session_state.current_page == "Dashboard":
    st.markdown("<h2 class='sub-header'>Dashboard</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Patients", "128", "12%")
    
    with col2:
        st.metric("Therapies Today", "24", "-3%")
    
    with col3:
        st.metric("Notification Rate", "92%", "5%")
    
    # Upcoming therapies
    st.subheader("Upcoming Therapies")
    
    # Sample data - in real app, this would come from Firestore
    upcoming_therapies = [
        {"patient": "Rahul Sharma", "therapy": "Abhyanga", "time": "10:00 AM", "status": "Scheduled"},
        {"patient": "Priya Patel", "therapy": "Shirodhara", "time": "11:30 AM", "status": "Scheduled"},
        {"patient": "Amit Kumar", "therapy": "Basti", "time": "2:00 PM", "status": "Scheduled"},
    ]
    
    for therapy in upcoming_therapies:
        with st.container():
            col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
            with col1:
                st.write(f"**{therapy['patient']}**")
            with col2:
                st.write(therapy['therapy'])
            with col3:
                st.write(therapy['time'])
            with col4:
                st.metric(label="Status", value=therapy['status'])
            st.divider()

# Patient Management Page
elif st.session_state.current_page == "Patient Management":
    st.markdown("<h2 class='sub-header'>Patient Management</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Add Patient", "View Patients", "Patient Details"])
    
    with tab1:
        with st.form("add_patient_form"):
            st.subheader("Add New Patient")
            
            col1, col2 = st.columns(2)
            
            with col1:
                patient_id = st.text_input("Patient ID")
                full_name = st.text_input("Full Name")
                age = st.number_input("Age", min_value=1, max_value=100)
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            
            with col2:
                phone = st.text_input("Phone Number")
                email = st.text_input("Email Address")
                address = st.text_area("Address")
            
            # Ayurvedic specific fields
            st.subheader("Ayurvedic Profile")
            col3, col4 = st.columns(2)
            
            with col3:
                prakriti = st.selectbox("Prakriti (Body Constitution)", 
                                       ["Vata", "Pitta", "Kapha", "Vata-Pitta", "Pitta-Kapha", "Vata-Kapha", "Tridosha"])
                agni = st.selectbox("Agni (Digestive Fire)", 
                                   ["Sama", "Vishama", "Tikshna", "Manda"])
            
            with col4:
                vikriti = st.selectbox("Vikriti (Current Imbalance)", 
                                      ["Vata", "Pitta", "Kapha", "Vata-Pitta", "Pitta-Kapha", "Vata-Kapha", "Tridosha"])
                ama = st.selectbox("Ama (Toxins Presence)", 
                                  ["None", "Mild", "Moderate", "Severe"])
            
            # Submit button
            submitted = st.form_submit_button("Add Patient")
            
            if submitted:
                patient_data = {
                    "patient_id": patient_id,
                    "full_name": full_name,
                    "age": age,
                    "gender": gender,
                    "contact": {
                        "phone": phone,
                        "email": email,
                        "address": address
                    },
                    "ayurvedic_profile": {
                        "prakriti": prakriti,
                        "vikriti": vikriti,
                        "agni": agni,
                        "ama": ama
                    },
                    "registration_date": datetime.datetime.now()
                }
                
                # Save to Firestore
                try:
                    db.collection("patients").document(patient_id).set(patient_data)
                    st.success("Patient added successfully!")
                except Exception as e:
                    st.error(f"Error adding patient: {e}")
    
    with tab2:
        st.subheader("Patient List")
        
        # Search functionality
        search_term = st.text_input("Search patients by name or ID")
        
        # Sample patient data - in real app, this would come from Firestore
        patients = [
            {"id": "PT001", "name": "Rahul Sharma", "age": 42, "therapy": "Panchakarma", "progress": 65},
            {"id": "PT002", "name": "Priya Patel", "age": 35, "therapy": "Abhyanga", "progress": 40},
            {"id": "PT003", "name": "Amit Kumar", "age": 50, "therapy": "Basti", "progress": 80},
            {"id": "PT004", "name": "Sunita Devi", "age": 28, "therapy": "Shirodhara", "progress": 25},
        ]
        
        # Filter patients based on search term
        if search_term:
            filtered_patients = [p for p in patients if search_term.lower() in p["name"].lower() or search_term.lower() in p["id"].lower()]
        else:
            filtered_patients = patients
        
        # Display patients
        for patient in filtered_patients:
            with st.expander(f"{patient['id']} - {patient['name']} ({patient['age']} years)"):
                col1, col2, col3 = st.columns([2, 1, 2])
                
                with col1:
                    st.write(f"**Therapy:** {patient['therapy']}")
                    st.write(f"**Progress:** {patient['progress']}%")
                
                with col2:
                    st.progress(patient['progress'] / 100)
                
                with col3:
                    if st.button("View Details", key=f"view_{patient['id']}"):
                        st.session_state.patient_data = patient
                        st.session_state.current_page = "Patient Details"
                    if st.button("Schedule Therapy", key=f"schedule_{patient['id']}"):
                        st.session_state.patient_data = patient
                        st.session_state.current_page = "Therapy Scheduling"

# Therapy Scheduling Page
elif st.session_state.current_page == "Therapy Scheduling":
    st.markdown("<h2 class='sub-header'>Therapy Scheduling</h2>", unsafe_allow_html=True)
    
    # Patient selection
    patient_options = ["PT001 - Rahul Sharma", "PT002 - Priya Patel", "PT003 - Amit Kumar", "PT004 - Sunita Devi"]
    selected_patient = st.selectbox("Select Patient", options=patient_options)
    
    if selected_patient:
        patient_id = selected_patient.split(" - ")[0]
        
        # Therapy selection
        therapy_options = ["Abhyanga", "Shirodhara", "Basti", "Nasya", "Raktamokshana", "Full Panchakarma"]
        selected_therapy = st.selectbox("Select Therapy", options=therapy_options)
        
        # Schedule details
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input("Start Date", value=datetime.date.today())
            duration = st.number_input("Duration (days)", min_value=1, max_value=90, value=14)
        
        with col2:
            frequency = st.selectbox("Frequency", options=["Daily", "Alternate Days", "Weekly", "Custom"])
            therapist = st.selectbox("Assign Therapist", options=["Dr. Sharma", "Dr. Patel", "Dr. Kumar", "Dr. Devi"])
        
        # Pre and post procedure instructions
        st.subheader("Procedure Instructions")
        
        pre_instructions = st.text_area("Pre-Procedure Instructions", 
                                       "Avoid heavy meals 2 hours before therapy. Wear comfortable clothing.")
        
        post_instructions = st.text_area("Post-Procedure Instructions", 
                                        "Rest for at least 1 hour after therapy. Avoid cold drinks and food.")
        
        # Schedule button
        if st.button("Schedule Therapy"):
            # Generate therapy schedule
            schedule = []
            current_date = start_date
            
            for day in range(duration):
                if frequency == "Daily" or (frequency == "Alternate Days" and day % 2 == 0) or frequency == "Weekly" and day % 7 == 0:
                    schedule.append({
                        "date": current_date,
                        "therapy": selected_therapy,
                        "therapist": therapist,
                        "status": "Scheduled"
                    })
                
                current_date += timedelta(days=1)
            
            # Save to session state and Firestore
            therapy_data = {
                "patient_id": patient_id,
                "patient_name": selected_patient.split(" - ")[1],
                "therapy": selected_therapy,
                "start_date": start_date,
                "duration": duration,
                "frequency": frequency,
                "therapist": therapist,
                "pre_instructions": pre_instructions,
                "post_instructions": post_instructions,
                "schedule": schedule,
                "created_at": datetime.datetime.now()
            }
            
            if save_therapy_schedule(patient_id, therapy_data):
                st.success("Therapy scheduled successfully!")
                
                # Send initial notification
                message = f"Your {selected_therapy} therapy has been scheduled starting from {start_date}. Please follow pre-procedure instructions: {pre_instructions}"
                send_notification(patient_id, "therapy_scheduled", message)
            
            st.session_state.therapy_schedule = therapy_data

# Progress Tracking Page
elif st.session_state.current_page == "Progress Tracking":
    st.markdown("<h2 class='sub-header'>Progress Tracking</h2>", unsafe_allow_html=True)
    
    # Patient selection
    patient_options = ["PT001 - Rahul Sharma", "PT002 - Priya Patel", "PT003 - Amit Kumar", "PT004 - Sunita Devi"]
    selected_patient = st.selectbox("Select Patient", options=patient_options, key="progress_patient")
    
    if selected_patient:
        patient_id = selected_patient.split(" - ")[0]
        
        # Get therapy progress (in real app, this would come from Firestore)
        progress_data = {
            "PT001": {"completed": 12, "total": 15, "symptoms": ["Improved digestion", "Better sleep", "Reduced joint pain"]},
            "PT002": {"completed": 5, "total": 10, "symptoms": ["Reduced stress", "Improved skin texture"]},
            "PT003": {"completed": 8, "total": 8, "symptoms": ["Significant pain relief", "Improved mobility"]},
            "PT004": {"completed": 3, "total": 7, "symptoms": ["Reduced headaches", "Better concentration"]}
        }
        
        if patient_id in progress_data:
            data = progress_data[patient_id]
            progress_percent = (data["completed"] / data["total"]) * 100
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Sessions Completed", f"{data['completed']}/{data['total']}")
                st.progress(progress_percent / 100)
            
            with col2:
                st.write("**Reported Improvements:**")
                for symptom in data["symptoms"]:
                    st.write(f"✓ {symptom}")
            
            # Progress visualization
            st.subheader("Progress Over Time")
            
            # Sample data for chart
            progress_days = list(range(1, data["total"] + 1))
            progress_values = [10, 20, 35, 30, 45, 60, 55, 70, 65, 75, 80, 85, 90, 95, 100][:data["total"]]
            
            chart_data = {
                "Day": progress_days,
                "Wellness Score": progress_values[:len(progress_days)]
            }
            
            st.line_chart(chart_data, x="Day", y="Wellness Score")
            
            # Patient feedback
            st.subheader("Patient Feedback")
            feedback = st.text_area("Enter feedback after today's session")
            
            if st.button("Submit Feedback"):
                if feedback:
                    # Save feedback to Firestore
                    try:
                        feedback_data = {
                            "patient_id": patient_id,
                            "feedback": feedback,
                            "date": datetime.datetime.now(),
                            "wellness_score": progress_values[data["completed"] - 1] if data["completed"] > 0 else 0
                        }
                        db.collection("patient_feedback").add(feedback_data)
                        st.success("Feedback submitted successfully!")
                    except Exception as e:
                        st.error(f"Error submitting feedback: {e}")
                else:
                    st.warning("Please enter feedback before submitting.")

# Notifications Page
elif st.session_state.current_page == "Notifications":
    st.markdown("<h2 class='sub-header'>Notification System</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Send Notification", "Notification Templates", "Notification History"])
    
    with tab1:
        st.subheader("Send New Notification")
        
        # Patient selection
        patient_options = ["PT001 - Rahul Sharma", "PT002 - Priya Patel", "PT003 - Amit Kumar", "PT004 - Sunita Devi"]
        selected_patient = st.selectbox("Select Patient", options=patient_options, key="notify_patient")
        
        if selected_patient:
            patient_id = selected_patient.split(" - ")[0]
            
            # Notification type
            notification_type = st.selectbox("Notification Type", 
                                           ["Pre-Procedure", "Post-Procedure", "Appointment Reminder", "General Message"])
            
            # Message content
            message = st.text_area("Message Content", height=100)
            
            # Delivery options
            st.subheader("Delivery Options")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                send_email = st.checkbox("Email", value=True)
            with col2:
                send_sms = st.checkbox("SMS", value=True)
            with col3:
                send_app = st.checkbox("In-App", value=True)
            
            # Schedule option
            schedule_later = st.checkbox("Schedule for later")
            
            if schedule_later:
                send_time = st.time_input("Schedule time")
                send_date = st.date_input("Schedule date", value=datetime.date.today())
            else:
                send_time = datetime.datetime.now().time()
                send_date = datetime.date.today()
            
            # Send button
            if st.button("Send Notification"):
                if message:
                    # Send notification
                    if send_notification(patient_id, notification_type, message):
                        st.success("Notification sent successfully!")
                else:
                    st.warning("Please enter a message before sending.")
    
    with tab2:
        st.subheader("Notification Templates")
        
        template_options = {
            "Pre-Procedure": "Reminder: Your therapy session is scheduled for {date} at {time}. Please follow these pre-procedure instructions: {instructions}",
            "Post-Procedure": "Hope your therapy session went well. Please remember to follow these post-procedure instructions: {instructions}",
            "Appointment Reminder": "Reminder: You have an appointment for {therapy} tomorrow at {time} with {therapist}.",
            "General Message": "Message from AyurSutra: {message}"
        }
        
        selected_template = st.selectbox("Select Template", options=list(template_options.keys()))
        
        if selected_template:
            st.text_area("Template Content", value=template_options[selected_template], height=100)
            
            if st.button("Use Template"):
                st.session_state.notification_message = template_options[selected_template]
                st.experimental_rerun()

# AyurBuddy Assistant Page
elif st.session_state.current_page == "AyurBuddy Assistant":
    st.markdown("<h2 class='sub-header'>AyurBuddy Assistant</h2>", unsafe_allow_html=True)
    
    st.write("Ask me anything about Panchakarma therapies, patient care, or Ayurvedic principles.")
    
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
                log_conversation(user_query, "ayurvedic_query", response)
        
        # Clear uploaded file after processing
        if uploaded_file:
            uploaded_file = None

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #6B8E23;'>AyurSutra - Panchakarma Patient Management System</div>", unsafe_allow_html=True)