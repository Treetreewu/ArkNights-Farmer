import os
import sys
import time

from airtest.core.api import sleep, touch, Template, exists as airtest_exists, wait as airtest_wait
from airtest.core.settings import Settings as ST

RECORD_POS = {
    "back": (-0.441, -0.223),
    "home_icon": (-0.312, -0.223),
    "menu_home": (-0.38, -0.088),
    "menu_maps": (-0.077, -0.152),
    "menu_gay": (0.031, -0.15),
    "menu_recruit": (0.22, -0.064),
    "menu_tasks": (0.306, -0.224),
    "menu_friends": (0.385, -0.224),
    "friends": (-0.246, 0.15),
    "friend_list": (-0.415, -0.096),
    "gay_friends": (0.184, -0.133),
    "recruit": (0.295, 0.109),
    "task": (0.121, 0.161),
    "gay": (0.285, 0.176),
    "confirm": (0.176, 0.1),
    "start1": (0.316, 0.101),
    "cancel": (-0.269, 0.123),
    "start0": (0.421, 0.201),
    "start0_event": (0.4, 0.2),
    "over": (-0.349, 0.189),
    "upgrade": (-0.15, 0.011),
    "update_proxy": (-0.292, -0.008),
    "skip": (0.459, -0.22),
    "task_weekly": (0.139, -0.225),
    "task_main_line": (0.348, -0.226),
    "task_daily": (0.069, -0.225),
    "task_event": (-0.045, -0.225),
    "gay_next": (0.433, 0.183),
    "notification": (0.444, -0.184),
    "orders": (-0.33, 0.231),
    "open_up_trade": (-0.37, -0.045),
    "open_up_manufacturing": (-0.184, 0.146),
    "01": (-0.472, -0.102),
    "02": (-0.47, -0.045),
    "03": (-0.471, 0.01),
    "04": (-0.471, 0.067),
    "popup0": (0.41, -0.212),
    "maps": (0.275, -0.13),
    "mail": (-0.363, -0.22),
    "maps_material": (-0.338, 0.207),
    "maps_mainline": (-0.444, 0.209),
    "maps_chip": (-0.23, 0.209),
    "maps_annihilation": (-0.127, 0.21),
    "material_LS": (-0.369, -0.013),
    "material_AP": (-0.183, -0.016),
    "material_CE": (0.002, -0.014),
    "chip_A": (-0.28, -0.017),
    "chip_C": (-0.092, -0.016),
    "max_drone": (0.22, -0.017),
    "ok": (0.234, 0.153),
    "0drone": (0.137, -0.227),
    "stone-": (0.34, 0.18),
    "gold-": (0.339, 0.18),
    "gold+": (0.388, -0.052),
    "record+": (0.388, -0.05),
    "stone+": (0.387, -0.051),
    "max_manufacturing": (0.278, -0.108),
    "drone_trade": (-0.241, 0.092),
    "ok1": (0.268, 0.163),
    "drone_manufacturing": (0.456, 0.124),
    "use_drink": (0.096, -0.195),
    "use_stone": (0.334, -0.196),
    "cancel1": (0.096, 0.152),
    "ok2": (0.309, 0.152),
    "stone_large": (0.111, -0.023),
    "gather": (0.393, 0.195),

    "maps/annihilation0": (-0.358, -0.013),
    "maps/annihilation1": (0.019, 0.156),
    "maps/annihilation2": (0.244, 0.008),
}


def wait(image, timeout=None, interval=1, intervalfunc=None, resolution=(2160, 1080), **kwargs):
    return airtest_wait(
        Template(resource_path(f"image/{image}.png"),
                 resolution=resolution, record_pos=RECORD_POS.get(image), **kwargs
                 ),
        timeout=timeout, interval=interval, intervalfunc=intervalfunc)


def exists(image, resolution=(2160, 1080), timeout=ST.FIND_TIMEOUT_TMP, **kwargs):
    old_timeout = None
    if timeout != ST.FIND_TIMEOUT_TMP:
        old_timeout = ST.FIND_TIMEOUT_TMP
        ST.FIND_TIMEOUT_TMP = timeout
    pos = airtest_exists(Template(resource_path(f"image/{image}.png"), resolution=resolution, record_pos=RECORD_POS.get(image), **kwargs))
    if old_timeout is not None:
        ST.FIND_TIMEOUT_TMP = old_timeout
    return pos


def cached_try_touch(image, cache_dict, delay=1, wait=0, **kwargs):
    """
    try touch with cached position.
    :param delay:
    :param image: str
    :param cache_dict:
    :param kwargs:
    :return:
    """
    if cache_dict.get(image):
        time.sleep(delay)
        return touch(cache_dict[image])
    else:
        cache_dict[image] = try_touch(image, wait, **kwargs)
        return cache_dict[image]


def cached_touch(image, cache_dict, delay=0.5, **kwargs):
    """
    touch with cached position.
    :param delay: wait before click if cached.
    :param image: str
    :param cache_dict:
    :param kwargs:
    :return:
    """
    if cache_dict.get(image):
        time.sleep(delay)
        return touch(cache_dict[image])
    else:
        cache_dict[image] = touch_image(image, **kwargs)
        return cache_dict[image]


def touch_image(image, resolution=(2160, 1080), **kwargs):
    return touch(Template(resource_path(f"image/{image}.png"), resolution=resolution, record_pos=RECORD_POS.get(image), **kwargs))


def try_touch(image, wait=0.5, **kwargs):
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


class StringUtils:
    @staticmethod
    def parse_net_adb(ip):
        ip = ip.replace("：", ":")
        if ":" not in ip:
            ip += ":5555"
        return ip
