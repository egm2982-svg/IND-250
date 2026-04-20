import sys
import subprocess
import importlib.util
import tkinter as tk
from tkinter import messagebox

# -------------------------------
# DEPENDENCY BOOTSTRAPPER
# -------------------------------
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
original_text = ""
audio_file = "output.mp3"
selected_language = "English"

# Audio Player and Timings
player = Playback()
is_user_seeking = False  
word_boundaries = []  # Stores raw TTS timing data
ui_word_timings = []  # Stores mapped Tkinter text positions
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
        translated_chunk = GoogleTranslator(source='auto', target=target_lang_code).translate(chunk)
        if translated_chunk:
            translated_text += translated_chunk + " "
            
    return translated_text

# -------------------------------
# TEXT TO SPEECH & TIMESTAMPS
# -------------------------------
async def generate_audio_and_timestamps(text):
    # This intercepts the stream to get both audio data and word boundary timestamps
    global word_boundaries
    word_boundaries = []
    
    voice = "es-ES-ElviraNeural" if selected_language == "Spanish" else "en-US-AriaNeural"
    communicate = edge_tts.Communicate(text, voice=voice)
    
    with open(audio_file, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                # Write raw audio bytes to file
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                # Offset is in 100-nanosecond units. Divide by 10 million to get seconds.
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
        
        # Start our two UI loops
        update_slider()
        update_highlight()
    except Exception as e:
        messagebox.showerror("Audio Error", str(e))

def update_highlight():
    # Polls every 50ms to check the audio position and highlight the correct word
    global highlight_loop_id
    
    if player.active and not is_user_seeking:
        curr_time = player.curr_pos
        
        # Remove any existing highlight tags
        text_box.tag_remove("highlight", "1.0", "end")
        
        # Find which word we are currently speaking
        for item in ui_word_timings:
            # Added a 0.1s buffer to keep the highlight smooth
            if item["start"] <= curr_time <= (item["end"] + 0.1):
                text_box.tag_add("highlight", item["tk_start"], item["tk_end"])
                # Automatically scroll the text box to the active word
                text_box.see(item["tk_start"])
                break
                
    if player.active:
        highlight_loop_id = app.after(50, update_highlight)

def toggle_pause():
    if player.active:
        if player.paused:
            player.resume()
            pause_btn.configure(text="Pause")
        else:
            player.pause()
            pause_btn.configure(text="Resume")

def stop_audio():
    if player.active:
        player.stop()
    progress_slider.set(0)
    status_label.configure(text="Stopped")
    pause_btn.configure(text="Pause")
    text_box.tag_remove("highlight", "1.0", "end")

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

        text_box.configure(state="normal")
        text_box.delete("1.0", "end")
        text_box.insert("1.0", processed_text)
        text_box.configure(state="disabled")

        status_label.configure(text="Generating audio & mapping timestamps...")
        run_tts(processed_text)

        # -------------------------------------------------------------
        # THE MAGIC: Map raw timestamps to strict Tkinter Line.Col indices
        # -------------------------------------------------------------
        ui_word_timings = []
        char_offset = 0
        
        for wb in word_boundaries:
            word = wb["text"]
            # Find the index of the word in the processed string
            idx = processed_text.find(word, char_offset)
            
            if idx != -1:
                # Calculate start Line and Column
                line_count = processed_text.count('\n', 0, idx) + 1
                last_newline = processed_text.rfind('\n', 0, idx)
                col = idx - (last_newline + 1)
                tk_start = f"{line_count}.{col}"
                
                # Calculate end Line and Column
                end_idx = idx + len(word)
                end_line_count = processed_text.count('\n', 0, end_idx) + 1
                end_last_newline = processed_text.rfind('\n', 0, end_idx)
                end_col = end_idx - (end_last_newline + 1)
                tk_end = f"{end_line_count}.{end_col}"
                
                ui_word_timings.append({
                    "start": wb["start"],
                    "end": wb["end"],
                    "tk_start": tk_start,
                    "tk_end": tk_end
                })
                # Move the offset forward so we don't map to the same word twice
                char_offset = end_idx

        status_label.configure(text="Playing audio...")
        play_audio()

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

def replay_audio():
    if os.path.exists(audio_file):
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

# -------------------------------
# UI SETUP
# -------------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Read To Me - Live Karaoke Sync")
app.geometry("650x600")

title = ctk.CTkLabel(app, text="PDF Reader (Live Highlighting)", font=("Arial", 18, "bold"))
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

# Bottom frame for Text Display
text_frame = ctk.CTkFrame(app)
text_frame.pack(pady=10, padx=20, fill="both", expand=True)

text_label = ctk.CTkLabel(text_frame, text="Live Read-Along:")
text_label.pack(anchor="w", padx=5)

text_box = ctk.CTkTextbox(text_frame, wrap="word", font=("Arial", 14))
text_box.pack(fill="both", expand=True, padx=5, pady=5)
text_box.insert("1.0", "Your English or Spanish text will appear here so you can read along...")
text_box.configure(state="disabled")

# Configure the highlight tag visuals (Blue background, White text)
text_box.tag_config("highlight", background="#1f6aa5", foreground="white")

app.mainloop()