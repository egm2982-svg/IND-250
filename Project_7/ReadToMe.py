import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import asyncio
import edge_tts
import os
from pypdf import PdfReader
from deep_translator import GoogleTranslator
from playsound import playsound

# -------------------------------
# GLOBAL STATE
# -------------------------------
current_file = None
audio_file = "output.mp3"

is_playing = False
stop_flag = False  # Used to simulate stopping playback

selected_language = "English"


# -------------------------------
# PDF TEXT EXTRACTION
# -------------------------------
def extract_text_from_pdf(file_path):
    """
    Extracts all readable text from a PDF file.

    WHY:
    Text must be extracted before converting to speech.
    """
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
    """
    Translates text into Spanish if selected.
    """
    if selected_language == "Spanish":
        return GoogleTranslator(source='auto', target='es').translate(text)
    return text


# -------------------------------
# TEXT TO SPEECH
# -------------------------------
async def generate_audio(text):
    """
    Converts text into speech using edge_tts.
    Saves result as MP3.
    """
    voice = "en-US-AriaNeural"

    if selected_language == "Spanish":
        voice = "es-ES-ElviraNeural"

    communicate = edge_tts.Communicate(text, voice=voice)
    await communicate.save(audio_file)


def run_tts(text):
    """
    Runs async TTS in a synchronous context.
    """
    asyncio.run(generate_audio(text))


# -------------------------------
# AUDIO PLAYBACK (PLAYSOND)
# -------------------------------
def play_audio():
    """
    Plays audio file.

    IMPORTANT:
    playsound is blocking, so we run it in a thread.
    """
    global is_playing, stop_flag

    is_playing = True
    stop_flag = False

    try:
        playsound(audio_file)
    except Exception as e:
        messagebox.showerror("Audio Error", str(e))

    is_playing = False


def stop_audio():
    """
    Simulated stop.

    NOTE:
    playsound cannot truly stop playback once started.
    This only updates UI state.
    """
    global stop_flag, is_playing
    stop_flag = True
    is_playing = False


# -------------------------------
# MAIN PROCESS PIPELINE
# -------------------------------
def process_file(file_path):
    """
    Full pipeline:
    1. Read PDF
    2. Translate (optional)
    3. Generate audio
    4. Play audio
    """
    try:
        status_label.configure(text="Reading PDF...")
        text = extract_text_from_pdf(file_path)

        status_label.configure(text="Translating...")
        text = translate_text(text)

        status_label.configure(text="Generating audio...")
        run_tts(text)

        status_label.configure(text="Playing audio...")

        # Run audio in separate thread so UI stays responsive
        threading.Thread(target=play_audio, daemon=True).start()

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
    """
    Replays the last generated audio.
    """
    if os.path.exists(audio_file):
        threading.Thread(target=play_audio, daemon=True).start()
    else:
        messagebox.showwarning("Warning", "No audio loaded yet.")


def stop():
    """
    Stops playback (UI-level only).
    """
    stop_audio()
    status_label.configure(text="Stopped (soft stop)")


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
app.geometry("500x350")

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

replay_btn = ctk.CTkButton(app, text="Replay Audio", command=replay_audio)
replay_btn.pack(pady=5)

stop_btn = ctk.CTkButton(app, text="Stop", command=stop)
stop_btn.pack(pady=5)

app.mainloop()