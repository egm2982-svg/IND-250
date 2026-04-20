import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import asyncio
import edge_tts
import os
import time
from pypdf import PdfReader
from deep_translator import GoogleTranslator
from playsound import playsound

# -------------------------------
# GLOBAL STATE
# -------------------------------
current_file = None
audio_chunks = []   # NEW: store chunked audio files
is_playing = False
stop_flag = False
selected_language = "English"


# -------------------------------
# PDF TEXT EXTRACTION
# -------------------------------
def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    return text


# -------------------------------
# TRANSLATION
# -------------------------------
def translate_text(text):
    if selected_language == "Spanish":
        return GoogleTranslator(source='auto', target='es').translate(text)
    return text


# -------------------------------
# SPLIT TEXT INTO CHUNKS
# -------------------------------
def split_text(text, max_length=1000):
    """
    Breaks text into smaller pieces.

    WHY:
    Allows us to stop playback between chunks.
    """
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]


# -------------------------------
# TEXT TO SPEECH (CHUNKED)
# -------------------------------
async def generate_audio_chunks(text_chunks):
    global audio_chunks
    audio_chunks = []

    voice = "en-US-AriaNeural"
    if selected_language == "Spanish":
        voice = "es-ES-ElviraNeural"

    for i, chunk in enumerate(text_chunks):
        file_name = f"chunk_{i}.mp3"
        communicate = edge_tts.Communicate(chunk, voice=voice)
        await communicate.save(file_name)
        audio_chunks.append(file_name)


def run_tts_chunks(text):
    chunks = split_text(text)
    asyncio.run(generate_audio_chunks(chunks))


# -------------------------------
# AUDIO PLAYBACK (FIXED STOP)
# -------------------------------
def play_audio_chunks():
    """
    Plays each chunk one at a time.
    Stops immediately when stop_flag is set.
    """
    global is_playing, stop_flag

    is_playing = True
    stop_flag = False

    for chunk in audio_chunks:
        if stop_flag:
            break

        try:
            playsound(chunk)
        except:
            pass

    is_playing = False
    status_label.configure(text="Finished")


def stop_audio():
    """
    REAL STOP:
    Stops playback between chunks.
    """
    global stop_flag
    stop_flag = True
    status_label.configure(text="Stopped")


# -------------------------------
# MAIN PROCESS
# -------------------------------
def process_file(file_path):
    try:
        status_label.configure(text="Reading PDF...")
        text = extract_text_from_pdf(file_path)

        status_label.configure(text="Translating...")
        text = translate_text(text)

        status_label.configure(text="Generating audio...")
        run_tts_chunks(text)

        status_label.configure(text="Playing audio...")
        threading.Thread(target=play_audio_chunks, daemon=True).start()

    except Exception as e:
        messagebox.showerror("Error", str(e))


# -------------------------------
# BUTTON FUNCTIONS
# -------------------------------
def load_file():
    global current_file

    file_path = filedialog.askopenfilename(
        filetypes=[("PDF Files", "*.pdf")]
    )

    if file_path:
        current_file = file_path
        file_label.configure(text=os.path.basename(file_path))

        threading.Thread(
            target=process_file,
            args=(file_path,),
            daemon=True
        ).start()


def replay_audio():
    if audio_chunks:
        threading.Thread(target=play_audio_chunks, daemon=True).start()
    else:
        messagebox.showwarning("Warning", "No audio loaded.")


def stop():
    stop_audio()


def open_pdf():
    """
    Opens the selected PDF using system default viewer.
    """
    if current_file:
        os.startfile(current_file)  # Windows
    else:
        messagebox.showwarning("Warning", "No file selected.")


def change_language(choice):
    global selected_language
    selected_language = choice


# -------------------------------
# UI SETUP
# -------------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Read To Me")
app.geometry("520x400")

title = ctk.CTkLabel(app, text="PDF Reader (Text-to-Speech)", font=("Arial", 18))
title.pack(pady=10)

file_label = ctk.CTkLabel(app, text="No file selected")
file_label.pack(pady=5)

status_label = ctk.CTkLabel(app, text="Idle")
status_label.pack(pady=5)

# Language selector
language_menu = ctk.CTkOptionMenu(
    app,
    values=["English", "Spanish"],
    command=change_language
)
language_menu.pack(pady=10)

# Buttons
load_btn = ctk.CTkButton(app, text="Load PDF", command=load_file)
load_btn.pack(pady=10)

open_btn = ctk.CTkButton(app, text="Open PDF Viewer", command=open_pdf)
open_btn.pack(pady=5)

replay_btn = ctk.CTkButton(app, text="Replay Audio", command=replay_audio)
replay_btn.pack(pady=5)

stop_btn = ctk.CTkButton(app, text="Stop", command=stop)
stop_btn.pack(pady=5)

app.mainloop()