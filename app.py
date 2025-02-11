import streamlit as st
import requests
import pyttsx3
import speech_recognition as sr
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY", "write API key here")  # Defaulting to provided API key

# Streamlit Page Config
st.set_page_config(page_title="🎬 AI Movie Chatbot", page_icon="🎥", layout="centered")

# Function to get movie details from OMDb API
def get_movie_info(movie_name):
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}"
    response = requests.get(url).json()
    return response if response.get("Response") == "True" else None

# Function to convert text to speech
def text_to_speech(text):
    """Fixes threading issues by initializing a new engine every time."""
    tts_engine = pyttsx3.init()
    tts_engine.say(text)
    tts_engine.runAndWait()
    tts_engine.stop()

# Function to recognize speech
def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            st.success(f"✅ You said: {text}")
            return text
        except sr.UnknownValueError:
            st.error("❌ Sorry, I couldn't understand. Try again!")
        except sr.RequestError:
            st.error("❌ Speech service unavailable.")
        return None

# UI Components
st.title("🎬 AI Movie Chatbot")
st.write("🎤 Speak a movie name and get instant details!")

# Voice Input Button
if st.button("🎤 Tap to Speak", key="voice_button"):
    movie_name = voice_input()
else:
    movie_name = None

# Process the movie search
if movie_name:
    st.chat_message("user").markdown(f"🎥 **You asked:** {movie_name}")

    movie_info = get_movie_info(movie_name)

    if movie_info:
        # Display Movie Details
        st.subheader(f"{movie_info['Title']} ({movie_info['Year']})")
        st.write(f"🎭 **Genre:** {movie_info['Genre']}")
        st.write(f"🎬 **Director:** {movie_info['Director']}")
        st.write(f"⭐ **IMDB Rating:** {movie_info['imdbRating']}")
        st.write(f"📜 **Plot:** {movie_info['Plot']}")
        st.write(f"🎭 **Actors:** {movie_info['Actors']}")
        
        # Show Movie Poster
        st.image(movie_info["Poster"], caption=movie_info["Title"], width=300)

        # Text-to-Speech for Response
        response_text = f"{movie_info['Title']} is a {movie_info['Genre']} movie released in {movie_info['Year']}. Directed by {movie_info['Director']}. IMDB rating: {movie_info['imdbRating']}. Plot: {movie_info['Plot']}"
        text_to_speech(response_text)

        # Chatbot Response
        st.chat_message("assistant").markdown(f"✅ **Movie Found!** \n\n{response_text}")

    else:
        st.chat_message("assistant").markdown("❌ **Movie not found in OMDb database.** Try another one!")
