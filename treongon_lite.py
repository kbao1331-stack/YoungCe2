import discord
from discord.ext import commands
import threading
import asyncio
import time
import re
import os
import requests
from datetime import datetime  # Thêm thư viện để lấy thời gian
# Chỉ giữ lại module treo_mqtt theo yêu cầu
from module.treomqtt import * # --- Giao diện Banner & Màu sắc ---
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
        "│                ADMIN: YOUNGCE                       │",
        "└─────────────────────────────────────────────────────┘",
    ]
    for i, line in enumerate(banner):
        print(rainbow_text(line, offset=i))

# --- Hàm xử lý Treo MQTT ---
def start_treo_task(cookie: str, thread_id: str, message_content: str, delay: float, folder_name: str):
    try:
        # Lọc chỉ lấy số từ thread_id
        clean_thread_id = re.sub(r'[^\d]', '', thread_id)
        if not clean_thread_id:
            return
        
        # Khởi tạo sender từ module.treomqtt
        sender = FacebookMQTTSender(cookie, f"Task_{folder_name}")
        sender.connect()
        
        print(rainbow_text(f"[OK] Đã kết nối MQTT cho Cookie: {cookie[:15]}..."))
        
        while True:
            # Lấy thời gian hiện tại định dạng Giờ:Phút:Giây
            current_time = datetime.now().strftime("%H:%M:%S")
            try:
                # Gửi tin nhắn thông qua hàm của module
                sender.send_message(message_content, clean_thread_id)
                
                # Định dạng thông báo: THÀNH CÔNG | THỜI GIAN | ID BOX | DELAY
                status_msg = f"THÀNH CÔNG | {current_time} | {clean_thread_id} | {delay}s"
                print(rainbow_text(status_msg))
                
                time.sleep(delay)
            except Exception as e:
                # Định dạng thông báo khi THẤT BẠI
                error_msg = f"THẤT BẠI | {current_time} | {clean_thread_id} | {delay}s"
                print(rainbow_text(error_msg))
                
                time.sleep(delay)
                continue
    except Exception as e:
        print(rainbow_text(f"[LỖI HỆ THỐNG] {str(e)}"))

# --- Luồng chính điều khiển Input ---
def main():
    print_banner()

    # 1. Nhập Đa Cookie
    cookies = []
    print(rainbow_text("\nNhập danh sách Cookie (Nhập 'done' để dừng):"))
    while True:
        ck = input(rainbow_text("> ")).strip()
        if ck.lower() == 'done' or not ck:
            break
        cookies.append(ck)

    if not cookies:
        print(rainbow_text("[!] Danh sách cookie trống. Thoát..."))
        return

    # 2. Nhập ID Box (thread_id)
    thread_id = input(rainbow_text("\nNhập ID Box (thread_id): ")).strip()

    # 3. Nhập File ngôn (message_content)
    message_content = ""
    while not message_content:
        file_path = input(rainbow_text("\nNhập đường dẫn file nội dung (VD: ngon.txt): ")).strip()
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                message_content = f.read().strip()
                print(rainbow_text(f"[OK] Đã tải nội dung từ file: {file_path}"))
        except FileNotFoundError:
            print(rainbow_text("[X] Không tìm thấy file, vui lòng nhập lại!"))

    # 4. Nhập Delay
    try:
        delay_input = input(rainbow_text("\nNhập delay (giây) [Mặc định 1.0]: ")).strip()
        delay = float(delay_input) if delay_input else 1.0
    except ValueError:
        delay = 1.0

    print(rainbow_text("\n" + "="*50))
    print(rainbow_text("🚀 BẮT ĐẦU TIẾN TRÌNH TREO MQTT..."))
    print(rainbow_text("="*50 + "\n"))

    # Khởi chạy đa luồng cho từng cookie
    threads = []
    for i, cookie in enumerate(cookies):
        t = threading.Thread(
            target=start_treo_task, 
            args=(cookie, thread_id, message_content, delay, f"User_{i}")
        )
        t.daemon = True
        t.start()
        threads.append(t)

    # Giữ chương trình chạy
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(rainbow_text("\n[!] Đang dừng chương trình..."))

if __name__ == "__main__":
    main()
