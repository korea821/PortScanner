import socket
import locale
import json
from ipaddress import IPv4Network, AddressValueError
from concurrent.futures import ThreadPoolExecutor

# 시스템 locale 얻기
current_locale = locale.setlocale(locale.LC_ALL, '')

# locale 문자열에서 불필요한 부분 제거
current_locale = current_locale.split('.')[0]  # en_US.UTF-8 > en_US / Korean_Korea.949 -> Korean_Korea

# JSON에서 언어 메시지를 불러오는 함수
def load_language_messages():
    with open("languages.json", "r", encoding="utf-8") as f:
        return json.load(f)
    
messages = load_language_messages()

messages = messages.get(current_locale, messages["en_US"])

def scan_target(ip, port, file_name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        socket.setdefaulttimeout(2)
        result = s.connect_ex((ip, port))  # Returns 0 if success
        if result == 0:
            message = f"{ip}"
            print(message)
            with open(file_name, 'a') as f:
                f.write(message + "\n")

def get_input_cidr():
    while True:
        # IP 주소 범위를 입력받는 부분
        cidr = input(messages["input_cidr"])
        try:
            IPv4Network(cidr)
            return cidr
        except AddressValueError:
            print(messages["wrong_cidr"])

def get_ports():
    ports = input(messages["input_ports"])
    
    if "-" in ports:
        start_port, end_port = map(int, ports.split("-"))
        return range(start_port, end_port + 1)
    else:
        return [int(ports)]
    
def get_input_file_name():
    while True:
        # 파일 이름을 입력받는 부분
        file_name = input(messages["input_file_name"])
        if file_name.endswith(".txt"):
            return file_name
        else:
            print(messages["wrong_ext"])

def main():
    cidr = get_input_cidr()
    ports = get_ports()
    file_name = get_input_file_name()
    
    target_ips = IPv4Network(cidr)
    
    socket.setdefaulttimeout(2) # Timeout 값 2초
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        for ip in target_ips:
            for port in ports:
                executor.submit(scan_target, str(ip), port, file_name)

if __name__ == "__main__":
    main()
