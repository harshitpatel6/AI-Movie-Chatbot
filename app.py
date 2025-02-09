import streamlit as st
import requests
import pyttsx3
import speech_recognition as sr
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

# Initialize TTS Engine
tts_engine = pyttsx3.init()

# Streamlit Page Config
st.set_page_config(page_title="🎬 AI Movie Chatbot", page_icon="🎥", layout="centered")

# Custom CSS for UI Styling
st.markdown("""
    <style>
        .stApp {
            background-color: #1e1e1e;
            color: white;
        }
        .title {
            font-size: 2.5em;
            font-weight: bold;
            text-align: center;
            color: #f4c542;
        }
        .subtitle {
            font-size: 1.2em;
            text-align: center;
            color: #d4d4d4;
        }
        .button-container {
            text-align: center;
            margin-top: 20px;
        }
        .movie-container {
            background-color: #333;
            padding: 15px;
            border-radius: 10px;
        }
        .movie-title {
            font-size: 1.5em;
            font-weight: bold;
            color: #f4c542;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="title">🎬 AI Movie Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">🎤 Speak a movie name and get instant details!</div>', unsafe_allow_html=True)

# Function to get movie details from OMDb API
def get_movie_info(movie_name):
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}"
    response = requests.get(url).json()
    return response if response.get("Response") == "True" else None

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

# Function for Text-to-Speech
def text_to_speech(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

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
        st.markdown(f"""
            <div class="movie-container">
                <div class="movie-title">{movie_info['Title']} ({movie_info['Year']})</div>
                <p>🎭 **Genre:** {movie_info['Genre']}</p>
                <p>🎬 **Director:** {movie_info['Director']}</p>
                <p>⭐ **IMDB Rating:** {movie_info['imdbRating']}</p>
                <p>📜 **Plot:** {movie_info['Plot']}</p>
                <p>🎭 **Actors:** {movie_info['Actors']}</p>
            </div>
        """, unsafe_allow_html=True)

        # Show Movie Poster
        st.image(movie_info["Poster"], caption=movie_info["Title"], width=300)

        # Text-to-Speech for Response
        response_text = f"{movie_info['Title']} is a {movie_info['Genre']} movie released in {movie_info['Year']}. Directed by {movie_info['Director']}. IMDB rating: {movie_info['imdbRating']}. Plot: {movie_info['Plot']}"
        text_to_speech(response_text)

        # Chatbot Response
        st.chat_message("assistant").markdown(f"✅ **Movie Found!** \n\n{response_text}")

    else:
        st.chat_message("assistant").markdown("❌ **Movie not found in OMDb database.** Try another one!")
