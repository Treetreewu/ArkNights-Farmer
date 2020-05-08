import time
import traceback

from airtest.core.api import sleep, touch, connect_device, auto_setup, ST
import utils
from copy import deepcopy
from threading import Thread

from configurator import s
import logging

logging.getLogger("airtest").setLevel(logging.WARNING)
ST.FIND_TIMEOUT = 5
POSITION_CACHE = {}


class Navigator:
    MAPS = "maps"
    HOME = "home"
    GAY = "poke_wife"
    RECRUIT = "recruit"
    TASK = "tasks"
    GAY_FRIENDS = "gay"

    @staticmethod
    def go_back(times=1):
        for i in range(times):
            if not utils.try_touch("back"):
                break

    @staticmethod
    def goto_screen(screen):
        global POSITION_CACHE
        # do nothing if at home, else show menu
        home_icon_pos = utils.exists("home_icon")
        if home_icon_pos:
            touch(home_icon_pos)

        if screen == Navigator.HOME:
            utils.cached_touch("menu_home", POSITION_CACHE)
        elif screen == Navigator.GAY_FRIENDS:
            if home_icon_pos:
                utils.touch_image("menu_friends")
            else:
                utils.touch_image("friends")
            utils.touch_image("friend_list")
            utils.touch_image("gay_friends")
        elif screen == Navigator.RECRUIT:
            if home_icon_pos:
                utils.touch_image("menu_recruit")
            else:
                utils.touch_image("recruit")
        elif screen == Navigator.TASK:
            if home_icon_pos:
                utils.touch_image("menu_tasks")
            else:
                utils.touch_image("task")
        elif screen == Navigator.GAY:
            if home_icon_pos:
                utils.touch_image("menu_gay")
            else:
                utils.touch_image("gay")
            sleep(5)
        elif screen == Navigator.MAPS:
            if home_icon_pos:
                utils.touch_image("menu_maps")
            else:
                utils.touch_image("maps")
        sleep(0.5)
        if utils.try_touch("confirm"):
            # in gay.
            sleep(5)

    @staticmethod
    def goto_map(map_):
        """
        goto certain map and select auto command.
        :param map_: 1-7
        :return:
        """
        Navigator.goto_screen(Navigator.MAPS)
        # TODO goto selected map.
        pass

    @staticmethod
    def at_home():
        if utils.exists("home_icon"):
            return False
        else:
            return True


def farm(status, map_=None, times=None, auto_drink=False, auto_eat=False, **kwargs):
    """
    :param status:
    :param map_: TODO goto selected map.
    :param times: if reason not enough,...
    :param auto_drink: drink if reason run out.
    :param auto_eat: eat stones if reason run out and drink run out.
    :return:
    """
    def add_reason(drink, eat):
        if not (drink or eat) and times:
            raise ReasonRunOutException
        if drink:
            if not utils.exists("stone_large"):
                utils.touch_image("ok2")
                time.sleep(4)
                return
        if eat:
            utils.try_touch("use_stone")
            if utils.exists("stone_large"):
                utils.touch_image("ok2")
                time.sleep(4)
                return

    if map_:
        pass
        # Navigator.goto_map(map_)
    utils.try_touch("proxy")

    if not times:
        limit = 65535
    else:
        limit = times
    for count in range(limit):
        status.set_status(status.RUNNING, task=TASKS["farm"]["str"].format(times=f"{count+1}/{times}"))
        print('\r', f"(。・∀・)ノ[{count + 1}]", end='', flush=True)
        if not utils.cached_try_touch("start0", POSITION_CACHE):
            utils.cached_try_touch("start0_event", POSITION_CACHE)
        sleep(3)
        if not utils.try_touch("start1"):
            pos = utils.exists("cancel1")
            if pos:
                add_reason(auto_drink, auto_eat)
                if utils.try_touch("cancel1"):
                    return
                # restart
                if not utils.cached_try_touch("start0", POSITION_CACHE):
                    utils.cached_try_touch("start0_event", POSITION_CACHE)
                sleep(3)
                utils.touch_image("start1")
            else:
                raise Exception
        sleep(90)
        while True:
            try:
                pos = utils.wait("over", timeout=20, interval=5)
                sleep(3)
                touch(pos)
                break
            except:
                pass
            try:
                pos = utils.wait("upgrade", timeout=1)
                sleep(3)
                touch(pos)
            except:
                pass
            utils.try_touch("update_proxy")
            sleep(3)
        sleep(4)
    print()


def recruit(**kwargs):
    print("干员招募中...")
    # TODO auto choose tags.
    Navigator.goto_screen(Navigator.RECRUIT)
    while True:
        if utils.try_touch("hire"):
            sleep(3)
            pos = utils.cached_touch("skip", POSITION_CACHE)
            sleep(4)
            touch(pos)
        else:
            break


def done_task(**kwargs):
    def done_tab(main_line=False):
        last_pos = None
        for i in range(12):  # <- new implement by limiting loop times
            if main_line:
                pos = utils.exists("receive_main_line")
            else:
                pos = utils.exists("receive")  # , rgb=True, threshold=0.97) <- old implement
            if pos:
                last_pos = pos
                touch(pos)
                sleep(1)
                if main_line:
                    touch(pos)
            elif last_pos:
                # receive bonus perhaps
                touch(last_pos)
                last_pos = None
                sleep(1)
            else:
                break

    print("任务收集中...")
    Navigator.goto_screen(Navigator.TASK)
    # daily or event
    done_tab()
    # utils.try_touch("task_daily")
    # weekly
    utils.try_touch("task_weekly")
    done_tab()
    # mainline
    utils.try_touch("task_main_line")
    done_tab(main_line=True)


def gay_friends(**kwargs):
    print("正在与好友基♂健...")
    Navigator.goto_screen(Navigator.GAY_FRIENDS)
    sleep(5)
    while True:
        if not utils.try_touch("gay_next", rgb=True, threshold=0.9):
            break
        sleep(3)


def poke_wife(drone=None, **kwargs):
    # 现在可以批量收信赖+制造站，就放在一起了。
    print("少女祈祷中...")

    Navigator.goto_screen(Navigator.GAY)
    # TODO count passed errors.
    # TODO auto change exhausted.
    errors = []

    # notification
    sleep(2)
    if utils.try_touch("notification", rgb=True):
        sleep(2)
        # 制造站
        utils.try_touch("manufacturer")
        # 信赖
        utils.try_touch("trust")
        # 贸易站
        utils.try_touch("orders")

    # auto drone manufacturing
    if drone:
        if drone.endswith("+"):
            pos = utils.touch_image("manufacturing_station")
            while not utils.try_touch("open_up_manufacturing"):
                # 防止刚好生产出来一个新的，导致没点进去。
                touch(pos)
            # 假设只有1234
            for i in range(1, 5):
                utils.try_touch(f"0{i}", threshold=0.9)
                utils.cached_touch("max_manufacturing", POSITION_CACHE)
                utils.cached_try_touch("ok1", POSITION_CACHE)
                if utils.exists(drone):
                    utils.cached_touch("drone_manufacturing", POSITION_CACHE)
                    utils.cached_touch("max_drone", POSITION_CACHE)
                    utils.cached_touch("ok", POSITION_CACHE)
                    utils.cached_touch("gather", POSITION_CACHE)
            Navigator.go_back(2)
        elif drone.endswith("-"):
            utils.touch_image("trade")
            # 防止刚好有新订单，导致没点进去。
            utils.try_touch("trade")
            utils.touch_image("open_up_trade")
            for i in range(1, 5):
                utils.try_touch(f"0{i}", threshold=0.9)
                if utils.exists(drone):
                    while not utils.exists("0drone", threshold=0.9):
                        utils.touch_image("drone_trade")
                        utils.cached_touch("max_drone", POSITION_CACHE)
                        utils.cached_touch("ok", POSITION_CACHE)
                        utils.try_touch("deliver")
                    break


# for UI
TASKS = {
    "farm": {"function": farm, "str": "刷图({times})", "add_str": "+刷图", "config_template": {
        "map": None,
        "times": 0,
        "auto_drink": False,
        "auto_eat": False
    }},
    "recruit": {"function": recruit, "str": "收招募", "add_str": "+收招募"},
    "done_task": {"function": done_task, "str": "收任务", "add_str": "+收任务"},
    "gay_friends": {"function": gay_friends, "str": "好友基♂建", "add_str": "+基建信用"},
    "poke_wife": {"function": poke_wife, "str": "基建收菜({drone})", "add_str": "+基建收菜",
                  "config_template": {"drone": None}},
}


class TasksRunnerDummy:
    # dummy for unit test.
    def __init__(self, serial_number, task_list, status):
        from view import Cache
        if Cache.running:
            raise TaskRunningError
        Cache.running = self
        self.status = status
        self.status.set_status(self.status.RUNNING, task="tttttttttt")
        self.task_list = deepcopy(task_list)
        self.thread = Thread(target=self._run_tasks)

    def run(self):
        self.thread.start()

    def _run_tasks(self):
        from view import Cache
        print(self.task_list)
        time.sleep(30)
        Cache.running = None
        self.status.set_status(self.status.READY)


class TasksRunner:
    # TODO add scheduled task
    def __init__(self, serial_number, task_list, status):
        from view import Cache
        self.status = status
        if Cache.running:
            raise TaskRunningError
        Cache.running = self
        self.status.set_status(self.status.RUNNING)
        try:
            connect_device(f"android:///{serial_number}?touch_method=adb")
            auto_setup(__file__)
        except:
            Cache.running = None
            self.status.set_status(self.status.READY)
            raise DeviceError

        self.task_list = deepcopy(task_list)
        self.thread = Thread(target=self._run_tasks)

    def _run_tasks(self):
        from view import Cache
        try:
            for task in self.task_list:
                self.status.set_status(self.status.RUNNING,
                                       task=TASKS[task["type"]]["str"].format(**(task.get("config")) or {}))
                t = TASKS.get(task["type"])
                if not t:
                    raise TaskNotFoundError(task["type"])
                task_func = t["function"]
                kwargs = task.get("config") or {}
                task_func(status=self.status, **kwargs)
            self.status.set_status(self.status.READY)
        except Exception as e:
            self.status.set_status(self.status.ERROR)
            Cache.message = e.__str__()
            raise e
        finally:
            Cache.running = None

    def run(self):
        self.thread.start()


class TaskNotFoundError(Exception):
    def __init__(self, task):
        self.task = task

    def __str__(self):
        return f"{self.task} not in {TASKS.keys()}"


class TaskRunningError(Exception):
    def __str__(self):
        return s.error_task_running


class DeviceError(Exception):
    pass


class ReasonRunOutException(Exception):
    def __str__(self):
        return s.error_reason_run_out

