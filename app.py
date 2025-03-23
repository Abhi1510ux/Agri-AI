import streamlit as st
import google.generativeai as genai
import os
import requests
from dotenv import load_dotenv
import random
import cv2
import numpy as np
import streamlit as st
from PIL import Image
# Load API key from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_GEMINI_API_KEY")

# OpenWeather API Key (Replace with your own)
WEATHER_API_KEY = "334897a1e8a2b8c5a10831e6b6740675"  # 🔴 Replace with actual API key

# Check if AI API key exists
if not api_key:
    st.error("⚠️ Google Gemini API Key is missing. Set it in a `.env` file.")
else:
    genai.configure(api_key=api_key)

# Streamlit UI
st.set_page_config(page_title="🌾 AI-Driven Agricultural Advisory", layout="wide")
st.sidebar.title("📌 Navigation")

# ✅ Define Main Content Area
main_container = st.empty()

# ✅ AI Chatbot Function
def chatbot_ui():
    with main_container.container():
        st.subheader("🤖 AI Farming Chatbot")
        st.write("Ask me any farming-related questions!")

        user_query = st.text_input("💬 Enter your query:")

        # Answer Type Selection
        answer_type = st.radio("Choose answer type:", ["🌿 Simple Advice", "📜 Detailed Explanation"])

        if st.button("🚀 Ask AI"):
            if user_query.strip():
                try:
                    # AI Model with system instruction
                    model = genai.GenerativeModel("gemini-1.5-pro-latest", 
                                                  system_instruction="Provide precise, farmer-friendly advice. Use simple language and avoid unnecessary details.")

                    # Modify query based on answer type
                    if answer_type == "🌿 Simple Advice":
                        user_query = f"Give a short and clear answer in simple words. Provide only key points for: {user_query}"
                    else:
                        user_query = f"Give a detailed and expert-level response for: {user_query}"

                    # AI Response with word limit
                    response = model.generate_content(user_query, generation_config={"max_output_tokens": 150})
                    
                    st.success(f"🤖 AI Chatbot: {response.text}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("⚠️ Please enter a question!")

# ✅ Fetch Weather Data
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_info = {
            "Temperature": data["main"]["temp"],
            "Humidity": data["main"]["humidity"],
            "Condition": data["weather"][0]["description"].title()
        }
        return weather_info
    else:
        return None

# ✅ Weather Information Function
def weather_ui():
    with main_container.container():
        st.subheader("🌦️ Weather Information")
        city = st.text_input("🏙️ Enter your city:", "New Delhi")
        
        if st.button("🔍 Get Weather"):
            weather_data = get_weather(city)
            if weather_data:
                st.success(f"🌡️ Temperature: {weather_data['Temperature']}°C")
                st.success(f"💧 Humidity: {weather_data['Humidity']}%")
                st.success(f"🌤️ Condition: {weather_data['Condition']}")
            else:
                st.error("❌ Failed to fetch weather data. Check city name or API key.")

# ✅ Crop Prediction Based on Weather
def crop_advisory_ui():
    with main_container.container():
        st.subheader("🌱 Crop Advisory")
        city = st.text_input("🏙️ Enter your location for crop suggestions:", "New Delhi")

        if st.button("🌾 Get Crop Advice"):
            weather_data = get_weather(city)
            if weather_data:
                temperature = weather_data["Temperature"]

                # Simple crop prediction logic
                if temperature < 15:
                    crop_suggestion = "Wheat, Barley, Mustard"
                elif 15 <= temperature < 25:
                    crop_suggestion = "Rice, Maize, Sunflower"
                else:
                    crop_suggestion = "Sugarcane, Cotton, Millet"

                st.success(f"🌱 Recommended Crops: {crop_suggestion}")
                st.info(f"📌 Based on current temperature: {temperature}°C")
            else:
                st.error("❌ Failed to fetch weather data. Check city name or API key.")

# ✅ Pest Detection Function (Placeholder)
# ✅ Pest Information Database
pest_info = {
    "Aphids": {
        "description": "Aphids are tiny, sap-sucking insects that weaken plants by draining essential nutrients. They multiply rapidly and can cause leaf curling, yellowing, and stunted growth.",
        "causes": [
            "Overuse of nitrogen-rich fertilizers",
            "Warm, dry weather conditions",
            "Lack of natural predators like ladybugs"
        ],
        "remedies": {
            "Organic Solutions": [
                "Spray neem oil solution (5ml per liter of water) on affected areas",
                "Introduce natural predators like ladybugs and lacewings",
                "Use garlic or chili spray to repel aphids"
            ],
            "Chemical Treatments": [
                "Apply insecticidal soap (safe for plants and non-toxic to humans)",
                "Use systemic insecticides like Imidacloprid for severe infestations"
            ]
        },
        "prevention": [
            "Plant marigolds, basil, or chives to deter aphids naturally",
            "Avoid excessive use of nitrogen-based fertilizers",
            "Regularly inspect plants for early signs of infestation"
        ]
    },
    "Caterpillars": {
        "description": "Caterpillars are larvae of butterflies and moths that chew leaves, leading to defoliation and reduced crop yields.",
        "causes": [
            "Presence of butterfly and moth eggs on leaves",
            "Lack of natural predators such as birds or parasitic wasps",
            "Warm weather conditions favoring rapid growth"
        ],
        "remedies": {
            "Organic Solutions": [
                "Handpick caterpillars and destroy them",
                "Apply Bacillus thuringiensis (Bt) spray to affected crops",
                "Use neem oil to prevent caterpillar growth"
            ],
            "Chemical Treatments": [
                "Apply synthetic pyrethroids like Cypermethrin or Lambda-cyhalothrin",
                "Use Carbaryl-based insecticides for effective control"
            ]
        },
        "prevention": [
            "Use row covers to prevent moths from laying eggs",
            "Encourage birds and natural predators in your farm",
            "Rotate crops to disrupt caterpillar life cycle"
        ]
    },
    "Whiteflies": {
        "description": "Whiteflies are small, winged insects that suck plant sap, causing yellowing, leaf drop, and reduced crop yield. They also transmit viral diseases.",
        "causes": [
            "High humidity and warm temperatures favor their reproduction",
            "Dense plant spacing that allows easy spread",
            "Lack of natural predators like parasitic wasps"
        ],
        "remedies": {
            "Organic Solutions": [
                "Use yellow sticky traps to catch adult whiteflies",
                "Spray neem oil or insecticidal soap on infected plants",
                "Introduce natural predators like Encarsia formosa wasps"
            ],
            "Chemical Treatments": [
                "Apply Imidacloprid or Thiamethoxam for systemic control",
                "Use Pyrethroid-based insecticides for fast action"
            ]
        },
        "prevention": [
            "Regularly prune infected leaves and dispose of them",
            "Use reflective mulches to deter whiteflies",
            "Maintain proper plant spacing to improve airflow"
        ]
    },
    "Healthy Crop": {
        "description": "No pests detected. Your crop is healthy and does not require any immediate treatment.",
        "prevention": [
            "Regularly inspect crops to catch early signs of infestation",
            "Use companion planting to naturally repel pests",
            "Ensure proper irrigation and fertilization for healthy plant growth"
        ]
    }
}

# ✅ Pest Detection Function with Camera & Upload Option
def pest_detection_ui():
    st.subheader("🐛 Pest Detection")
    st.write("📌 Scan using your camera or upload an image to detect pests.")

    # Selection: Camera or Image Upload
    option = st.radio("Choose Input Method:", ["📷 Scan with Camera", "🖼️ Upload Image"])

    if option == "📷 Scan with Camera":
        # ✅ Use Camera for Live Capture
        img_file_buffer = st.camera_input("📸 Capture an Image")

        if img_file_buffer is not None:
            image = Image.open(img_file_buffer)
            st.image(image, caption="Scanned Image", use_column_width=True)

            # Dummy AI Pest Detection Logic (Replace with real model)
            detected_result = random.choice(list(pest_info.keys()))
            display_pest_info(detected_result)

    elif option == "🖼️ Upload Image":
        # ✅ Upload Image for Detection
        uploaded_image = st.file_uploader("📂 Upload an Image", type=["jpg", "png", "jpeg"])

        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_column_width=True)

            # Dummy AI Pest Detection Logic
            detected_result = random.choice(list(pest_info.keys()))
            display_pest_info(detected_result)


# ✅ Function to Display Pest Information
def display_pest_info(pest_name):
    pest_details = pest_info.get(pest_name, {})

    if pest_name == "Healthy Crop":
        st.success(f"✅ {pest_name}: {pest_details['description']} 🌿")
        st.subheader("🌱 Prevention Tips")
        for tip in pest_details["prevention"]:
            st.write(f"✔️ {tip}")
        return

    st.error(f"⚠️ Pest Detected: {pest_name}! Immediate action is required.")

    st.subheader("📖 Pest Description")
    st.write(pest_details["description"])

    st.subheader("🧐 Causes of Infestation")
    for cause in pest_details["causes"]:
        st.write(f"🔸 {cause}")

    st.subheader("💊 Treatment & Remedies")
    
    # ✅ Organic Solutions
    st.markdown("### 🌿 Organic Solutions")
    for remedy in pest_details["remedies"]["Organic Solutions"]:
        st.write(f"✅ {remedy}")

    # ✅ Chemical Treatments
    st.markdown("### 🧪 Chemical Treatments")
    for treatment in pest_details["remedies"]["Chemical Treatments"]:
        st.write(f"⚠️ {treatment}")

    # ✅ Preventive Measures
    st.subheader("🛡️ Prevention Tips")
    for tip in pest_details["prevention"]:
        st.write(f"✔️ {tip}")
# ✅ Sidebar Navigation
menu = st.sidebar.radio("Select a feature:", ["Home", "AI Chatbot", "Weather", "Crop Advisory", "Pest Detection"])

# ✅ Navigation Logic (Clears Content Before Rendering)
if menu == "AI Chatbot":
    chatbot_ui()
elif menu == "Weather":
    weather_ui()
elif menu == "Crop Advisory":
    crop_advisory_ui()
elif menu == "Pest Detection":
    pest_detection_ui()
else:
    with main_container.container():
        st.markdown("""
        ### Welcome to the AI-Driven Agricultural Advisory System! 🌾  
        Select a feature from the sidebar to get started. ✅
        """)

