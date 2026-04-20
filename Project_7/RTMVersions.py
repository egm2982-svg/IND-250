# ==============================================================================
# INSTALLATION NOTE FOR VS CODE VERSION 1.116.0+ USERS
# ==============================================================================
# If you are using VS Code v1.116.0, the auto-installer below may install 
# packages to your global Python environment instead of your workspace's 
# virtual environment (.venv). 
#
# To install manually in VS Code:
# 1. Open the Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
# 2. Select "Python: Select Interpreter" -> Choose your virtual environment
# 3. Open a new integrated terminal (Terminal -> New Terminal)
# 4. Run the pip install command for your chosen packages.
# ==============================================================================

import sys
import subprocess
import importlib.util
import tkinter as tk
from tkinter import messagebox

# -------------------------------
# STARTUP: VERSION & ENGINE CHECK
# -------------------------------
root = tk.Tk()
root.withdraw() 

is_116 = messagebox.askyesno(
    "VS Code Version Check", 
    "Are you currently using VS Code version 1.116.0?\n\n(Click 'No' if you are using an updated version)"
)

use_playback3 = False
use_alt_translator = False

if is_116:
    use_playback3 = messagebox.askyesno(
        "Audio Engine Selection", 
        "Since you are on v1.116.0, would you like to use the 'playback3' library for audio instead of the default 'just_playback'?"
    )
    
    use_alt_translator = messagebox.askyesno(
        "Translator Selection",
        "Would you also like to use the alternative translator ('googletrans') optimized for v1.116.0 instead of 'deep-translator'?"
    )

# -------------------------------
# DEPENDENCY BOOTSTRAPPER
# -------------------------------
REQUIRED_PACKAGES = {
    'customtkinter': 'customtkinter',
    'edge_tts': 'edge-tts',
    'pypdf': 'pypdf'
}

# Dynamically assign audio dependency
if use_playback3:
    REQUIRED_PACKAGES['playback3'] = 'playback3'
else:
    REQUIRED_PACKAGES['just_playback'] = 'just_playback'

# Dynamically assign translator dependency
if use_alt_translator:
    # 4.0.0-rc1 is the most stable modern release of googletrans
    REQUIRED_PACKAGES['googletrans'] = 'googletrans==4.0.0-rc1'
else:
    REQUIRED_PACKAGES['deep_translator'] = 'deep-translator'


missing_packages = []
for module, pip_name in REQUIRED_PACKAGES.items():
    if importlib.util.find_spec(module) is None:
        missing_packages.append(pip_name)

if missing_packages:
    prompt_message = (
        f"The following required packages are missing:\n\n{', '.join(missing_packages)}\n\n"
        f"Would you like to install them automatically now?\n\n"
        f"NOTE FOR VS CODE 1.116.0 USERS:\n"
        f"If you are using a virtual environment, it is recommended to click 'No' "
        f"and install these manually via your integrated terminal."
    )
    
    ans = messagebox.askyesno("Missing Dependencies", prompt_message)
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

# -------------------------------
# GLOBAL STATE & DYNAMIC ENGINES
# -------------------------------
current_file = None
original_text = ""
audio_file = "output.mp3"
selected_language = "English"

# 1. Assign Audio Engine
if use_playback3:
    import playback3
    player = playback3.Playback()
else:
    from just_playback import Playback
    player = Playback()

# 2. Assign Translator Engine
translator_engine = None
if use_alt_translator:
    from googletrans import Translator
    translator_engine = Translator()
else:
    from deep_translator import GoogleTranslator

is_user_seeking = False  
word_boundaries = []
ui_word_timings = []
highlight_loop_id = None
slider_loop_id = None

# -------------------------------
# PDF & TRANSLATION
# -------------------------------
def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

def safe_translate(text, target_lang_code):
    if not text.strip():
        return ""
        
    chunks = [text[i:i+4500] for i in range(0, len(text), 4500)]
    translated_text = ""
    
    for chunk in chunks:
        if use_alt_translator:
            # Using googletrans
            result = translator_engine.translate(chunk, dest=target_lang_code)
            if result and result.text:
                translated_text += result.text + " "
        else:
            # Using deep-translator
            translated_chunk = GoogleTranslator(source='auto', target=target_lang_code).translate(chunk)
            if translated_chunk:
                translated_text += translated_chunk + " "
            
    return translated_text

# -------------------------------
# TEXT TO SPEECH & TIMESTAMPS
# -------------------------------
async def generate_audio_and_timestamps(text):
    global word_boundaries
    word_boundaries = []
    
    voice = "es-ES-ElviraNeural" if selected_language == "Spanish" else "en-US-AriaNeural"
    communicate = edge_tts.Communicate(text, voice=voice)
    
    with open(audio_file, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                start_sec = chunk["offset"] / 10000000.0
                end_sec = (chunk["offset"] + chunk["duration"]) / 10000000.0
                word_boundaries.append({
                    "start": start_sec,
                    "end": end_sec,
                    "text": chunk["text"]
                })

def run_tts(text):
    asyncio.run(generate_audio_and_timestamps(text))

# -------------------------------
# AUDIO PLAYBACK & HIGHLIGHTING
# -------------------------------
def play_audio():
    global highlight_loop_id, slider_loop_id
    try:
        if player.active:
            player.stop()
            if highlight_loop_id:
                app.after_cancel(highlight_loop_id)
            if slider_loop_id:
                app.after_cancel(slider_loop_id)
            
        player.load_file(audio_file)
        player.play()
        
        progress_slider.configure(to=player.duration)
        pause_btn.configure(text="Pause")
        
        update_slider()
        update_highlight()
    except Exception as e:
        messagebox.showerror("Audio Error", str(e))

def update_highlight():
    global highlight_loop_id
    
    if player.active and not is_user_seeking:
        curr_time = player.curr_pos
        
        # Clear existing highlights
        text_box.tag_remove("highlight", "1.0", "end")
        
        for item in ui_word_timings:
            # 0.1 buffer keeps the highlight smooth
            if item["start"] <= curr_time <= (item["end"] + 0.1):
                text_box.tag_add("highlight", item["tk_start"], item["tk_end"])
                text_box.see(item["tk_start"])
                break
                
    if player.active:
        highlight_loop_id = app.after(50, update_highlight)

def toggle_pause():
    if player.active:
        if player.paused:
            player.resume()
            pause_btn.configure(text="Pause")
            status_label.configure(text="Playing audio...")
        else:
            player.pause()
            pause_btn.configure(text="Resume")
            status_label.configure(text="Paused")

def stop_audio():
    if player.active:
        player.pause() # Pause to prevent it playing in the background behind the prompt
        
    if original_text:
        ans = messagebox.askyesno("Stopped", "Playback Stopped.\n\nClick YES to upload a new PDF, or NO to return to the Main Menu.")
        
        # Hard stop regardless of choice
        player.stop()
        progress_slider.set(0)
        pause_btn.configure(text="Pause")
        text_box.tag_remove("highlight", "1.0", "end")
        
        if ans:
            status_label.configure(text="Stopped")
            load_file()
        else:
            reset_to_main_menu()
    else:
        # If no text was loaded but stop was clicked somehow
        if player.active:
            player.stop()
        progress_slider.set(0)

def reset_to_main_menu():
    # Resets the UI entirely to its starting state
    global current_file, original_text
    current_file = None
    original_text = ""
    
    file_label.configure(text="No file selected")
    status_label.configure(text="Idle")
    
    text_box.configure(state="normal")
    text_box.delete("1.0", "end")
    text_box.insert("1.0", "Your English or Spanish text will appear here so you can read along...")
    text_box.configure(state="disabled")

def update_slider():
    global is_user_seeking, slider_loop_id
    
    if player.active and not is_user_seeking:
        progress_slider.set(player.curr_pos)
    
    if player.active:
        slider_loop_id = app.after(500, update_slider)
    elif not player.active and progress_slider.get() >= player.duration - 0.5:
        progress_slider.set(0)
        status_label.configure(text="Finished")
        pause_btn.configure(text="Pause")
        text_box.tag_remove("highlight", "1.0", "end")

def slider_press(event):
    global is_user_seeking
    is_user_seeking = True

def slider_release(value):
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
def process_content():
    global ui_word_timings
    try:
        status_label.configure(text=f"Translating to {selected_language}...")
        
        target_code = 'es' if selected_language == "Spanish" else 'en'
        processed_text = safe_translate(original_text, target_code)

        # Insert text first so Tkinter establishes its internal indexing
        text_box.configure(state="normal")
        text_box.delete("1.0", "end")
        text_box.insert("1.0", processed_text)
        text_box.configure(state="disabled")

        status_label.configure(text="Generating audio & mapping timestamps...")
        run_tts(processed_text)

        ui_word_timings = []
        char_offset = 0
        
        for wb in word_boundaries:
            word = wb["text"]
            idx = processed_text.find(word, char_offset)
            
            if idx != -1:
                tk_start = text_box.index(f"1.0 + {idx} chars")
                end_idx = idx + len(word)
                tk_end = text_box.index(f"1.0 + {end_idx} chars")
                
                ui_word_timings.append({
                    "start": wb["start"],
                    "end": wb["end"],
                    "tk_start": tk_start,
                    "tk_end": tk_end
                })
                char_offset = end_idx

        status_label.configure(text="Audio generated. Press Play to start.")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        status_label.configure(text="Idle")

# -------------------------------
# UI BUTTON FUNCTIONS
# -------------------------------
def load_file():
    global current_file, original_text
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    
    if file_path:
        current_file = file_path
        file_label.configure(text=os.path.basename(file_path))
        
        status_label.configure(text="Reading PDF...")
        original_text = extract_text_from_pdf(file_path)
        
        threading.Thread(target=process_content, daemon=True).start()

def action_play_audio():
    if os.path.exists(audio_file) and original_text:
        play_audio()
        status_label.configure(text="Playing audio...")
    else:
        messagebox.showwarning("Warning", "No PDF processed yet.")

def replay_audio():
    if os.path.exists(audio_file) and original_text:
        play_audio()
        status_label.configure(text="Playing audio...")
    else:
        messagebox.showwarning("Warning", "No audio loaded yet.")

def change_language(choice):
    global selected_language
    selected_language = choice
    
    if original_text:
        if player.active:
            player.stop()
        threading.Thread(target=process_content, daemon=True).start()

def exit_app():
    if player.active:
        player.stop()
    app.quit()

# -------------------------------
# UI SETUP
# -------------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Read To Me - Live Karaoke Sync")
app.geometry("650x680")

title = ctk.CTkLabel(app, text="PDF Reader (Live Highlighting)", font=("Arial", 18, "bold"))
title.pack(pady=10)

# Top frame for controls
control_frame = ctk.CTkFrame(app)
control_frame.pack(pady=10, padx=20, fill="x")

file_label = ctk.CTkLabel(control_frame, text="No file selected")
file_label.pack(pady=5)

language_menu = ctk.CTkOptionMenu(control_frame, values=["English", "Spanish"], command=change_language)
language_menu.pack(pady=5)

warning_label = ctk.CTkLabel(control_frame, text="Note: Cannot switch mid audio, close and restart.", text_color="#ffcc00", font=("Arial", 11, "italic"))
warning_label.pack(pady=(0, 5))

# Group buttons in the control frame
top_btn_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
top_btn_frame.pack(pady=5)

load_btn = ctk.CTkButton(top_btn_frame, text="Load PDF", width=120, command=load_file)
load_btn.grid(row=0, column=0, padx=5)

exit_btn = ctk.CTkButton(top_btn_frame, text="Exit", width=120, fg_color="darkred", hover_color="red", command=exit_app)
exit_btn.grid(row=0, column=1, padx=5)

status_label = ctk.CTkLabel(control_frame, text="Idle", text_color="gray")
status_label.pack(pady=5)

# Middle frame for Audio Player controls
player_frame = ctk.CTkFrame(app)
player_frame.pack(pady=10, padx=20, fill="x")

progress_slider = ctk.CTkSlider(player_frame, from_=0, to=100, command=slider_release)
progress_slider.bind("<Button-1>", slider_press)
progress_slider.set(0)
progress_slider.pack(pady=10, padx=10, fill="x")

button_frame = ctk.CTkFrame(player_frame, fg_color="transparent")
button_frame.pack(pady=5)

# Buttons aligned side-by-side cleanly
play_btn = ctk.CTkButton(button_frame, text="Play", width=80, command=action_play_audio)
play_btn.grid(row=0, column=0, padx=5)

replay_btn = ctk.CTkButton(button_frame, text="Replay", width=80, command=replay_audio)
replay_btn.grid(row=0, column=1, padx=5)

pause_btn = ctk.CTkButton(button_frame, text="Pause", width=80, command=toggle_pause)
pause_btn.grid(row=0, column=2, padx=5)

stop_btn = ctk.CTkButton(button_frame, text="Stop", width=80, command=stop_audio)
stop_btn.grid(row=0, column=3, padx=5)

# Bottom frame for Text Display
text_frame = ctk.CTkFrame(app)
text_frame.pack(pady=10, padx=20, fill="both", expand=True)

text_label = ctk.CTkLabel(text_frame, text="Live Read-Along:")
text_label.pack(anchor="w", padx=5)

text_box = ctk.CTkTextbox(text_frame, wrap="word", font=("Arial", 14))
text_box.pack(fill="both", expand=True, padx=5, pady=5)
text_box.insert("1.0", "Your English or Spanish text will appear here so you can read along...")
text_box.configure(state="disabled")

text_box.tag_config("highlight", background="yellow", foreground="black")

app.mainloop()