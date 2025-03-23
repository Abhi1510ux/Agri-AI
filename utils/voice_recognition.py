import speech_recognition as sr
import streamlit as st

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎤 Say the name of the pest or the issue with your crop...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        st.write(f"🗣️ You said: {text}")
        return text
    except sr.UnknownValueError:
        st.write("⚠️ Could not understand the audio.")
    except sr.RequestError as e:
        st.write(f"⚠️ Error with speech recognition: {e}")
