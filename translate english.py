import speech_recognition as sr
import tkinter as tk
from gtts import gTTS
import pygame
from io import BytesIO
import openai
import tempfile
import threading
import pygame.mixer

from tkinter import ttk

#Author：Haohua Zheng

openai.api_key = "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"

pygame.mixer.init(buffer=512)

def record_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("请说话...")
        audio = recognizer.listen(source)
        print("录音结束。")

    try:
        text = recognizer.recognize_google(audio, language='zh-CN')
        print(f"您说的是: {text}")
        return text
    except Exception as e:
        print("抱歉，我没听清楚。")
        return None

def record_audio_en():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please speak...")
        audio = recognizer.listen(source)
        print("Done")

    try:
        text = recognizer.recognize_google(audio, language='en')
        print(f"You: {text}")
        return text
    except Exception as e:
        print("Sorry, I can't hear clearly")
        return None

def ask_gpt(text):
    response = openai.Completion.create(
        engine="text-davinci-003", 
        prompt="请有礼貌和有意识将双引号里的中文翻译成英文并且回答中不要出现任何中文“" + text + "”", 
        max_tokens=200, 
        n=1, 
        stop=None, 
        temperature=0.8
    )

    return response.choices[0].text.strip()

def ask_gpt_en(text):
    response = openai.Completion.create(
        engine="text-davinci-003", 
        prompt="Please politely and consciously translate the English in the double quotation marks into Chinese, and make sure that there is no English in the answer “" + text + "”", 
        max_tokens=200, 
        n=1, 
        stop=None, 
        temperature=0.8
    )

    return response.choices[0].text.strip()

def on_start_click(event):
    pygame.mixer.music.stop()
    window.unbind('<ButtonPress-1>')
    window.bind('<ButtonRelease-1>', on_stop_click)
    text = record_audio()
    if text:
        response = ask_gpt(text)
        print(f"GPT: {response}")
        tts = gTTS(response, lang='en')
        tts.save("response.mp3")

def on_start_click_en(event):
    pygame.mixer.music.stop()
    window.unbind('<ButtonPress-1>')
    window.bind('<ButtonRelease-1>', on_stop_click)
    text = record_audio_en()
    if text:
        response = ask_gpt_en(text)
        print(f"GPT: {response}")
        tts = gTTS(response, lang='zh-CN')
        tts.save("response.mp3")

def play_response(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

def on_stop_click(event):
    pygame.mixer.music.stop()
    play_thread = threading.Thread(target=play_response, args=("response.mp3",))
    play_thread.start()
    window.unbind('<ButtonRelease-1>')

def on_interrupt_click():
    pygame.mixer.music.stop()

window = tk.Tk()
window.geometry("400x200")
window.title("语音问答")

mic_button = tk.Canvas(window, width=100, height=100)
mic_button.pack(side=tk.LEFT, padx=10, pady=10)
mic_button.create_oval(10, 10, 90, 90, fill='red')
mic_button.create_text(50, 50, text="中文 -> 英文", fill='white', font=("Helvetica", 12))
mic_button.bind('<ButtonPress-1>', on_start_click)

mic_button_en = tk.Canvas(window, width=100, height=100)
mic_button_en.pack(side=tk.LEFT, padx=10, pady=10)
mic_button_en.create_oval(10, 10, 90, 90, fill='blue')
mic_button_en.create_text(50, 50, text="English\n-> Chinese", fill='white', font=("Helvetica", 12))
mic_button_en.bind('<ButtonPress-1>', on_start_click_en)

interrupt_button = tk.Button(window, text="Stop Play", command=on_interrupt_click)
interrupt_button.pack(pady=10)

window.mainloop()
