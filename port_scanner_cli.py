import socket
import locale
import json
from ipaddress import IPv4Network, AddressValueError
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

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

def scan_target(ip, port, results):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        socket.setdefaulttimeout(1)
        result = s.connect_ex((ip, port))  # Returns 0 if success
        if result == 0:
            results[ip].append(port)
            message = f"Port {port} open on {ip}"  # 실시간으로 결과를 화면에 출력
            print(message)

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
    input_str = input(messages["input_ports"])
    port_ranges = input_str.split(',')
    ports = []
    
    for r in port_ranges:
        if "-" in r:
            start_port, end_port = map(int, r.split("-"))
            ports.extend(range(start_port, end_port + 1))
        else:
            ports.append(int(r))

    return ports
    
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
    
    socket.setdefaulttimeout(1) # Timeout 값 1초

    # IP별로 열린 포트를 저장하는 dictionary
    open_ports = defaultdict(list)
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = []
        for ip in target_ips:
            for port in ports:
                futures.append(executor.submit(scan_target, str(ip), port, open_ports))

    # 모든 스캔 작업이 완료되기를 기다림
    for future in futures:
        future.result()

    # 결과 출력 및 파일에 저장
    with open(file_name, 'a') as f:
        for ip, ports in open_ports.items():
            if ports:
                ports.sort()  # 포트를 오름차순으로 정렬
                message = f"{ip} has open ports: {', '.join(map(str, ports))}"
                print(message)
                f.write(message + "\n")

if __name__ == "__main__":
    main()
