import requests
import json
import time
import threading
import re
import os
from bs4 import BeautifulSoup

def rainbow_text(text, offset=0, speed_factor=1):
    """Rainbow chạy ngang nhanh hơn"""
    colors = [
        (255, 0, 0), (255, 140, 0), (255, 215, 0), (0, 255, 0),
        (0, 255, 200), (0, 150, 255), (138, 43, 226), (255, 20, 147)
    ]
    result = ""
    for i, char in enumerate(text):
        idx = (i + offset * 2) % len(colors)  # *2 để chạy nhanh hơn
        r, g, b = colors[idx]
        result += f"\033[38;2;{r};{g};{b}m{char}"
    result += "\033[0m"
    return result

def print_rainbow_banner(offset=0):
    lines = [
        "┌──────────────────────── Info ───────────────────────┐",
        " ➜ Admin: YOUNGCE",
        " ➜ Box: AE HẮC LINH",
        " ➜ CHỨC NĂNG: SPAM BOX MESSENGER VÔ HẠN 💥",
        "└─────────────────────────────────────────────────────┘",
    ]
    for line in lines:
        print(rainbow_text(line, offset=offset))

def animate_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    for i in range(50):  # Chạy nhanh hơn, nhiều frame hơn
        print_rainbow_banner(offset=i)
        time.sleep(0.04)   # Tốc độ nhanh gấp đôi
    os.system('clear' if os.name == 'posix' else 'cls')
    print_rainbow_banner(offset=25)

# ────────────────────────────────────────────────

class Messenger:
    def __init__(self, cookie):
        self.cookie = cookie
        self.user_id = self.get_user_id()
        self.fb_dtsg = None
        self.init_params()

    def get_user_id(self):
        try:
            return re.search(r"c_user=(\d+)", self.cookie).group(1)
        except:
            raise Exception("Cookie không hợp lệ")

    def init_params(self):
        headers = {'Cookie': self.cookie, 'User-Agent': 'Mozilla/5.0'}
        try:
            for url in ['https://www.facebook.com', 'https://mbasic.facebook.com', 'https://m.facebook.com']:
                response = requests.get(url, headers=headers, timeout=8)
                match = re.search(r'name="fb_dtsg" value="(.*?)"', response.text)
                if match:
                    self.fb_dtsg = match.group(1)
                    return
            raise Exception("Không tìm thấy fb_dtsg")
        except Exception as e:
            raise Exception(f"Lỗi khởi tạo: {str(e)}")

    def send_message(self, recipient_id, message):
        timestamp = int(time.time() * 1000)
        data = {
            'fb_dtsg': self.fb_dtsg,
            '__user': self.user_id,
            'body': message,
            'action_type': 'ma-type:user-generated-message',
            'timestamp': timestamp,
            'offline_threading_id': str(timestamp),
            'message_id': str(timestamp),
            'thread_fbid': recipient_id,
            'source': 'source:chat:web',
            'client': 'mercury'
        }
        headers = {
            'Cookie': self.cookie,
            'User-Agent': 'Mozilla/5.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        try:
            response = requests.post('https://www.facebook.com/messaging/send/', 
                                   data=data, headers=headers, timeout=6)
            return response.status_code in (200, 204)
        except:
            return False

# Biến toàn cục
stop_flag = False
current_delay = 0.3   # ← Giảm delay mặc định để chạy NHANH

def send_messages_loop(messengers, recipient_ids, messages_list):
    global stop_flag, current_delay
    counter = 0
    while not stop_flag:
        counter += 1
        for recipient_id in recipient_ids:
            if stop_flag: return
            for messenger in messengers:
                if stop_flag: return
                for message in messages_list:
                    if stop_flag: return
                    success = messenger.send_message(recipient_id, message)
                    status = "OK" if success else "X"
                    # In status nhanh, rainbow nhẹ
                    ts = time.strftime("%H:%M:%S")
                    print(f"\r{rainbow_text(f'[{status}] {ts} | Box: {recipient_id} | Lần: {counter} | Delay: {current_delay:.2f}s', offset=int(time.time()*5))}", end="")
                    time.sleep(current_delay)

def main():
    global stop_flag, current_delay
    os.system('clear' if os.name == 'posix' else 'cls')
    animate_banner()  # Banner chạy nhanh

    recipient_ids = []
    print(rainbow_text("Nhập ID box (Enter trống hoặc 'done' để xong):"))
    while True:
        rid = input(rainbow_text("> ")).strip()
        if not rid or rid.lower() == 'done': break
        recipient_ids.append(rid)

    cookies = []
    print(rainbow_text("\nNhập cookie (Enter trống hoặc 'done' để xong):"))
    while True:
        c = input(rainbow_text("> ")).strip()
        if not c or c.lower() == 'done': break
        cookies.append(c)

    messages_list = []
    print(rainbow_text("\nNhập file ngôn (VD: ngon.txt) (Enter trống hoặc 'done'):"))
    while True:
        fn = input(rainbow_text("> ")).strip()
        if not fn or fn.lower() == 'done': break
        try:
            with open(fn, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    messages_list.append(content)
                    print(rainbow_text(f"Đã load: {fn} ({len(content)} ký tự)"))
        except:
            print(rainbow_text(f"File {fn} lỗi hoặc không tồn tại"))

    messengers = []
    for i, cookie in enumerate(cookies, 1):
        try:
            m = Messenger(cookie)
            messengers.append(m)
            print(rainbow_text(f"Cookie {i}: OK | ID: {m.user_id}"))
        except Exception as e:
            print(rainbow_text(f"Cookie {i}: LỖI → {e}"))

    if not messengers or not messages_list or not recipient_ids:
        print(rainbow_text("Thiếu cookie / ngôn / box → thoát"))
        return

    try:
        current_delay = float(input(rainbow_text("\nDelay mỗi tin (giây, mặc định 0.3): ") or "0.3"))
        if current_delay < 0.1:
            current_delay = 0.1  # tránh quá nhanh gây block
    except:
        current_delay = 0.3

    print(rainbow_text("\n💥 SPAM VÔ HẠN BẮT ĐẦU – By YOUNGCE 🔥"))
    print(rainbow_text("➜ 's' = dừng | 'c' = đổi delay"))

    thread = threading.Thread(target=send_messages_loop, args=(messengers, recipient_ids, messages_list))
    thread.daemon = True
    thread.start()

    while True:
        cmd = input().strip().lower()
        if cmd == 's':
            stop_flag = True
            print(rainbow_text("\n[!] ĐANG DỪNG... chờ thread kết thúc"))
            break
        elif cmd == 'c':
            try:
                new_d = float(input(rainbow_text("Delay mới (giây): ")))
                if new_d < 0.1: new_d = 0.1
                current_delay = new_d
                print(rainbow_text(f"[OK] Delay mới: {current_delay:.2f}s"))
            except:
                print(rainbow_text("[Lỗi] Nhập số hợp lệ"))

    print(rainbow_text("Chương trình đã dừng."))
    time.sleep(1.2)

if __name__ == "__main__":
    main()