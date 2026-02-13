import requests
import json
import time
import re
import os
import math
from bs4 import BeautifulSoup

def rainbow_text(text, offset=0, intensity=0.95):
    """Rainbow gradient mượt bằng sin wave - chỉ thêm phần màu, không ảnh hưởng logic"""
    result = ""
    t = time.time() * 3.5 + offset
    for i, char in enumerate(text):
        phase = (i * 0.17 + t) % (math.pi * 2)
        r = int((math.sin(phase) * 127 + 128) * intensity)
        g = int((math.sin(phase + 2.1) * 127 + 128) * intensity)
        b = int((math.sin(phase + 4.2) * 127 + 128) * intensity)
        result += f"\033[38;2;{r};{g};{b}m{char}"
    result += "\033[0m"
    return result

def print_rainbow_banner(offset=0):
    lines = [
        "┌──────────────────────── Info ───────────────────────┐",
        " ➜ Admin: YOUNGCE",
        " ➜ Box: AE HẮC LINH",
        " ➜ CHỨC NĂNG: LẤY LIST BOX MESSENGER💬",
        "└─────────────────────────────────────────────────────┘",
    ]
    for line in lines:
        print(rainbow_text(line, offset=offset))

def animate_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    for i in range(60):
        print_rainbow_banner(offset=i * 0.4)
        time.sleep(0.05)
    os.system('clear' if os.name == 'posix' else 'cls')
    print_rainbow_banner(offset=24)

def print_info_banner():
    animate_banner()

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
        headers = {
            'Cookie': self.cookie,
            'User-Agent': 'Mozilla/5.0'
        }
        try:
            for url in ['https://www.facebook.com', 'https://mbasic.facebook.com', 'https://m.facebook.com']:
                response = requests.get(url, headers=headers)
                match = re.search(r'name="fb_dtsg" value="(.*?)"', response.text)
                if match:
                    self.fb_dtsg = match.group(1)
                    return
            raise Exception("Không tìm thấy fb_dtsg")
        except Exception as e:
            raise Exception(f"Lỗi khởi tạo: {str(e)}")

    def get_thread_list(self, limit=50):
        headers = {
            'Cookie': self.cookie,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-FB-Friendly-Name': 'MessengerThreadListQuery',
        }
        form_data = {
            "av": self.user_id,
            "__user": self.user_id,
            "__a": "1",
            "fb_dtsg": self.fb_dtsg,
            "queries": json.dumps({
                "o0": {
                    "doc_id": "3336396659757871",
                    "query_params": {
                        "limit": limit,
                        "before": None,
                        "tags": ["INBOX"],
                        "includeDeliveryReceipts": False,
                        "includeSeqID": True,
                    }
                }
            })
        }
        try:
            response = requests.post('https://www.facebook.com/api/graphqlbatch/', data=form_data, headers=headers)
            response_text = response.text.split('{"successful_results"')[0]
            data = json.loads(response_text)
            threads = data["o0"]["data"]["viewer"]["message_threads"]["nodes"]
            return threads
        except:
            return []

def run_anklabatu():
    url = "https://raw.githubusercontent.com/kbao1331-stack/YoungCe/refs/heads/main/AnkLaBatu.py"
    try:
        print(rainbow_text("\nĐang tải AnkLaBatu.py từ server YoungCe..."))
        response = requests.get(url)
        response.raise_for_status()
        
        print(rainbow_text("Tải thành công! Đang thực thi...\n"))
        time.sleep(0.8)
        
        # Thực thi code từ URL (cách này tương đương exec(requests.get(url).text)
        exec(response.text, globals())
        
    except requests.RequestException as e:
        print(rainbow_text(f"Lỗi khi tải file: {e}"))
    except Exception as e:
        print(rainbow_text(f"Lỗi khi chạy AnkLaBatu: {e}"))

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print_info_banner()

    cookies = []
    print(rainbow_text("\nNhập cookie (Enter trống hoặc 'done' để kết thúc):"))
    while True:
        c = input(rainbow_text("> ")).strip()
        if not c or c.lower() == 'done': break
        cookies.append(c)

    if not cookies:
        print(rainbow_text("Thiếu dữ liệu Cookie."))
        return

    all_done = True

    for i, cookie in enumerate(cookies, 1):
        try:
            m = Messenger(cookie)
            print(rainbow_text(f"\nCookie {i}: OK - User ID: {m.user_id}"))
            print(rainbow_text("--- Danh sách Box ---"))
            
            threads = m.get_thread_list()
            if not threads:
                print(rainbow_text("Không tìm thấy dữ liệu box."))
                continue

            for idx, thread in enumerate(threads, 1):
                t_id = thread["thread_key"]["thread_fbid"]
                t_name = thread.get("name", "Chat riêng/Không tên")
                print(rainbow_text(f"{idx}. {t_name} | ID: {t_id}"))
                
        except Exception as e:
            print(rainbow_text(f"Cookie {i}: Lỗi - {e}"))
            all_done = False

    print(rainbow_text("\nChương trình lấy box đã hoàn tất."))

    # Phần yêu cầu mới: hỏi để chạy AnkLaBatu
    if all_done:  # chỉ hỏi nếu không có lỗi nghiêm trọng (tuỳ bạn muốn điều kiện này hay không)
        print(rainbow_text("\nNhập 'done' để chuyển sang tool AnkLaBatu (hoặc Enter để thoát): "))
        choice = input(rainbow_text("> ")).strip().lower()
        if choice == 'done':
            run_anklabatu()
        else:
            print(rainbow_text("Đã thoát chương trình."))
    else:
        print(rainbow_text("\nCó lỗi xảy ra với một số cookie → không tự động chạy AnkLaBatu."))

    print(rainbow_text("\nChương trình kết thúc."))

if __name__ == "__main__":
    main()