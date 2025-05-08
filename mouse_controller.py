import ctypes
import threading
import time
import json
import os
from pynput import mouse, keyboard
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import math

PROFILES_FILE = "profiles.json"
ACTIVE_FILE = "active_profile.txt"
enabled = False
left_click_held = False
click_start_time = None
cached_profile = {"x": 0.0, "y": 0.0, "interval": 0.01, "accel_x": 0.5, "accel_y": 0.5}
active_profile_name = None
scaleval = 0.05

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = [("mi", MOUSEINPUT)]
    _fields_ = [("type", ctypes.c_ulong), ("ii", _INPUT)]

INPUT_MOUSE = 0
MOUSEEVENTF_MOVE = 0x0001

def move_mouse(dx, dy):
    extra = ctypes.c_ulong(0)
    mi = MOUSEINPUT(dx, dy, 0, MOUSEEVENTF_MOVE, 0, ctypes.pointer(extra))
    inp = INPUT(INPUT_MOUSE, INPUT._INPUT(mi))
    ctypes.windll.user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))

def load_profile():
    global cached_profile, active_profile_name
    if not os.path.exists(PROFILES_FILE) or not os.path.exists(ACTIVE_FILE):
        return
    try:
        with open(ACTIVE_FILE) as f:
            name = f.read().strip()
        with open(PROFILES_FILE) as f:
            profiles = json.load(f)
        if name in profiles:
            cached_profile = {
                "x": float(profiles[name]["x"]),
                "y": float(profiles[name]["y"]),
                "interval": float(profiles[name].get("interval", 0.01)),
                "accel_x": float(profiles[name].get("accel_x", 0.5)),
                "accel_y": float(profiles[name].get("accel_y", 0.5))
            }
            active_profile_name = name
            print(f"[INFO] Profile loaded: {name}")
        else:
            print(f"[WARNING] Profile '{name}' not found")
    except Exception as e:
        print(f"[ERROR] Failed to load profile: {e}")

class ProfileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(PROFILES_FILE) or event.src_path.endswith(ACTIVE_FILE):
            load_profile()

def move_continuous(speed_x, speed_y, interval):
    if not (left_click_held and enabled):
        return

    hold_time = time.time() - click_start_time if click_start_time else 0
    factor_x = min(3.0, 1.0 + hold_time * cached_profile.get("accel_x", 0.5))
    factor_y = min(3.0, 1.0 + hold_time * cached_profile.get("accel_y", 0.5))

    dx = round(speed_x * scaleval * factor_x)
    dy = round(speed_y * scaleval * factor_y)

    move_mouse(dx, dy)
    time.sleep(interval)

def mouse_mover():
    while True:
        if enabled and left_click_held:
            move_continuous(cached_profile["x"], cached_profile["y"], cached_profile["interval"])
        else:
            time.sleep(0.01)

def on_click(x, y, button, pressed):
    global left_click_held, click_start_time
    if button == mouse.Button.left:
        left_click_held = pressed
        click_start_time = time.time() if pressed else None

def on_press(key):
    global enabled
    try:
        if key.char == 'g':
            enabled = not enabled
            print(f"[INFO] Script {'ENABLED' if enabled else 'DISABLED'}")
    except AttributeError:
        pass

if __name__ == "__main__":
    load_profile()

    observer = Observer()
    handler = ProfileChangeHandler()
    observer.schedule(handler, ".", recursive=False)
    observer.start()

    threading.Thread(target=mouse_mover, daemon=True).start()
    mouse.Listener(on_click=on_click).start()
    keyboard.Listener(on_press=on_press).start()

    print("[INFO] Raw input mover started. Press 'g' to toggle.")
    print("[INFO] Hold left mouse button to activate movement.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
