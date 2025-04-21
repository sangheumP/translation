import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
import tkinter.font as tkfont
from tkinter import filedialog, messagebox
import pandas as pd
import difflib
import os
import re
import random
from PIL import Image, ImageTk
import json

root = ttk.Window(themename="cosmo")
FONT_SIZES = {"작게": 12, "보통": 14, "크게": 16}

root.title("Language Reactor Quiz")
root.geometry("800x600")

font_size_var = tk.StringVar(value="보통")
theme_var = tk.StringVar(value="cosmo")

subtitles = []
current_index = 0
user_answers = []
favorites = []
vocab_list = []
show_answer_var = tk.BooleanVar(value=False)
shuffle_enabled = tk.BooleanVar(value=False)

FONT_LARGE = ("Arial", 28)
FONT_MEDIUM = ("Arial", 20)
FONT_NORMAL = ("Arial", 14)
FONT_BOLD = ("Arial", 16, "bold")

def normalize(text):
    text = text.lower()
    text = re.sub(r"[^\w\s']", "", text)
    contractions = {
        "im": "i am", "i'm": "i am",
        "youre": "you are", "you're": "you are",
        "hes": "he is", "he's": "he is",
        "shes": "she is", "she's": "she is",
        "its": "it is", "it's": "it is",
        "were": "we are", "we're": "we are",
        "theyre": "they are", "they're": "they are",
        "ive": "i have", "i've": "i have",
        "cant": "cannot", "can't": "cannot",
        "dont": "do not", "doesnt": "does not", "didnt": "did not",
        "wont": "will not", "wouldnt": "would not",
    }
    words = text.split()
    new_words = [contractions.get(w, w) for w in words]
    return ' '.join(new_words)

def check_similarity(a, b):
    a, b = normalize(a), normalize(b)
    return int(difflib.SequenceMatcher(None, a, b).ratio() * 100)

def extract_keywords(sentence):
    stopwords = {'the', 'a', 'an', 'is', 'are', 'am', 'i', 'you', 'he', 'she', 'we', 'they', 'to', 'and', 'of', 'in'}
    words = re.findall(r"\b[a-zA-Z']+\b", sentence.lower())
    return sorted(set(w for w in words if w not in stopwords))

def show_frame(frame):
    for f in (home_frame, quiz_frame, vocab_frame, fav_frame, settings_frame):
        f.pack_forget()
    frame.pack(fill="both", expand=True)
    if frame == home_frame:
        continue_btn.state(["!disabled"] if subtitles else ["disabled"])
    elif frame == fav_frame:
        update_fav_list()
    elif frame == vocab_frame:
        update_vocab_list()

def load_csv():
    global subtitles, current_index
    path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not path: return
    df = pd.read_csv(path)
    if 'Subtitle' not in df.columns or 'Human Translation' not in df.columns:
        messagebox.showerror("오류", "Subtitle, Human Translation 열이 있어야 합니다.")
        return
    subtitles = df.to_dict(orient='records')
    if shuffle_enabled.get():
        random.shuffle(subtitles)
    current_index = 0
    show_question()
    show_frame(quiz_frame)

def show_question():
    if not subtitles: return
    entry.delete(0, tk.END)
    entry.focus()
    item = subtitles[current_index]
    question_label.config(text=item["Human Translation"])
    result_label.config(text="")
    answer_label.config(text="")
    fav_btn.config(text="★" if item in favorites else "☆")

def check_answer():
    if not subtitles: return
    user_input = entry.get()
    item = subtitles[current_index]
    correct = item["Subtitle"]
    score = check_similarity(correct, user_input)
    msg = "정답!" if score >= 90 else "가장 비슷해요." if score >= 70 else "❌ 의미가 다르어요."
    result_label.config(text=f"유사도 점수: {score}점\n{msg}")
    if show_answer_var.get():
        answer_label.config(text=f"📖 정답: {correct}")

def keyword_click(word):
    if word in vocab_list:
        vocab_list.remove(word)
        msg = f"❌ '{word}' 삭제됨"
    else:
        vocab_list.append(word)
        msg = f"✅ '{word}' 추가됨"
    update_vocab_list()
    vocab_notice_label.config(text=msg)
    quiz_notice_label.config(text=msg)
    vocab_frame.after(2000, lambda: vocab_notice_label.config(text=""))
    center_frame.after(2000, lambda: quiz_notice_label.config(text=""))

def toggle_answer():
    for w in keyword_frame.winfo_children():
        w.destroy()
    if show_answer_var.get():
        show_answer_var.set(False)
        answer_label.config(text="")
    else:
        show_answer_var.set(True)
        item = subtitles[current_index]
        correct = item["Subtitle"]
        answer_label.config(text=f"📖 정답: {correct}")
        for word in extract_keywords(correct):
            lbl = ttk.Label(keyword_frame, text=f"#{word}", font=FONT_NORMAL, foreground="#555", background="#f0f0f0", padding=(5, 2))
            lbl.pack(side="left", padx=4, pady=2)
            lbl.bind("<Button-1>", lambda e, w=word: keyword_click(w))

def delete_vocab_word(word):
    if word in vocab_list:
        vocab_list.remove(word)
        vocab_notice_label.config(text=f"❌ '{word}' 삭제됨")
        update_vocab_list()
        vocab_frame.after(2000, lambda: vocab_notice_label.config(text=""))


def update_vocab_list():
    for widget in vocab_listbox_frame.winfo_children():
        widget.destroy()

    for word in sorted(vocab_list):
        frame = ttk.Frame(vocab_listbox_frame, padding=8)
        frame.pack(fill="x", pady=4)

        lbl = ttk.Label(frame, text=f"📘 {word}", font=FONT_NORMAL, anchor="w")
        lbl.pack(side="left", fill="x", expand=True)

        # 더블클릭으로 삭제
        lbl.bind("<Double-Button-1>", lambda e, w=word: delete_vocab_word(w))


def toggle_favorite():
    if not subtitles: return
    item = subtitles[current_index]
    if item in favorites:
        favorites.remove(item)
    else:
        favorites.append(item)
    fav_btn.config(text="★" if item in favorites else "☆")
    update_fav_list()

def jump_to_favorite_by_index(idx):
    if idx < len(favorites):
        item = favorites[idx]
        if item in subtitles:
            global current_index
            current_index = subtitles.index(item)
            show_frame(quiz_frame)
            show_question()

def delete_favorite(item):
    if item in favorites:
        favorites.remove(item)
        update_fav_list()


def update_fav_list():
    for widget in fav_listbox_frame.winfo_children():
        widget.destroy()

    for item in favorites:
        frame = ttk.Frame(fav_listbox_frame, padding=10, relief="ridge", borderwidth=2)
        frame.pack(fill="x", pady=6, padx=4)

        label1 = ttk.Label(frame, text=f"🗣 {item['Human Translation']}", font=FONT_NORMAL, anchor="w", wraplength=700)
        label1.pack(fill="x", padx=4)

        label2 = ttk.Label(frame, text=f"📝 {item['Subtitle']}", font=FONT_NORMAL, anchor="w", wraplength=700, foreground="#444")
        label2.pack(fill="x", padx=4, pady=(0, 4))

        # 더블클릭 시 삭제
        frame.bind("<Double-Button-1>", lambda e, it=item: delete_favorite(it))
        label1.bind("<Double-Button-1>", lambda e, it=item: delete_favorite(it))
        label2.bind("<Double-Button-1>", lambda e, it=item: delete_favorite(it))


def go_to_question():
    show_frame(quiz_frame)
    show_question()

def delete_from_vocab():
    selection = vocab_listbox.curselection()
    if selection:
        word = vocab_listbox.get(selection[0])
        vocab_list.remove(word)
        update_vocab_list()

def change_question(delta):
    global current_index
    if not subtitles: return
    current_index = (current_index + delta) % len(subtitles)
    show_question()

FAV_FILE = "favorites.json"
VOCAB_FILE = "vocab.json"

def save_data():
    unique_favorites = [dict(t) for t in {tuple(d.items()) for d in favorites}]
    with open(FAV_FILE, "w", encoding="utf-8") as f:
        json.dump(unique_favorites, f, ensure_ascii=False, indent=2)
    with open(VOCAB_FILE, "w", encoding="utf-8") as f:  # 🔥 이 부분 추가
        json.dump(vocab_list, f, ensure_ascii=False, indent=2)    

def load_saved_data():
    global favorites, vocab_list
    if os.path.exists(FAV_FILE):
        with open(FAV_FILE, encoding="utf-8") as f:
            try:
                favorites = json.load(f)
            except json.JSONDecodeError:
                favorites = []
    if os.path.exists(VOCAB_FILE):
        with open(VOCAB_FILE, encoding="utf-8") as f:
            try:
                vocab_list = json.load(f)
            except json.JSONDecodeError:
                vocab_list = []

root.protocol("WM_DELETE_WINDOW", lambda: (save_data(), root.destroy()))
load_saved_data()

def jump_to_favorite(event):
    selection = fav_listbox.curselection()
    if not selection:
        return
    index = selection[0]
    if index % 4 == 1:  # '🗣 번역' 줄만 반응
        fav_index = index // 4
        item = favorites[fav_index]
        if item in subtitles:
            global current_index
            current_index = subtitles.index(item)
            show_frame(quiz_frame)
            show_question()
            
# 홈 프레임과 배경 캔버스 설정
home_frame = ttk.Frame(root)
home_canvas = tk.Canvas(home_frame, highlightthickness=0, bd=0)
home_canvas.pack(fill="both", expand=True)

# 배경 이미지 원본 로딩 후 리사이즈 (800x600 기준)
original_bg_img = Image.open("background.jpg")
resized_img = original_bg_img.resize((800, 600), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(resized_img)
home_canvas.bg_photo = bg_photo  # 참조 유지
bg_image_id = home_canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# 제목
home_title_id = home_canvas.create_text(
    400, 80,  # 고정 위치 (가운데 정렬된 가정, root width=800 기준)
    text="Language Reactor Quiz",
    font=("Segoe UI", 30, "bold"),
    fill="white",
    anchor="n"
)

# 버튼 생성
csv_btn = ttk.Button(home_canvas, text="📁 CSV 불러오기", command=load_csv, bootstyle="info-outline")
fav_btn_home = ttk.Button(home_canvas, text="🌟 즐겨찾기", command=lambda: show_frame(fav_frame), bootstyle="warning-outline")
vocab_btn = ttk.Button(home_canvas, text="📚 단어장", command=lambda: show_frame(vocab_frame), bootstyle="secondary-outline")
continue_btn = ttk.Button(home_canvas, text="▶ 문제 계속 풀기", command=go_to_question, bootstyle="success-outline")
shuffle_chk = ttk.Checkbutton(home_canvas, text="문제 순서 랜덤", variable=shuffle_enabled, bootstyle="light")
settings_btn = ttk.Button(home_canvas, text="⚙ 설정", command=lambda: show_frame(settings_frame), bootstyle="dark-outline")

# 버튼 배치 (고정된 Y 좌표로 수직 정렬)
btn_x = 400  # 중앙
start_y = 150
spacing = 50

csv_btn_id = home_canvas.create_window(btn_x, start_y + spacing * 0, window=csv_btn, anchor="n")
fav_btn_home_id = home_canvas.create_window(btn_x, start_y + spacing * 1, window=fav_btn_home, anchor="n")
vocab_btn_id = home_canvas.create_window(btn_x, start_y + spacing * 2, window=vocab_btn, anchor="n")
continue_btn_id = home_canvas.create_window(btn_x, start_y + spacing * 3, window=continue_btn, anchor="n")
shuffle_chk_id = home_canvas.create_window(btn_x, start_y + spacing * 4, window=shuffle_chk, anchor="n")
settings_btn_id = home_canvas.create_window(btn_x, start_y + spacing * 5, window=settings_btn, anchor="n")

# ✅ 자동 배경 리사이징
def resize_bg(event):
    canvas_width = event.width
    canvas_height = event.height

    resized_img = original_bg_img.resize((canvas_width, canvas_height), Image.LANCZOS)
    new_photo = ImageTk.PhotoImage(resized_img)

    home_canvas.itemconfig(bg_image_id, image=new_photo)
    home_canvas.image = new_photo  # 🔐 중요: 참조 유지 안 하면 배경 안 보임

    # 중앙 위치 재조정
    cx = canvas_width // 2
    top = 80
    spacing = 50

    home_canvas.coords(home_title_id, cx, top)
    for i, btn_id in enumerate([csv_btn_id, fav_btn_home_id, vocab_btn_id, continue_btn_id, shuffle_chk_id, settings_btn_id]):
        home_canvas.coords(btn_id, cx, top + 70 + spacing * i)

home_canvas.bind("<Configure>", resize_bg)




# 퀴즈 화면
quiz_frame = ttk.Frame(root)
back_btn = ttk.Button(quiz_frame, text="← 홈으로", command=lambda: show_frame(home_frame), style="primary.TButton")
back_btn.pack(anchor="nw", padx=10, pady=10)
center_frame = ttk.Frame(quiz_frame, padding=20) 
center_frame.place(relx=0.5, rely=0.5, anchor="center")
question_label = ttk.Label(center_frame, text="", font=FONT_MEDIUM, wraplength=700)
question_label.pack(pady=10)
entry = ttk.Entry(center_frame, font=FONT_NORMAL, width=60)
entry.pack(pady=5)
entry.bind("<Return>", lambda e: check_answer())
ttk.Button(center_frame, text="체점하기", command=check_answer, style="success.TButton").pack(pady=5)
feedback_frame = ttk.LabelFrame(center_frame, text="결과", padding=10)
feedback_frame.pack(pady=10, fill="x")
result_label = ttk.Label(center_frame, text="", font=FONT_NORMAL)
result_label.pack()
answer_label = ttk.Label(center_frame, text="", font=FONT_NORMAL, foreground="blue", wraplength=700)
answer_label.pack()
quiz_notice_label = ttk.Label(center_frame, text="", font=FONT_NORMAL, foreground="green")
quiz_notice_label.pack(pady=(0, 10))
ttk.Button(center_frame, text="정답 보기 ON/OFF", command=toggle_answer, style="warning.TButton").pack(pady=5)
fav_btn = ttk.Button(center_frame, text="☆", command=toggle_favorite, style="danger.TButton")
fav_btn.pack()
# 퀴즈 화면 내부에서 기존 keyword_box 대신
keyword_frame = ttk.Frame(center_frame)
keyword_frame.pack(pady=5)

nav_frame = ttk.Frame(quiz_frame)
nav_frame.pack(fill="x", pady=10)
ttk.Button(nav_frame, text="← 이전", command=lambda: change_question(-1), style="info.TButton").pack(side="left", padx=20)
ttk.Button(nav_frame, text="다음 →", command=lambda: change_question(1), style="info.TButton").pack(side="right", padx=20)

# 단어장 화면
vocab_frame = ttk.Frame(root)
ttk.Button(vocab_frame, text="← 홈으로", command=lambda: show_frame(home_frame), style="primary.TButton").pack(anchor="nw", padx=10, pady=10)
ttk.Label(vocab_frame, text="단어장", font=FONT_BOLD).pack(pady=10)

# 🔽 스크롤 가능한 캔버스 + 프레임 구조
vocab_scroll_canvas = tk.Canvas(vocab_frame, borderwidth=0, highlightthickness=0)
vocab_scroll_canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)

vocab_scrollbar = ttk.Scrollbar(vocab_frame, orient="vertical", command=vocab_scroll_canvas.yview)
vocab_scrollbar.pack(side="right", fill="y")

vocab_scroll_canvas.configure(yscrollcommand=vocab_scrollbar.set)

vocab_listbox_frame = ttk.Frame(vocab_scroll_canvas)
vocab_scroll_canvas.create_window((0, 0), window=vocab_listbox_frame, anchor="nw")

def on_vocab_configure(event):
    vocab_scroll_canvas.configure(scrollregion=vocab_scroll_canvas.bbox("all"))

vocab_listbox_frame.bind("<Configure>", on_vocab_configure)

# 단어 클릭 시 삭제 안내 표시용 라벨
vocab_notice_label = ttk.Label(vocab_frame, text="", font=FONT_NORMAL, foreground="green")
vocab_notice_label.pack(pady=(0, 10))


# 즐겨찾기 화면
fav_frame = ttk.Frame(root)
ttk.Button(fav_frame, text="← 홈으로", command=lambda: show_frame(home_frame), style="primary.TButton").pack(anchor="nw", padx=10, pady=10)
ttk.Label(fav_frame, text="즐겨찾기", font=FONT_BOLD).pack(pady=10)

# 🔽 스크롤 가능한 캔버스 + 프레임 구조
fav_scroll_canvas = tk.Canvas(fav_frame, borderwidth=0, highlightthickness=0)
fav_scroll_canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)

fav_scrollbar = ttk.Scrollbar(fav_frame, orient="vertical", command=fav_scroll_canvas.yview)
fav_scrollbar.pack(side="right", fill="y")

fav_scroll_canvas.configure(yscrollcommand=fav_scrollbar.set)

fav_listbox_frame = ttk.Frame(fav_scroll_canvas)
fav_scroll_canvas.create_window((0, 0), window=fav_listbox_frame, anchor="nw")

def on_fav_configure(event):
    fav_scroll_canvas.configure(scrollregion=fav_scroll_canvas.bbox("all"))

fav_listbox_frame.bind("<Configure>", on_fav_configure)


# 설정 화면
settings_frame = ttk.Frame(root)
ttk.Button(settings_frame, text="← 홈으로", command=lambda: show_frame(home_frame), style="primary.TButton").pack(anchor="nw", padx=10, pady=10)
ttk.Label(settings_frame, text="설정", font=FONT_BOLD).pack(pady=10)

ttk.Label(settings_frame, text="테마 선택", font=FONT_NORMAL).pack()
theme_menu = ttk.OptionMenu(settings_frame, theme_var, theme_var.get(), "cosmo", "flatly", "journal", "minty", "pulse", "sandstone", "solar", "superhero")
theme_menu.pack(pady=5)

ttk.Checkbutton(settings_frame, text="기본적으로 정답 보기 활성화", variable=show_answer_var).pack(pady=5)
ttk.Checkbutton(settings_frame, text="문제 순서 랜덤", variable=shuffle_enabled).pack(pady=5)


def apply_settings():
    root.style.theme_use(theme_var.get())
    show_frame(home_frame)

ttk.Button(settings_frame, text="✅ 적용하고 홈으로", command=apply_settings, style="success.TButton").pack(pady=20)

# 단축키
root.bind("<Left>", lambda e: change_question(-1))
root.bind("<Right>", lambda e: change_question(1))

show_frame(home_frame)
root.mainloop()
