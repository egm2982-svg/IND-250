"""
PDF READER (EDGE TTS + VLC AUDIO + HIGHLIGHTING)
------------------------------------------------
- Uses VLC for stable playback
- Supports pause/resume/stop
- Keeps translation + highlighting
"""

# -------------------------------
# FAILSAFE IMPORT SYSTEM
# -------------------------------
missing = []
import vlc

player = vlc.MediaPlayer("test.mp3")
player.play()

def safe_import(name, install=None):
    try:
        return __import__(name)
    except:
        missing.append(install or name)
        return None

ctk = safe_import("customtkinter")
filedialog = safe_import("tkinter.filedialog")
messagebox = safe_import("tkinter.messagebox")
threading = safe_import("threading")
asyncio = safe_import("asyncio")
edge_tts = safe_import("edge_tts", "edge-tts")
os = safe_import("os")
pypdf = safe_import("pypdf")
deep_translator = safe_import("deep_translator", "deep-translator")
vlc = safe_import("vlc", "python-vlc")
time = safe_import("time")

if missing:
    print("\nInstall required packages:\n")
    for m in missing:
        print(f"pip install {m}")
    print("\nAlso install VLC media player from https://www.videolan.org/")
    exit()

from pypdf import PdfReader
from deep_translator import GoogleTranslator

# -------------------------------
# GLOBAL STATE
# -------------------------------
current_file = None
audio_file = "output.mp3"
text_words = []

player = None
is_playing = False
is_paused = False
selected_language = "English"

# -------------------------------
# PDF TEXT EXTRACTION
# -------------------------------
def extract_text(file_path):
    reader = PdfReader(file_path)
    text = ""
    for p in reader.pages:
        t = p.extract_text()
        if t:
            text += t + " "
    return text

# -------------------------------
# TRANSLATION
# -------------------------------
def translate(text):
    if selected_language == "Spanish":
        try:
            return GoogleTranslator(source='auto', target='es').translate(text)
        except:
            return text
    return text

# -------------------------------
# EDGE TTS
# -------------------------------
async def generate_audio(text):
    voice = "en-US-AriaNeural"
    if selected_language == "Spanish":
        voice = "es-ES-ElviraNeural"

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(audio_file)

def run_tts(text):
    asyncio.run(generate_audio(text))

# -------------------------------
# VLC AUDIO CONTROL
# -------------------------------
def play_audio():
    global player, is_playing, is_paused

    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(audio_file)
    player.set_media(media)

    player.play()
    is_playing = True
    is_paused = False

    word_index = 0

    while player.is_playing():
        if word_index < len(text_words):
            highlight_word(word_index)
            word_index += 1

        time.sleep(0.4)

    is_playing = False


def pause_audio():
    global is_paused
    if player:
        player.pause()
        is_paused = not is_paused


def stop_audio():
    global is_playing
    if player:
        player.stop()
    is_playing = False

# -------------------------------
# PROCESS PIPELINE
# -------------------------------
def process_file(path):
    try:
        status_label.configure(text="Reading PDF...")
        text = extract_text(path)

        status_label.configure(text="Translating...")
        text = translate(text)

        global text_words
        text_words = text.split()

        textbox.delete("1.0", "end")
        textbox.insert("end", text)

        status_label.configure(text="Generating audio...")
        run_tts(text)

        status_label.configure(text="Playing...")
        threading.Thread(target=play_audio, daemon=True).start()

    except Exception as e:
        messagebox.showerror("Error", str(e))

# -------------------------------
# UI FUNCTIONS
# -------------------------------
def load_file():
    global current_file
    file_path = filedialog.askopenfilename(filetypes=[("PDF", "*.pdf")])
    if file_path:
        current_file = file_path
        file_label.configure(text=os.path.basename(file_path))
        threading.Thread(target=process_file, args=(file_path,), daemon=True).start()

def replay():
    if os.path.exists(audio_file):
        threading.Thread(target=play_audio, daemon=True).start()

def stop():
    stop_audio()
    status_label.configure(text="Stopped")

def pause():
    pause_audio()
    status_label.configure(text="Paused")

def change_language(choice):
    global selected_language
    selected_language = choice

# -------------------------------
# HIGHLIGHT FUNCTION
# -------------------------------
def highlight_word(index):
    textbox.tag_remove("hl", "1.0", "end")

    start = "1.0"
    for i in range(index):
        pos = textbox.search(text_words[i], start)
        if not pos:
            return
        start = f"{pos}+{len(text_words[i])}c"

    pos = textbox.search(text_words[index], start)
    if pos:
        end = f"{pos}+{len(text_words[index])}c"
        textbox.tag_add("hl", pos, end)
        textbox.see(pos)

# -------------------------------
# UI SETUP
# -------------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("PDF Voice Reader (VLC Edition)")
app.geometry("700x500")

title = ctk.CTkLabel(app, text="PDF Reader (Neural Voice)", font=("Arial", 20))
title.pack(pady=10)

file_label = ctk.CTkLabel(app, text="No file selected")
file_label.pack()

status_label = ctk.CTkLabel(app, text="Idle")
status_label.pack()

language_menu = ctk.CTkOptionMenu(app, values=["English", "Spanish"], command=change_language)
language_menu.pack(pady=10)

textbox = ctk.CTkTextbox(app, height=250)
textbox.pack(fill="both", expand=True, padx=10)
textbox.tag_config("hl", background="yellow")

load_btn = ctk.CTkButton(app, text="Load PDF", command=load_file)
load_btn.pack(pady=5)

replay_btn = ctk.CTkButton(app, text="Replay", command=replay)
replay_btn.pack(pady=5)

pause_btn = ctk.CTkButton(app, text="Pause/Resume", command=pause)
pause_btn.pack(pady=5)

stop_btn = ctk.CTkButton(app, text="Stop", command=stop)
stop_btn.pack(pady=5)

app.mainloop()