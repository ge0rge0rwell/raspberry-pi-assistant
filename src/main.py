import sounddevice as sd
import numpy as np
import queue
import sys
import asyncio
import uvicorn
from stt_engine import STTEngine
from llm_engine import LLMEngine
from tts_engine import TTSEngine
from api import app, broadcast_event

# Configuration
SAMPLE_RATE = 16000
CHANNELS = 1
VAD_THRESHOLD = 0.01  # Simple amplitude threshold
SILENCE_DURATION = 1.5  # Seconds of silence before processing

class AssistantOrchestrator:
    def __init__(self):
        print("Initializing engines...")
        self.stt = STTEngine()
        self.llm = LLMEngine()
        self.tts = TTSEngine()
        self.audio_queue = queue.Queue()
        self.loop = asyncio.get_event_loop()
        print("Assistant ready.")

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        self.audio_queue.put(indata.copy())

    async def run_assistant(self):
        print("Listening... (Press Ctrl+C to stop)")
        with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=self.audio_callback):
            while True:
                audio_buffer = []
                silent_chunks = 0
                max_silent_chunks = int(SILENCE_DURATION * (SAMPLE_RATE / 1024))
                
                # Wait for speech
                recording = False
                while True:
                    await asyncio.sleep(0.01)
                    try:
                        data = self.audio_queue.get_nowait()
                        amplitude = np.max(np.abs(data))
                        
                        if amplitude > VAD_THRESHOLD:
                            if not recording:
                                await broadcast_event("state", {"status": "listening", "amplitude": float(amplitude)})
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
                    except queue.Empty:
                        continue
                            
                # Process Speech
                await broadcast_event("state", {"status": "processing"})
                audio_data = np.concatenate(audio_buffer, axis=0).flatten()
                text = self.stt.transcribe(audio_data)
                
                if text:
                    await broadcast_event("transcript", {"text": text, "role": "user"})
                    print(f"You: {text}")
                    
                    response = self.llm.generate(text)
                    await broadcast_event("transcript", {"text": response, "role": "assistant"})
                    print(f"Assistant: {response}")
                    
                    await broadcast_event("state", {"status": "speaking"})
                    self.tts.speak(response)
                
                await broadcast_event("state", {"status": "idle"})
                print("Listening again...")

async def main():
    orchestrator = AssistantOrchestrator()
    
    # Run FastAPI server and Assistant concurrently
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    
    await asyncio.gather(
        server.serve(),
        orchestrator.run_assistant()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopping assistant.")
