
import os
import uuid
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

# print(ELEVENLABS_API_KEY)
client = ElevenLabs(
    api_key="79fce72f5b4c18697f2b814d722ed28b",
)


def text_to_speech_stream(text: str , voice_id : str = 'VR6AewLTigWG4xSOukaG') -> str:
    # Calling the text_to_speech conversion API with detailed parameters
    response = client.text_to_speech.convert(
        voice_id=voice_id, # Adam pre-made voice
        optimize_streaming_latency="0",
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2", # use the turbo model for low latency, for other languages use the `eleven_multilingual_v2`
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    # uncomment the line below to play the audio back
    # play(response)

    audio_data = b''
    for chunk in response:
        if chunk:
            audio_data += chunk

    # print(audio_data)
    return audio_data

def play(audio_data):
    # Play the audio data
    with open(f"audio_{uuid.uuid4()}.mp3", "wb") as f:
        f.write(audio_data)
    os.system(f"afplay audio_{uuid.uuid4()}.mp3")
    os.remove(f"audio_{uuid.uuid4()}.mp3")

if __name__ == '__main__':
    text = "Hello, how are you doing today?"
    audio_data = text_to_speech_stream(text)
    play(audio_data)
    print("Audio played successfully!")