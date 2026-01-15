import sounddevice as sd
import numpy as np
import queue
import sys
from stt_engine import STTEngine
from llm_engine import LLMEngine
from tts_engine import TTSEngine

# Configuration
SAMPLE_RATE = 16000
CHANNELS = 1
VAD_THRESHOLD = 0.01  # Simple amplitude threshold
SILENCE_DURATION = 2.0  # Seconds of silence before processing

class AssistantOrchestrator:
    def __init__(self):
        print("Initializing engines...")
        self.stt = STTEngine()
        self.llm = LLMEngine()
        self.tts = TTSEngine()
        self.audio_queue = queue.Queue()
        print("Assistant ready.")

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        self.audio_queue.put(indata.copy())

    def run(self):
        print("Listening... (Press Ctrl+C to stop)")
        with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=self.audio_callback):
            while True:
                audio_buffer = []
                silent_chunks = 0
                max_silent_chunks = int(SILENCE_DURATION * (SAMPLE_RATE / 1024)) # Approximate
                
                # Wait for speech
                recording = False
                while True:
                    data = self.audio_queue.get()
                    amplitude = np.max(np.abs(data))
                    
                    if amplitude > VAD_THRESHOLD:
                        recording = True
                        silent_chunks = 0
                    
                    if recording:
                        audio_buffer.append(data)
                        if amplitude < VAD_THRESHOLD:
                            silent_chunks += 1
                        else:
                            silent_chunks = 0
                            
                        if silent_chunks > max_silent_chunks:
                            break
                            
                # Process Speech
                print("Processing...")
                audio_data = np.concatenate(audio_buffer, axis=0).flatten()
                text = self.stt.transcribe(audio_data)
                
                if text:
                    print(f"You: {text}")
                    response = self.llm.generate(text)
                    print(f"Assistant: {response}")
                    self.tts.speak(response)
                
                print("Listening again...")

if __name__ == "__main__":
    assistant = AssistantOrchestrator()
    try:
        assistant.run()
    except KeyboardInterrupt:
        print("\nStopping assistant.")
