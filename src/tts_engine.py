import subprocess
import os

class TTSEngine:
    def __init__(self, model_path="/home/pi/piper_models/en_US-lessac-medium.onnx"):
        self.model_path = model_path
        self.piper_exe = "/usr/bin/piper" # Assumed path after installation

    def speak(self, text):
        if not text:
            return
            
        # Piper produces raw audio or WAV. We pipe it to an audio player.
        # Using 'aplay' for RPi generic audio output.
        try:
            command = [
                self.piper_exe,
                "--model", self.model_path,
                "--output-raw"
            ]
            piper_process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEV_PIPE
            )
            
            # Pipe Piper's raw output to aplay
            aplay_process = subprocess.Popen(
                ["aplay", "-r", "22050", "-f", "S16_LE", "-t", "raw"],
                stdin=piper_process.stdout
            )
            
            piper_process.stdin.write(text.encode("utf-8"))
            piper_process.stdin.close()
            aplay_process.wait()
            
        except Exception as e:
            print(f"TTS Error: {e}")
