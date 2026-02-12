import requests
import json
import time
import threading
import re
import os
import random
import math  # Để tính sin cho gradient mượt

def rainbow_text(text, offset=0, intensity=1.0):
    """
    Rainbow gradient siêu mượt: dùng sin wave để màu chuyển tiếp tự nhiên
    intensity: độ "rực" (0.0 -> 1.0)
    """
    result = ""
    t = time.time() * 3 + offset  # Tốc độ chạy ngang \~3x/giây
    for i, char in enumerate(text):
        # Tính phase cho mỗi ký tự → tạo hiệu ứng sóng
        phase = (i * 0.15 + t) % (math.pi * 2)
        r = int((math.sin(phase) * 127 + 128) * intensity)
        g = int((math.sin(phase + 2) * 127 + 128) * intensity)
        b = int((math.sin(phase + 4) * 127 + 128) * intensity)
        result += f"\033[38;2;{r};{g};{b}m{char}"
    result += "\033[0m"
    return result

def print_rainbow_banner(offset=0):
    lines = [
        "┌──────────────────────── Info ───────────────────────┐",
        " ➜ Admin: YOUNGCE",
        " ➜ Box: AE HẮC LINH",
        " ➜ CHỨC NĂNG: NHÂY TAG VÔ HẠN 💥🔥",
        "└─────────────────────────────────────────────────────┘",
    ]
    for line in lines:
        print(rainbow_text(line, offset=offset, intensity=0.9))

def animate_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    for i in range(80):  # Animation dài hơn, mượt hơn
        print_rainbow_banner(offset=i * 0.3)  # Chạy chậm rãi, đẹp mắt
        time.sleep(0.05)
    os.system('clear' if os.name == 'posix' else 'cls')
    print_rainbow_banner(offset=24)  # Giữ frame đẹp nhất

class Messenger:
    def __init__(self, cookie):
        self.cookie = cookie
        self.user_id = self.get_user_id()
        self.fb_dtsg = ""
        self.jazoest = ""
        self.init_params()

    def get_user_id(self):
        try:
            return re.search(r"c_user=(\d+)", self.cookie).group(1)
        except:
            raise Exception("Cookie không hợp lệ")

    def init_params(self):
        headers = {'Cookie': self.cookie, 'User-Agent': 'Mozilla/5.0'}
        try:
            response = requests.get('https://m.facebook.com', headers=headers, timeout=8)
            self.fb_dtsg = re.search(r'name="fb_dtsg" value="(.*?)"', response.text).group(1)
            self.jazoest = re.search(r'name="jazoest" value="(.*?)"', response.text).group(1)
        except:
            raise Exception("Không thể lấy fb_dtsg. Kiểm tra lại cookie!")

    def send_tag_message(self, recipient_id, tag_uid, tag_name, message):
        body = f"@{tag_name} {message}"
        timestamp = int(time.time() * 1000)
        
        data = {
            'fb_dtsg': self.fb_dtsg,
            'jazoest': self.jazoest,
            'body': body,
            'action_type': 'ma-type:user-generated-message',
            'timestamp': timestamp,
            'offline_threading_id': str(timestamp),
            'message_id': str(timestamp),
            'thread_fbid': recipient_id,
            'source': 'source:chat:web',
            'client': 'mercury',
            'profile_xmd[0][id]': tag_uid,
            'profile_xmd[0][length]': len(tag_name) + 1,
            'profile_xmd[0][offset]': 0,
            'profile_xmd[0][type]': 'p',
        }
        
        headers = {
            'Cookie': self.cookie,
            'User-Agent': 'Mozilla/5.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        try:
            res = requests.post('https://www.facebook.com/messaging/send/', data=data, headers=headers, timeout=6)
            return res.status_code == 200
        except:
            return False

# Biến điều khiển
stop_flag = False
current_delay = 0.3

def nhay_tag_loop(messengers, id_box, target_uids, nhay_lines):
    global stop_flag, current_delay
    
    tag_list = [(uid, f"Người dùng {uid}") for uid in target_uids]
    
    counter = 0
    while not stop_flag:
        counter += 1
        for line in nhay_lines:
            if stop_flag: return
            for messenger in messengers:
                if stop_flag: return
                for uid, name in tag_list:
                    if stop_flag: return
                    
                    success = messenger.send_tag_message(id_box, uid, name, line)
                    status = "OK" if success else "X"
                    ts = time.strftime("%H:%M:%S")
                    
                    # Rainbow động theo thời gian thực
                    status_text = f"[{status}] {ts} | Tag: {uid} | Box: {id_box} | Lần: {counter} | Delay: {current_delay:.2f}s"
                    print(f"\r{rainbow_text(status_text, offset=time.time()*4, intensity=0.95)}", end="")
                    
                    # Sleep chia nhỏ để nhẹ CPU
                    remaining = current_delay
                    while remaining > 0 and not stop_flag:
                        sleep_step = min(0.08, remaining)
                        time.sleep(sleep_step)
                        remaining -= sleep_step

def main():
    global stop_flag, current_delay
    os.system('clear' if os.name == 'posix' else 'cls')
    animate_banner()

    cookies_input = []
    print(rainbow_text("Nhập cookie (Enter trống hoặc 'done' để xong):", intensity=0.8))
    while True:
        c = input(rainbow_text("> ", intensity=0.7)).strip()
        if not c or c.lower() == 'done': break
        cookies_input.append(c)

    messengers = []
    for i, ck in enumerate(cookies_input, 1):
        try:
            m = Messenger(ck)
            messengers.append(m)
            print(rainbow_text(f"Cookie {i}: OK - User ID: {m.user_id}", intensity=0.9))
        except Exception as e:
            print(rainbow_text(f"Cookie {i}: Lỗi - {e}", intensity=0.7))

    if not messengers:
        print(rainbow_text("Không có cookie hợp lệ."))
        return

    id_box = input(rainbow_text("\nNhập ID Box Messenger: ", intensity=0.8)).strip()

    target_uids = []
    print(rainbow_text("\nNhập UID người cần tag (Enter trống hoặc 'done'):"))
    while True:
        t_uid = input(rainbow_text("> ", intensity=0.7)).strip()
        if not t_uid or t_uid.lower() == 'done': break
        target_uids.append(t_uid)

    if not target_uids:
        print(rainbow_text("Chưa nhập UID người bị tag."))
        return

    try:
        current_delay = float(input(rainbow_text("\nNhập Delay (giây, mặc định 0.3): ", intensity=0.8) or "0.3"))
        if current_delay < 0.08: current_delay = 0.08
    except:
        current_delay = 0.3

    file_path = "nhay.txt"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            nhay_lines = [l.strip() for l in f if l.strip()]
        if not nhay_lines: raise Exception
        print(rainbow_text(f"Đã load {len(nhay_lines)} dòng ngôn từ nhay.txt", intensity=0.9))
    except:
        print(rainbow_text(f"File {file_path} không tồn tại hoặc trống!"))
        return

    print(rainbow_text("\n💥 NHÂY TAG VÔ HẠN BẮT ĐẦU – By YOUNGCE HL 🔥🌈", intensity=1.0))
    print(rainbow_text("➜ 's' = dừng | 'c' = đổi delay"))

    thread = threading.Thread(target=nhay_tag_loop, args=(messengers, id_box, target_uids, nhay_lines))
    thread.daemon = True
    thread.start()

    while True:
        cmd = input().strip().lower()
        if cmd == 's':
            stop_flag = True
            print(rainbow_text("\n[!] ĐANG DỪNG... chờ thread xong", intensity=0.9))
            break
        elif cmd == 'c':
            try:
                new_d = float(input(rainbow_text("Delay mới (giây): ", intensity=0.8)))
                if new_d < 0.08: new_d = 0.08
                current_delay = new_d
                print(rainbow_text(f"[OK] Delay cập nhật: {current_delay:.2f}s", intensity=0.95))
            except:
                print(rainbow_text("[Lỗi] Nhập số hợp lệ đi bro", intensity=0.7))
        
    print(rainbow_text("Tool đã dừng. Chạy lại khi nào cần nháy tiếp nhé! 🌈"))
    time.sleep(1.5)

if __name__ == "__main__":
    main()