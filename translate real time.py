import tkinter as tk
import pyaudio
import threading
import numpy as np
from deepspeech import Model

# Load models
ds_en = Model("deepspeech-0.9.3-models.pbmm")
ds_zh = Model("deepspeech-0.9.3-models-zh-CN.pbmm")

# Initialize
is_recording = False
audio_source = None
sample_rate = 16000
buffer_size = 1024

def record_stream():
    global is_recording
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=sample_rate,
        input=True,
        frames_per_buffer=buffer_size,
    )

    while is_recording:
        buffer = stream.read(buffer_size)
        data16 = np.frombuffer(buffer, dtype=np.int16)
        text_en = ds_en.stt(data16)
        text_zh = ds_zh.stt(data16)

        if len(text_en) > 0 and len(text_zh) > 0:
            print("English: ", text_en)
            print("Chinese: ", text_zh)

    stream.stop_stream()
    stream.close()
    p.terminate()

def toggle_recording():
    global is_recording

    if not is_recording:
        is_recording = True
        button.config(text="Stop Recording")
        threading.Thread(target=record_stream).start()
    else:
        is_recording = False
        button.config(text="Start Recording")

# Create window
window = tk.Tk()
window.title("Voice Recorder")
window.geometry("300x200")

# Create button
button = tk.Button(window, text="Start Recording", command=toggle_recording)
button.pack(expand=True, fill="both")

# Start main loop
window.mainloop()

