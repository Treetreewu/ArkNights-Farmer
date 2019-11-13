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



def wait(image, timeout=None, interval=0.5, intervalfunc=None, resolution=(2160, 1080), **kwargs):
    airtest_wait(Template(resource_path(f"image/{image}.png"), **kwargs),
                 timeout=timeout, interval=interval, intervalfunc=intervalfunc)


def exists(image, resolution=(2160, 1080), **kwargs):
    return airtest_exists(Template(resource_path(f"image/{image}.png"), resolution=resolution, **kwargs))


def cached_try_touch(image, cache_dict, wait=0, **kwargs):
    """
    try touch with cached position.
    :param image: str
    :param cache_dict:
    :param kwargs:
    :return:
    """

    if cache_dict.get(image):
        return touch(cache_dict[image])
    else:
        cache_dict[image] = try_touch(image, wait, **kwargs)
        return cache_dict[image]


def cached_touch(image, cache_dict, **kwargs):
    """
    touch with cached position.
    :param image: str
    :param cache_dict:
    :param kwargs:
    :return:
    """
    if cache_dict.get(image):
        return touch(cache_dict[image])
    else:
        cache_dict[image] = touch_image(image, **kwargs)
        return cache_dict[image]


def touch_image(image, resolution=(2160, 1080), **kwargs):
    return touch(Template(resource_path(f"image/{image}.png"), resolution=resolution, **kwargs))


def try_touch(image, wait=0, **kwargs):
    pos = exists(image, **kwargs)
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


