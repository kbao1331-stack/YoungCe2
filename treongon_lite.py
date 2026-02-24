import discord
from discord.ext import commands
import threading
import asyncio
import time
import re
import os
import requests
import sys
from datetime import datetime
# Chỉ giữ lại module treo_mqtt theo yêu cầu
from module.treomqtt import * # --- Biến toàn cục để điều khiển trạng thái ---
running_status = True
current_delay = 1.0

def rainbow_text(text, offset=0):
    colors = [
        (255, 0, 0), (255, 140, 0), (255, 215, 0), (0, 255, 0),
        (0, 255, 200), (0, 150, 255), (138, 43, 226), (255, 20, 147)
    ]
    result = ""
    for i, char in enumerate(text):
        idx = (i + offset * 2) % len(colors)
        r, g, b = colors[idx]
        result += f"\033[38;2;{r};{g};{b}m{char}"
    result += "\033[0m"
    return result

def print_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    banner = [
        "┌─────────────────────────────────────────────────────┐",
        "│            TOOL TREO MQTT - MULTI COOKIE            │",
        "│        Lệnh: 's' để DỪNG | 'd' để ĐỔI DELAY         │",
        "└─────────────────────────────────────────────────────┘",
    ]
    for i, line in enumerate(banner):
        print(rainbow_text(line, offset=i))

# --- Luồng lắng nghe lệnh điều khiển ---
def listen_for_commands():
    global running_status, current_delay
    while running_status:
        cmd = input().lower().strip()
        if cmd == 's':
            print(rainbow_text("\n[!] Đang dừng tất cả tiến trình..."))
            running_status = False
            os._exit(0) # Thoát toàn bộ chương trình ngay lập tức
        elif cmd == 'd':
            try:
                new_delay = float(input(rainbow_text("Nhập Delay mới (giây): ")))
                current_delay = new_delay
                print(rainbow_text(f"[OK] Đã cập nhật Delay thành: {current_delay}s"))
            except ValueError:
                print(rainbow_text("[Lỗi] Vui lòng nhập số hợp lệ!"))

# --- Hàm xử lý Treo MQTT ---
def start_treo_task(cookie: str, thread_id: str, message_content: str, folder_name: str):
    global running_status, current_delay
    try:
        clean_thread_id = re.sub(r'[^\d]', '', thread_id)
        if not clean_thread_id:
            return
        
        sender = FacebookMQTTSender(cookie, f"Task_{folder_name}")
        sender.connect()
        
        print(rainbow_text(f"[OK] Đã kết nối MQTT cho Cookie: {cookie[:15]}..."))
        
        while running_status:
            current_time = datetime.now().strftime("%H:%M:%S")
            try:
                sender.send_message(message_content, clean_thread_id)
                # 1|2|3|4 -> THÀNH CÔNG | THỜI GIAN | ID BOX | DELAY
                print(rainbow_text(f"SUCCESS | {current_time} | {clean_thread_id} | {current_delay}s"))
            except Exception:
                print(rainbow_text(f"FAILED  | {current_time} | {clean_thread_id} | {current_delay}s"))
            
            # Nghỉ theo delay hiện tại (cho phép thay đổi delay ngay lập tức)
            time.sleep(current_delay)
            
    except Exception as e:
        print(rainbow_text(f"[LỖI] {str(e)}"))

def main():
    global current_delay
    print_banner()

    # 1. Nhập Đa Cookie
    cookies = []
    print(rainbow_text("\nNhập danh sách Cookie (Nhập 'done' để dừng):"))
    while True:
        ck = input(rainbow_text("> ")).strip()
        if ck.lower() == 'done' or not ck:
            break
        cookies.append(ck)

    if not cookies: return

    # 2. Nhập ID Box
    thread_id = input(rainbow_text("\nNhập ID Box: ")).strip()

    # 3. Nhập File nội dung
    message_content = ""
    while not message_content:
        file_path = input(rainbow_text("\nNhập đường dẫn file (VD: ngon.txt): ")).strip()
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                message_content = f.read().strip()
        except FileNotFoundError:
            print(rainbow_text("[X] Không thấy file!"))

    # 4. Nhập Delay ban đầu
    try:
        current_delay = float(input(rainbow_text("\nNhập delay ban đầu (giây): ")) or 1.0)
    except ValueError:
        current_delay = 1.0

    # Khởi chạy luồng lắng nghe lệnh (Input Listener)
    cmd_thread = threading.Thread(target=listen_for_commands)
    cmd_thread.daemon = True
    cmd_thread.start()

    print(rainbow_text("\n" + "="*50))
    print(rainbow_text("🚀 ĐANG CHẠY... GÕ 's' ĐỂ DỪNG, 'd' ĐỂ ĐỔI DELAY"))
    print(rainbow_text("="*50 + "\n"))

    # Khởi chạy đa luồng cho cookie
    for i, cookie in enumerate(cookies):
        t = threading.Thread(
            target=start_treo_task, 
            args=(cookie, thread_id, message_content, f"User_{i}")
        )
        t.daemon = True
        t.start()

    # Giữ chương trình chạy chính
    while running_status:
        time.sleep(0.5)

if __name__ == "__main__":
    main()
