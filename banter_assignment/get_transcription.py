import logging
from banter_assignment.get_audio import text_to_speech_stream
from banter_assignment.rag_memory import chat_with_memory
from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone,
)
import base64

# Set up client configuration
config = DeepgramClientOptions(
    verbose=logging.DEBUG,
    options={"keepalive": "true"}
)

# Initialize Deepgram client and connection
deepgram = DeepgramClient("", config)
dg_connection = deepgram.listen.live.v("1")

def configure_deepgram():
    options = LiveOptions(
        smart_format=True,
        language="en-US",
        encoding="linear16",
        channels=1,
        sample_rate=16000,
    )
    dg_connection.start(options)

def start_microphone():
    microphone = Microphone(dg_connection.send)
    microphone.start()
    return microphone

def steve_intro(socketio):
    try:
        response = "Greetings, my dear friend! Emphasis on 'friend' because I don't just talk to any random person. Tell me what you want to discuss, but make it quick."

        # Generate audio data from the transcription
        audio_data_bytes = text_to_speech_stream(response)
        # Convert audio data to base64 string
        audio_data = base64.b64encode(audio_data_bytes).decode('utf-8')

        # Emit the audio data
        socketio.emit('audio_update', {'audio': audio_data})
    
    except Exception as e:
        logging.error(f"Error: {e}")

def start_transcription_loop(transcribing, transcription_event , socketio):
    try:
        all_transcriptions = ""

        while transcribing:
            configure_deepgram()

            # Open a microphone stream
            microphone = start_microphone()

            def on_message(self, result, **kwargs):
                # nonlocal all_transcriptions
                transcript = result.channel.alternatives[0].transcript
                if len(transcript) > 0:
                        socketio.emit('transcription_update', {'transcription': transcribing.strip()})

                        response = chat_with_memory(transcribing.strip())
                        print(response)

                        # Generate audio data from the transcription
                        audio_data_bytes = text_to_speech_stream(response)
                        # Convert audio data to base64 string
                        audio_data = base64.b64encode(audio_data_bytes).decode('utf-8')

                        # Emit the audio data
                        socketio.emit('audio_update', {'audio': audio_data})    

                        # # Clear the transcription string after emitting
                        # all_transcriptions = ""

            dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

            # Wait for the transcription to finish
            transcription_event.wait()
            transcription_event.clear()

            # Finish the microphone and Deepgram connection
            microphone.finish()
            dg_connection.finish()
            logging.info("Transcription loop finished.")

            # Emit the entire transcription
            # if all_transcriptions.strip():  # Check if there's any content
            #     socketio.emit('transcription_update', {'transcription': all_transcriptions.strip()})

            #     response = chat_with_memory(all_transcriptions.strip())
            #     print(response)

            #     # Generate audio data from the transcription
            #     audio_data_bytes = text_to_speech_stream(response)
            #     # Convert audio data to base64 string
            #     audio_data = base64.b64encode(audio_data_bytes).decode('utf-8')

            #     # Emit the audio data
            #     socketio.emit('audio_update', {'audio': audio_data})    

            #     # Clear the transcription string after emitting
            #     all_transcriptions = ""

                
    except Exception as e:
        logging.error(f"Error: {e}")

def reconnect():
    try:
        logging.info("Reconnecting to Deepgram...")
        new_dg_connection = deepgram.listen.live.v("1")

        # Configure and start the new Deepgram connection
        configure_deepgram(new_dg_connection)

        logging.info("Reconnected to Deepgram successfully.")
        return new_dg_connection

    except Exception as e:
        logging.error(f"Reconnection failed: {e}")
        return None

def on_disconnect():
    logging.info("Client disconnected")
    global dg_connection
    if dg_connection:
        dg_connection.finish()
        dg_connection = None
        logging.info("Cleared listeners and set dg_connection to None")
    else:
        logging.info("No active dg_connection to disconnect from")