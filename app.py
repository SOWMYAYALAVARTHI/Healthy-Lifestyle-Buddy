import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Page setup
st.set_page_config(page_title="FitFusion AI", page_icon="🥗🏋️🌿", layout="centered")
st.title("🥗 FitFusion AI 🏋️🌿")
st.subheader(" Meal, Fitness & Wellness Chatbot")

# Welcome screen if no category is chosen yet
if "category" not in st.session_state:
    st.markdown("### 👋 Welcome to FitFusion - Your Healthy Lifestyle Buddy!")
    st.markdown("I'm your all-in-one assistant for:")
    st.markdown("- 🥗 Healthy Meals\n- 🏋️ Quick Workouts\n- 🧘 Mindfulness Tips")
    st.markdown("Choose what you'd like to start with:")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🍽️ Meals"):
         st.session_state.category = "Quick Healthy Meal"
         st.rerun()
    with col2:
        if st.button("💪 Workouts"):
         st.session_state.category = "Short Workout Plan"
         st.rerun()
    with col3:
        if st.button("🧘 Wellness"):
            st.session_state.category = "Wellness & Mindfulness Tip"
            st.rerun()
        
    st.stop()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    if st.session_state.category == "Quick Healthy Meal":
        system_instruction = "You are a helpful nutritionist that provides fast, healthy meal suggestions."
    elif st.session_state.category == "Short Workout Plan":
        system_instruction = "You are a fitness expert giving quick, goal-based workouts."
    else:
        system_instruction = "You are a calming wellness expert sharing mindfulness and stress relief tips."
    st.session_state.messages.append({"role": "user", "parts": [system_instruction]})

# Show previous messages
for msg in st.session_state.messages[1:]:  # skip system instruction
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["parts"][0])
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["parts"][0])

# 🔁 Reset button
if st.button("🔄 Reset Chat"):
    del st.session_state.messages
    del st.session_state.category
    st.rerun()

# Text input at the bottom (like a real chat!)
user_input = st.chat_input("Type your question here...")

if user_input:
    st.session_state.messages.append({"role": "user", "parts": [user_input]})

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        chat = model.start_chat(history=st.session_state.messages)
        response = chat.send_message(user_input)
        st.session_state.messages.append({"role": "model", "parts": [response.text]})
        st.rerun()

    except Exception as e:
        st.error(f"Something went wrong: {e}")
