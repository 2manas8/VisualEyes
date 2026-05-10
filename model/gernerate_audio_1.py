import pyttsx3
import time

# Initialize TTS engine
engine = pyttsx3.init()

# Voice settings
engine.setProperty("rate", 150)
engine.setProperty("volume", 1.0)

# Store last spoken message
last_message = ""
last_time = 0

# Prevent repeating too fast
COOLDOWN = 2


def speak(message):

    global last_message
    global last_time

    current_time = time.time()

    # Avoid repeating same message quickly
    if (
        message == last_message
        and current_time - last_time < COOLDOWN
    ):
        return

    print(f"Speaking: {message}")

    engine.say(message)
    engine.runAndWait()

    last_message = message
    last_time = current_time