import functools
import os
import sys
import time
import cv2
from airtest.core.api import \
    Template, ST, \
    touch as airtest_touch, \
    wait as airtest_wait
from airtest.core.cv import loop_find, TargetNotFoundError
from farmer.data import POSITION_CACHE

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


@functools.lru_cache()
def cached(func):
    """lru_cache is cache of functions, the decorator is cache of results."""
    @functools.wraps(func)
    def wrapped(image, *args, **kwargs):
        if pos := POSITION_CACHE.get(image):
            return pos
        pos = func(image, *args, **kwargs)
        if pos:
            POSITION_CACHE[image] = pos
        return pos
    return wrapped


def wait(image, timeout=None, interval=1, intervalfunc=None,
         resolution=(2160, 1080), **kwargs):
    return airtest_wait(
        Template(resource_path(f"image/{image}.png"),
                 resolution=resolution, record_pos=RECORD_POS.get(image),
                 **kwargs
                 ),
        timeout=timeout, interval=interval, intervalfunc=intervalfunc)


def must_exists(image, resolution=(2160, 1080),
                timeout=ST.FIND_TIMEOUT_TMP,
                threshold=None, interval=1, **kwargs):
    return loop_find(
        Template(
            resource_path(f"image/{image}.png"),
            resolution=resolution,
            record_pos=RECORD_POS.get(image),
            **kwargs),
        timeout=timeout,
        threshold=threshold,
        interval=interval
    )


def exists(image, resolution=(2160, 1080), timeout=ST.FIND_TIMEOUT_TMP,
           threshold=None, interval=1, **kwargs):
    try:
        pos = must_exists(image, resolution, timeout, threshold, interval,
                          **kwargs)
    except TargetNotFoundError:
        return False
    return pos


# Partial of exist, find once instead of loop find.
def exists_now(image, resolution=(2160, 1080), threshold=None, **kwargs):
    return exists(image, resolution, 0.01, threshold, 0, **kwargs)


def must_exists_now(image, resolution=(2160, 1080), threshold=None, **kwargs):
    return must_exists(image, resolution, 0.01, threshold, 0, **kwargs)


def _touch(image, exist_func, use_cache=True, *args, **kwargs):
    if use_cache:
        exist_func = cached(exist_func)
    else:
        exist_func = exist_func
    pos = exist_func(image, *args, **kwargs)
    if pos:
        airtest_touch(pos)
    return pos


def touch(image, use_cache=True, *args, **kwargs):
    return _touch(image, must_exists_now, use_cache, *args, **kwargs)


def try_touch(image, use_cache=False, *args, **kwargs):
    return _touch(image, exists_now, use_cache, *args, **kwargs)


def wait_and_touch(image, use_cache=False, *args, **kwargs):
    return _touch(image, exists, use_cache, *args, **kwargs)


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


if __name__ == '__main__':
    from airtest.core.api import ST
    from airtest.core.cv import MATCHING_METHODS

    for m in MATCHING_METHODS:
        t0 = time.time()
        ST.CVSTRATEGY = [m]
        Template(
            resource_path("image/home_icon.png"),
            resolution=(2160, 1080),
            record_pos=(-0.312, -0.223)
        ).match_in(cv2.imread("test_image/task.png"))
        print(m, time.time() - t0)
