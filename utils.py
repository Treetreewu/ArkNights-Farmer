import os
import sys
import time

from airtest.core.api import sleep, touch, Template, exists as airtest_exists, wait as airtest_wait

BACK_POS = None
HOME_POS = None
SKIP_POS = None


def press_back(times):
    global BACK_POS
    for i in range(times):
        if BACK_POS:
            touch(BACK_POS)
        else:
            BACK_POS = touch_image("back", record_pos=(-0.441, -0.223))
        sleep(0.5)


def go_home(in_gay=False):
    global HOME_POS
    if HOME_POS and False:
        touch(HOME_POS[0])
        touch(HOME_POS[1])
    else:
        HOME_POS = [
            touch_image("home_icon", record_pos=(-0.312, -0.223)),
            touch_image("home", record_pos=(-0.38, -0.088))
        ]
    sleep(0.5)
    if in_gay:
        pos = exists("confirm", record_pos=(0.176, 0.1))
        if pos:
            touch(pos)
        sleep(5)


def wait(image, timeout=None, interval=0.5, intervalfunc=None, resolution=(2160, 1080), **kwargs):
    airtest_wait(Template(resource_path(f"image/{image}.png"), **kwargs),
                 timeout=timeout, interval=interval, intervalfunc=intervalfunc)


def exists(image, resolution=(2160, 1080), **kwargs):
    return airtest_exists(Template(resource_path(f"image/{image}.png"), resolution=resolution, **kwargs))


def touch_image(image, resolution=(2160, 1080), **kwargs):
    return touch(Template(resource_path(f"image/{image}.png"), resolution=resolution, **kwargs))


def try_touch(image, resolution=(2160, 1080), wait=0, **kwargs):
    pos = exists(image, resolution, **kwargs)
    if pos:
        time.sleep(wait)
        touch(pos)
    return pos


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# def check_input():
#     while True:
#         try:
#             for i in task:
#                 if i not in TASK_INFO.keys():
#                     raise ValueError
#             if task.count("1") > 1 or (task.count("1") == 1 and not task.startswith("1")):
#                 raise ValueError
#             break
#         except:
#             task = input("别闹，请重新输入：")
#     return task

class StringUtils:
    @staticmethod
    def parse_net_adb(ip):
        ip = ip.replace("：", ":")
        if ":" not in ip:
            ip += ":5555"
        return ip


