import cv2
import tkinter as tk
from PIL import Image, ImageTk
import threading
import time
import queue
from vm_logic import process

# ─── Tkinter setup ─────────────────────────────────────────────────
root = tk.Tk()
root.title("Virtual Mouse")
root.configure(bg="#1e1e2e")
root.resizable(False, False)

BG     = "#1e1e2e"
PANEL  = "#2a2a3e"
ACCENT = "#a855f7"
TEXT   = "#e2e8f0"
DIM    = "#64748b"
GREEN  = "#22c55e"
RED    = "#ef4444"
YELLOW = "#facc15"

FONT_TITLE  = ("Consolas", 12, "bold")
FONT_BOLD   = ("Consolas", 10, "bold")
FONT_NORMAL = ("Consolas", 9)

# ─── Layout ────────────────────────────────────────────────────────
frame_left = tk.Frame(root, bg=BG)
frame_left.pack(side=tk.LEFT, padx=8, pady=8)

frame_right = tk.Frame(root, bg=PANEL, width=200)
frame_right.pack(side=tk.RIGHT, fill=tk.Y, padx=(0,8), pady=8)
frame_right.pack_propagate(False)

# Canvas webcam
canvas = tk.Canvas(frame_left, width=480, height=360,
                   bg="black", highlightthickness=0)
canvas.pack()
# ─── Panel phải ────────────────────────────────────────────────────
tk.Label(frame_right, text="VIRTUAL MOUSE",
         font=FONT_TITLE, bg=PANEL, fg=ACCENT).pack(pady=(14,4))
tk.Frame(frame_right, bg=ACCENT, height=1).pack(fill=tk.X, padx=12)

# FPS
fps_frame = tk.Frame(frame_right, bg=PANEL)
fps_frame.pack(fill=tk.X, padx=14, pady=6)
tk.Label(fps_frame, text="FPS", font=FONT_NORMAL,
         bg=PANEL, fg=DIM, width=8, anchor="w").pack(side=tk.LEFT)
fps_var = tk.StringVar(value="--")
tk.Label(fps_frame, textvariable=fps_var,
         font=FONT_BOLD, bg=PANEL, fg=GREEN).pack(side=tk.LEFT)

tk.Frame(frame_right, bg="#3f3f5a", height=1).pack(fill=tk.X, padx=12, pady=4)

# Hàm tạo row tọa độ
def make_coord_row(parent, label, bold=False):
    font  = FONT_BOLD   if bold else FONT_NORMAL
    color = TEXT        if bold else DIM
    tk.Label(parent, text=label, font=font,
             bg=PANEL, fg=ACCENT if bold else DIM).pack(padx=14, anchor="w", pady=(6,1))
    xf = tk.Frame(parent, bg=PANEL); xf.pack(fill=tk.X, padx=20, pady=1)
    tk.Label(xf, text="X:", font=font, bg=PANEL,
             fg=color, width=3, anchor="w").pack(side=tk.LEFT)
    xv = tk.StringVar(value="--")
    tk.Label(xf, textvariable=xv, font=font, bg=PANEL, fg=color).pack(side=tk.LEFT)

    yf = tk.Frame(parent, bg=PANEL); yf.pack(fill=tk.X, padx=20, pady=1)
    tk.Label(yf, text="Y:", font=font, bg=PANEL,
             fg=color, width=3, anchor="w").pack(side=tk.LEFT)
    yv = tk.StringVar(value="--")
    tk.Label(yf, textvariable=yv, font=font, bg=PANEL, fg=color).pack(side=tk.LEFT)
    return xv, yv

# Ngón cái + trỏ (bold)
cai_x, cai_y = make_coord_row(frame_right, "NGÓN CÁI", bold=True)
tro_x, tro_y = make_coord_row(frame_right, "NGÓN TRỎ", bold=True)

tk.Frame(frame_right, bg="#3f3f5a", height=1).pack(fill=tk.X, padx=12, pady=4)

# Mode
tk.Label(frame_right, text="MODE", font=FONT_NORMAL,
         bg=PANEL, fg=DIM).pack(padx=14, anchor="w", pady=(4,1))
mode_var   = tk.StringVar(value="WAITING")
mode_label = tk.Label(frame_right, textvariable=mode_var,
                      font=FONT_BOLD, bg=PANEL, fg=YELLOW)
mode_label.pack(padx=14, anchor="w")

# Dist
tk.Frame(frame_right, bg="#3f3f5a", height=1).pack(fill=tk.X, padx=12, pady=4)
dist_frame = tk.Frame(frame_right, bg=PANEL)
dist_frame.pack(fill=tk.X, padx=14, pady=2)
tk.Label(dist_frame, text="DIST:", font=FONT_NORMAL,
         bg=PANEL, fg=DIM, width=6, anchor="w").pack(side=tk.LEFT)
dist_var = tk.StringVar(value="--")
tk.Label(dist_frame, textvariable=dist_var,
         font=FONT_NORMAL, bg=PANEL, fg=DIM).pack(side=tk.LEFT)

# ─── Queue truyền frame từ thread → main thread ────────────────────
frame_queue = queue.Queue(maxsize=1)
running     = True
prev_time   = time.time()

# ─── Thread webcam ─────────────────────────────────────────────────
def update():
    global prev_time, running

    vcap = cv2.VideoCapture(0)
    while running:
        ret, frame = vcap.read()
        if not ret: break

        frame = cv2.flip(frame, 1)

        # FPS
        now       = time.time()
        fps_val   = 1 / (now - prev_time + 1e-9)
        prev_time = now
        fps_var.set(f"{fps_val:.1f}")

        # Gọi logic
        frame, data = process(frame)

        # Đẩy vào queue
        if not frame_queue.full():
            frame_queue.put((frame, data))

    vcap.release()

# ─── Cập nhật UI từ main thread ────────────────────────────────────
COLORS = {
    "LEFT CLICK":  RED,
    "RIGHT CLICK": "#f97316",
    "SCROLL UP":   GREEN,
    "SCROLL DOWN": "#3b82f6",
    "MOVING":      GREEN,
    "WAITING":     YELLOW,
}

def refresh_ui():
    if not frame_queue.empty():
        frame, data = frame_queue.get()

        # Cập nhật panel
        if data["found"]:
            cai_x.set(str(data["lm4x"]))
            cai_y.set(str(data["lm4y"]))
            tro_x.set(str(data["lm8x"]))
            tro_y.set(str(data["lm8y"]))
            dist_var.set(f"{data['dist']} px")
            mode_var.set(data["mode"])
            mode_label.config(fg=COLORS.get(data["mode"], YELLOW))
        else:
            mode_var.set("WAITING")
            mode_label.config(fg=YELLOW)

        # Cập nhật canvas
        frame_rgb   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_small = cv2.resize(frame_rgb, (480, 360))
        img         = Image.fromarray(frame_small)
        imgtk       = ImageTk.PhotoImage(image=img)
        canvas.imgtk = imgtk
        canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)

    root.after(15, refresh_ui)  # gọi lại sau 15ms

# ─── Đóng chương trình ─────────────────────────────────────────────
def on_close():
    global running
    running = False
    root.destroy()

def on_key(event):
    if event.char == "q":
        on_close()

# ─── Cố định góc phải trên màn hình ───────────────────────────────
root.update_idletasks()
screen_w = root.winfo_screenwidth()
win_w    = root.winfo_width()
root.geometry(f"+{screen_w - win_w - 10}+10")
root.attributes("-topmost", True)

# ─── Bind sự kiện ──────────────────────────────────────────────────
root.protocol("WM_DELETE_WINDOW", on_close)
root.bind("<Key>", on_key)

# ─── Khởi động ─────────────────────────────────────────────────────
t = threading.Thread(target=update, daemon=True)
t.start()

refresh_ui()       # ✅ bắt đầu vòng lặp UI từ main thread
root.mainloop()