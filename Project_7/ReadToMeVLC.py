import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import asyncio
import edge_tts
import vlc
import os
from pypdf import PdfReader
from deep_translator import GoogleTranslator

# -------------------------------
# GLOBAL STATE
# -------------------------------
current_file = None
audio_file = "output.mp3"

is_paused = False
is_playing = False

selected_language = "English"

# VLC PLAYER
player = vlc.MediaPlayer()

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
# TEXT TO SPEECH
# -------------------------------
async def generate_audio(text):
    voice = "en-US-AriaNeural"
    if selected_language == "Spanish":
        voice = "es-ES-ElviraNeural"

    communicate = edge_tts.Communicate(text, voice=voice)
    await communicate.save(audio_file)


def run_tts(text):
    asyncio.run(generate_audio(text))


# -------------------------------
# VLC AUDIO CONTROLS
# -------------------------------
def play_audio():
    global is_playing, is_paused

    if not os.path.exists(audio_file):
        return

    media = vlc.Media(audio_file)
    player.set_media(media)
    player.play()

    is_playing = True
    is_paused = False


def pause_audio():
    global is_paused

    if is_playing:
        player.pause()
        is_paused = True


def resume_audio():
    global is_paused

    if is_playing:
        player.pause()  # VLC toggles pause
        is_paused = False


def stop_audio():
    global is_playing, is_paused

    player.stop()  # TRUE HARD STOP

    is_playing = False
    is_paused = False


# -------------------------------
# OPTIONAL VLC FEATURES
# -------------------------------
def set_volume(value):
    player.audio_set_volume(int(value))


def seek(seconds):
    if is_playing:
        current = player.get_time()
        player.set_time(current + seconds * 1000)


# -------------------------------
# MAIN PROCESS
# -------------------------------
def process_file(file_path):
    try:
        status_label.configure(text="Reading PDF...")
        text = extract_text_from_pdf(file_path)

        if not text.strip():
            raise Exception("No readable text found in PDF.")

        status_label.configure(text="Translating...")
        text = translate_text(text)

        status_label.configure(text="Generating audio...")
        run_tts(text)

        status_label.configure(text="Playing audio...")
        play_audio()

        status_label.configure(text="Playing")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        status_label.configure(text="Error")


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


def pause_resume():
    global is_paused, is_playing

    if not is_playing:
        return

    if is_paused:
        resume_audio()
        status_label.configure(text="Resumed")
    else:
        pause_audio()
        status_label.configure(text="Paused")


def stop():
    stop_audio()
    status_label.configure(text="Stopped")


def change_language(choice):
    global selected_language
    selected_language = choice


# -------------------------------
# UI SETUP
# -------------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Read To Me (VLC Edition)")
app.geometry("520x420")

title = ctk.CTkLabel(app, text="PDF Reader (VLC Playback)", font=("Arial", 18))
title.pack(pady=10)

file_label = ctk.CTkLabel(app, text="No file selected")
file_label.pack(pady=5)

status_label = ctk.CTkLabel(app, text="Idle")
status_label.pack(pady=5)

# Language
language_menu = ctk.CTkOptionMenu(
    app,
    values=["English", "Spanish"],
    command=change_language
)
language_menu.pack(pady=10)

# Buttons
load_btn = ctk.CTkButton(app, text="Load PDF", command=load_file)
load_btn.pack(pady=10)

pause_btn = ctk.CTkButton(app, text="Pause / Resume", command=pause_resume)
pause_btn.pack(pady=5)

stop_btn = ctk.CTkButton(app, text="Stop", command=stop)
stop_btn.pack(pady=5)

# -------------------------------
# EXTRA CONTROLS (NEW)
# -------------------------------

volume_slider = ctk.CTkSlider(app, from_=0, to=100, command=set_volume)
volume_slider.set(80)
volume_slider.pack(pady=10)

forward_btn = ctk.CTkButton(app, text="⏩ +10s", command=lambda: seek(10))
forward_btn.pack(pady=2)

back_btn = ctk.CTkButton(app, text="⏪ -10s", command=lambda: seek(-10))
back_btn.pack(pady=2)

# Run app
app.mainloop()