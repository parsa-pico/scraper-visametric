
import psutil
import requests
from datetime import datetime
import time
import traceback
from time import sleep


class TOO_MUCH_REQ_EXCEPTION(Exception):
    pass


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_black(rgb):
    maxColor = max(rgb)
    blackness = 100 - 100 * maxColor / 255
    return blackness


def hex_to_black(hex):
    rgb = hex_to_rgb(hex)
    return rgb_to_black(rgb)


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)  # use start += 1 to find overlapping matches


def notify():
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    res = requests.post('https://api.mynotifier.app', {
        "apiKey": '6c340172-72cd-4fff-a2cc-8bf6d1930c9a',
        "message": f"!!!Visametric {now} !!!!",
        "type": "warning"
    })
    log("notify res:", res)


def multiNotify(n):
    for _ in range(0, n):
        notify()
        time.sleep(2)


def log(*strings):
    strings = map(lambda x: str(x), strings)
    string = "".join(strings)
    print(string)
    with open("logs.txt", "a") as file:
        file.write(string)
        file.write("\n")
        file.write(str(datetime.now()))
        file.write("\n")
        file.write("---\n")


def delay(t1, timeout):
    while time.time() - t1 < timeout:
        ...


def kill_proc(name):
    for proc in psutil.process_iter():
        if proc.name() == name:
            proc.kill()


def handle_exception(desc, e, browser, delay_time, log_trace_back=True):
    log(desc, e)
    if log_trace_back:
        log(traceback.format_exc())
    print("closing browser")
    try:
        kill_proc("chrome.exe")
    except Exception as e :
        log(e)
    sleep(delay_time)


if __name__ == "__main__":
    print("utils main")
