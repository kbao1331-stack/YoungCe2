import requests
import json
import time
import threading
import re
import os
import math

def rainbow_text(text, offset=0, intensity=0.95):
    """
    Rainbow gradient siêu mượt bằng sin wave - màu chuyển tiếp tự nhiên
    """
    result = ""
    t = time.time() * 3.5 + offset   # tốc độ chạy ngang nhanh vừa phải
    for i, char in enumerate(text):
        phase = (i * 0.18 + t) % (math.pi * 2)
        r = int((math.sin(phase)          * 127 + 128) * intensity)
        g = int((math.sin(phase + 2.1)    * 127 + 128) * intensity)
        b = int((math.sin(phase + 4.2)    * 127 + 128) * intensity)
        result += f"\033[38;2;{r};{g};{b}m{char}"
    result += "\033[0m"
    return result

def print_rainbow_banner(offset=0):
    lines = [
        "┌──────────────────────── Info ───────────────────────┐",
        " ➜ Admin: YOUNGCE",
        " ➜ Box: AE HẮC LINH",
        " ➜ CHỨC NĂNG: NHÂY NGÔN RÉO TÊN VÔ HẠN 💥🔥",
        "└─────────────────────────────────────────────────────┘",
    ]
    for line in lines:
        print(rainbow_text(line, offset=offset, intensity=0.92))

def animate_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    for i in range(70):
        print_rainbow_banner(offset=i * 0.35)
        time.sleep(0.045)
    os.system('clear' if os.name == 'posix' else 'cls')
    print_rainbow_banner(offset=24)

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
            for url in ['https://www.facebook.com', 'https://m.facebook.com']:
                response = requests.get(url, headers=headers, timeout=10)
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
                                   data=data, headers=headers, timeout=7)
            return response.status_code in (200, 204)
        except:
            return False

# Biến điều khiển
stop_flag = False
current_delay = 0.4   # mặc định nhỏ hơn để chạy nhanh hơn

def nhay_ngon_loop(messengers, recipient_id, name_to_call, lines):
    global stop_flag, current_delay
    counter = 0
    while not stop_flag:
        counter += 1
        for line in lines:
            if stop_flag: return
            formatted_message = line.replace("{chon_name}", name_to_call)
            
            for messenger in messengers:
                if stop_flag: return
                success = messenger.send_message(recipient_id, formatted_message)
                status = "OK" if success else "X"
                ts = time.strftime("%H:%M:%S")
                preview = formatted_message[:35].replace("\n", " ") + "..." if len(formatted_message) > 35 else formatted_message
                
                status_line = f"[{status}] {ts} | Box: {recipient_id} | Réo: {name_to_call} | Lần: {counter} | Delay: {current_delay:.2f}s | {preview}"
                print(f"\r{rainbow_text(status_line, offset=time.time()*5, intensity=0.93)}", end="")
                
                # sleep chia nhỏ để CPU nhẹ + phản hồi lệnh nhanh
                remaining = current_delay
                while remaining > 0 and not stop_flag:
                    step = min(0.08, remaining)
                    time.sleep(step)
                    remaining -= step

def main():
    global stop_flag, current_delay
    os.system('clear' if os.name == 'posix' else 'cls')
    animate_banner()

    cookies = []
    print(rainbow_text("Nhập cookie (Enter trống hoặc 'done' để kết thúc):", intensity=0.85))
    while True:
        c = input(rainbow_text("> ", intensity=0.75)).strip()
        if not c or c.lower() == 'done': break
        cookies.append(c)

    messengers = []
    for i, cookie in enumerate(cookies, 1):
        try:
            m = Messenger(cookie)
            messengers.append(m)
            print(rainbow_text(f"Cookie {i}: OK - User ID: {m.user_id}", intensity=0.9))
        except Exception as e:
            print(rainbow_text(f"Cookie {i}: LỖI - {e}", intensity=0.7))

    if not messengers:
        print(rainbow_text("Không có cookie hợp lệ."))
        return

    id_box = input(rainbow_text("\nNhập ID Box Messenger: ", intensity=0.85)).strip()
    name_to_call = input(rainbow_text("Nhập Họ/Tên người cần réo: ", intensity=0.85)).strip()
    
    try:
        current_delay = float(input(rainbow_text("\nNhập Delay (giây, mặc định 0.4): ", intensity=0.85) or "0.4"))
        if current_delay < 0.08:
            current_delay = 0.08
    except:
        current_delay = 0.4

    try:
        with open("nhay1.txt", "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        if not lines:
            print(rainbow_text("File nhay1.txt không có nội dung!"))
            return
        print(rainbow_text(f"Đã load {len(lines)} dòng ngôn từ nhay1.txt", intensity=0.9))
    except FileNotFoundError:
        print(rainbow_text("Không tìm thấy file nhay1.txt!"))
        return

    print(rainbow_text(f"\n💥 BẮT ĐẦU NHÂY RÉO {name_to_call.upper()} VÔ HẠN 🔥🌈", intensity=1.0))
    print(rainbow_text("➜ 's' = dừng | 'c' = đổi delay"))

    thread = threading.Thread(target=nhay_ngon_loop, args=(messengers, id_box, name_to_call, lines))
    thread.daemon = True
    thread.start()

    while True:
        cmd = input().strip().lower()
        if cmd == 's':
            stop_flag = True
            print(rainbow_text("\n[!] ĐANG DỪNG... chờ thread kết thúc", intensity=0.9))
            break
        elif cmd == 'c':
            try:
                new_d = float(input(rainbow_text("Delay mới (giây): ", intensity=0.85)))
                if new_d < 0.08: new_d = 0.08
                current_delay = new_d
                print(rainbow_text(f"[OK] Delay mới: {current_delay:.2f}s", intensity=0.95))
            except:
                print(rainbow_text("[Lỗi] Nhập số hợp lệ bro", intensity=0.7))

    print(rainbow_text("Tool đã dừng. Chạy lại khi cần réo tiếp nhé! 🌈"))
    time.sleep(1.2)

if __name__ == "__main__":
    main()