from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO
from config import openai_instance as openai
import tempfile
import os
from playsound import playsound

def talker(message):
    # Use a system temp directory
    temp_dir = tempfile.gettempdir()  # Gets OS-defined temp folder
    print('temp_dir:', temp_dir)

    response = openai.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=message
    )

    audio_stream = BytesIO(response.content)
    audio = AudioSegment.from_file(audio_stream, format="mp3")

    # Generate a temporary file in the temp directory
    temp_audio_file = os.path.join(temp_dir, "temp_audio.wav")
    with open(temp_audio_file, 'wb') as f:
        audio.export(f, format="wav")  # Explicitly export to wav format

    # Play the audio from the temporary file using playsound
    playsound(temp_audio_file)

    # Optionally, delete the temporary file after playing
    os.remove(temp_audio_file)

# talker("Hello, I am a chatbot. How can I help you today?")
