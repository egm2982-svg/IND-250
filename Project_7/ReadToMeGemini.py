import sys
import subprocess
import importlib.util
import tkinter as tk
from tkinter import messagebox

# -------------------------------
# DEPENDENCY BOOTSTRAPPER
# -------------------------------
# Required packages for the application
REQUIRED_PACKAGES = {
    'customtkinter': 'customtkinter',
    'edge_tts': 'edge-tts',
    'pypdf': 'pypdf',
    'deep_translator': 'deep-translator',
    'just_playback': 'just_playback'
}

missing_packages = []
for module, pip_name in REQUIRED_PACKAGES.items():
    if importlib.util.find_spec(module) is None:
        missing_packages.append(pip_name)

if missing_packages:
    root = tk.Tk()
    # Hide the main tk window during install prompt
    root.withdraw() 
    ans = messagebox.askyesno(
        "Missing Dependencies", 
        f"The following required packages are missing:\n\n{', '.join(missing_packages)}\n\nWould you like to install them automatically now?"
    )
    if ans:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing_packages])
            messagebox.showinfo("Success", "Packages installed successfully! The app will now load.")
        except Exception as e:
            messagebox.showerror("Install Error", f"Failed to install packages: {e}\nPlease install them manually.")
            sys.exit()
    else:
        sys.exit()

# --- Third-party library imports ---
import customtkinter as ctk
from tkinter import filedialog
import threading
import asyncio
import edge_tts
import os
from pypdf import PdfReader
from deep_translator import GoogleTranslator
from just_playback import Playback

# -------------------------------
# GLOBAL STATE
# -------------------------------
current_file = None
audio_file = "output.mp3"
selected_language = "English"

# Initialize the Audio Player
player = Playback()

# Prevents the slider from fighting the user when dragging
is_user_seeking = False  

# -------------------------------
# PDF & TRANSLATION
# -------------------------------
def extract_text_from_pdf(file_path):
    # Read the PDF and extract text page by page
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

def translate_text(text):
    # Translate to Spanish if selected in the UI
    if selected_language == "Spanish":
        return GoogleTranslator(source='auto', target='es').translate(text)
    return text

# -------------------------------
# TEXT TO SPEECH
# -------------------------------
async def generate_audio(text):
    # Generate the audio file using Microsoft Edge TTS
    voice = "en-US-AriaNeural" if selected_language == "English" else "es-ES-ElviraNeural"
    communicate = edge_tts.Communicate(text, voice=voice)
    await communicate.save(audio_file)

def run_tts(text):
    # Wrapper to run the async TTS function synchronously
    asyncio.run(generate_audio(text))

# -------------------------------
# AUDIO PLAYBACK (JUST_PLAYBACK)
# -------------------------------
def play_audio():
    # Load and play the generated audio file
    try:
        if player.active:
            player.stop()
            
        player.load_file(audio_file)
        player.play()
        
        # Configure slider to match audio duration
        progress_slider.configure(to=player.duration)
        pause_btn.configure(text="Pause")
        
        update_slider()
    except Exception as e:
        messagebox.showerror("Audio Error", str(e))

def toggle_pause():
    # Pause or resume the currently playing audio
    if player.active:
        if player.paused:
            player.resume()
            pause_btn.configure(text="Pause")
        else:
            player.pause()
            pause_btn.configure(text="Resume")

def stop_audio():
    # Stop playback and reset the UI slider
    if player.active:
        player.stop()
    progress_slider.set(0)
    status_label.configure(text="Stopped")
    pause_btn.configure(text="Pause")

def update_slider():
    # Updates the slider position as the audio plays
    global is_user_seeking
    
    if player.active and not is_user_seeking:
        current_pos = player.curr_pos
        progress_slider.set(current_pos)
    
    # Loop this function every 500ms for smooth UI updates
    if player.active:
        app.after(500, update_slider)
    elif not player.active and progress_slider.get() >= player.duration - 0.5:
        # Reset UI when audio finishes naturally
        progress_slider.set(0)
        status_label.configure(text="Finished")
        pause_btn.configure(text="Pause")

def slider_press(event):
    # Triggered when the user clicks the slider to start dragging
    global is_user_seeking
    is_user_seeking = True

def slider_release(value):
    # Triggered when the user lets go of the slider to set the new time
    global is_user_seeking
    if player.active:
        try:
            player.seek(float(value))
        except Exception:
            pass
    is_user_seeking = False

# -------------------------------
# MAIN PROCESS PIPELINE
# -------------------------------
def process_file(file_path):
    # Full pipeline to extract, translate, generate, and play
    try:
        status_label.configure(text="Reading PDF...")
        text = extract_text_from_pdf(file_path)

        status_label.configure(text="Translating...")
        text = translate_text(text)

        # Update Text Box so the user can read along
        text_box.configure(state="normal")
        text_box.delete("1.0", "end")
        text_box.insert("1.0", text)
        text_box.configure(state="disabled")

        status_label.configure(text="Generating audio (this may take a moment)...")
        run_tts(text)

        status_label.configure(text="Playing audio...")
        play_audio()

    except Exception as e:
        messagebox.showerror("Error", str(e))
        status_label.configure(text="Idle")

# -------------------------------
# UI BUTTON FUNCTIONS
# -------------------------------
def load_file():
    # Open file dialog and start the processing thread
    global current_file
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        current_file = file_path
        file_label.configure(text=os.path.basename(file_path))
        threading.Thread(target=process_file, args=(file_path,), daemon=True).start()

def replay_audio():
    # Replay the existing audio file without re-generating it
    if os.path.exists(audio_file):
        play_audio()
        status_label.configure(text="Playing audio...")
    else:
        messagebox.showwarning("Warning", "No audio loaded yet.")

def change_language(choice):
    # Update the selected language
    global selected_language
    selected_language = choice

# -------------------------------
# UI SETUP
# -------------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Read To Me - Advanced")
app.geometry("600x550")

title = ctk.CTkLabel(app, text="PDF Reader (Text-to-Speech)", font=("Arial", 18, "bold"))
title.pack(pady=10)

# Top frame for controls
control_frame = ctk.CTkFrame(app)
control_frame.pack(pady=10, padx=20, fill="x")

file_label = ctk.CTkLabel(control_frame, text="No file selected")
file_label.pack(pady=5)

language_menu = ctk.CTkOptionMenu(control_frame, values=["English", "Spanish"], command=change_language)
language_menu.pack(pady=5)

load_btn = ctk.CTkButton(control_frame, text="Load & Process PDF", command=load_file)
load_btn.pack(pady=5)

status_label = ctk.CTkLabel(control_frame, text="Idle", text_color="gray")
status_label.pack(pady=5)

# Middle frame for Audio Player controls
player_frame = ctk.CTkFrame(app)
player_frame.pack(pady=10, padx=20, fill="x")

# Slider with dedicated press/release commands
progress_slider = ctk.CTkSlider(player_frame, from_=0, to=100, command=slider_release)
progress_slider.bind("<Button-1>", slider_press)
progress_slider.set(0)
progress_slider.pack(pady=10, padx=10, fill="x")

button_frame = ctk.CTkFrame(player_frame, fg_color="transparent")
button_frame.pack(pady=5)

replay_btn = ctk.CTkButton(button_frame, text="Replay", width=80, command=replay_audio)
replay_btn.grid(row=0, column=0, padx=5)

pause_btn = ctk.CTkButton(button_frame, text="Pause", width=80, command=toggle_pause)
pause_btn.grid(row=0, column=1, padx=5)

stop_btn = ctk.CTkButton(button_frame, text="Stop", width=80, command=stop_audio)
stop_btn.grid(row=0, column=2, padx=5)

# Bottom frame for Text Display (Read-along)
text_frame = ctk.CTkFrame(app)
text_frame.pack(pady=10, padx=20, fill="both", expand=True)

text_label = ctk.CTkLabel(text_frame, text="Extracted Text:")
text_label.pack(anchor="w", padx=5)

text_box = ctk.CTkTextbox(text_frame, wrap="word")
text_box.pack(fill="both", expand=True, padx=5, pady=5)
text_box.insert("1.0", "Your PDF text will appear here so you can read along...")
text_box.configure(state="disabled")

app.mainloop()