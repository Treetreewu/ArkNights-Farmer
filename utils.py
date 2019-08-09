import os
import sys
import time

from airtest.core.api import sleep, touch, Template, exists


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
        pos = exists(Template(resource_path("image/confirm.png"), record_pos=(0.176, 0.1), resolution=(2160, 1080)))
        if pos:
            touch(pos)
        sleep(5)


def touch_image(image, record_pos=None, resolution=(2160, 1080)):
    return touch(Template(resource_path(f"image/{image}.png"), record_pos=record_pos, resolution=resolution))


def exist_at_home(image, record_pos=None, resolution=(2160, 1080)):
    template = Template(resource_path(f"image/{image}.png"), record_pos=record_pos, resolution=resolution)
    pos = exists(template)
    if not pos:
        try:
            go_home(True)
            pos = exists(template)
        except:
            pass
    if not pos:
        print("放在主页哦~亲。")
        return None
    return pos


def try_touch(image, record_pos=None, resolution=(2160, 1080), wait=0):
    pos = exists(Template(resource_path(f"image/{image}.png"), record_pos=record_pos, resolution=resolution))
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
