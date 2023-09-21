# Py3-Port-Scanner
A simple and fast Python3 Port Scanner.


# Features
Scans the IP range specified in CIDR format.

Scans the single port specified by the user or all ports in multiple ranges.

Stores the IP with open ports in a txt file.


# Usage
Launch the Linux terminal.

```Bash
git clone https://github.com/korea821/py3-port-scanner.git
cd py3-port-scanner
python3 port-scanner.py
```

Please enter the IP address range to scan in CIDR format. (e.g., 192.168.0.0/24)

Please enter the port or port range to scan. (e.g., 80 or 80-100)

Please enter the name of the file to save. (e.g., results.txt)

The IP with the open port is saved in a txt file.
