# pip install netifaces
import ctypes
import subprocess
import sys
import time
from datetime import datetime
import schedule as sc


def enable():
    subprocess.call("netsh interface set interface Wi-Fi enabled")
    print("Turning On the laptop WiFi")

def disable():
    subprocess.call("netsh interface set interface Wi-Fi disabled")
    print("Turning Off the laptop WiFi")


    
def job():
    if subprocess.call("netsh interface set interface Wi-Fi enabled") == 0:
        print("WiFi is enabled and connected to internet")
        hostname = "www.google.com"
        response = subprocess.call("ping -n 1 " + hostname)
        if response == 1:
            print("Your Connection is not working")
            disable()
            time.sleep(1)
            enable()

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    # job()
    sc.every(50).seconds.do(job)
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)


while True:
    sc.run_pending()
    time.sleep(1)


# import ctypes
# import subprocess
# import sys
# import time
# import schedule as sc

# def enable_wifi():
#     result = subprocess.call("netsh interface set interface Wi-Fi enabled", shell=True)
#     if result == 0:
#         print("Wi-Fi is turned ON.")
#     else:
#         print("Failed to enable Wi-Fi.")

# def disable_wifi():
#     result = subprocess.call("netsh interface set interface Wi-Fi disabled", shell=True)
#     if result == 0:
#         print("Wi-Fi is turned OFF.")
#     else:
#         print("Failed to disable Wi-Fi.")

# def check_connection():
#     hostname = "www.google.com"
#     response = subprocess.call(["ping", "-n", "1", hostname])
#     return response == 0

# def send_message():
#     print("Wi-Fi is working great!")
    
# def job():
#     if check_connection():
#         print("Wi-Fi is enabled and connected to the internet.")
#         send_message()
#     else:
#         print("Connection is not working.")
#         disable_wifi()
#         time.sleep(1)
#         enable_wifi()

# def is_admin():
#     try:
#         return ctypes.windll.shell32.IsUserAnAdmin()
#     except:
#         return False

# def main():
#     sc.every(50).seconds.do(job)
#     while True:
#         sc.run_pending()
#         time.sleep(1)

# if __name__ == '__main__':
#     if is_admin():
#         main()
#     else:
#         print("Requesting admin privileges...")
#         ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
