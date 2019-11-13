import time

from airtest.core.api import sleep, touch, connect_device, auto_setup, ST
import utils
from copy import deepcopy
from threading import Thread

from configurator import s

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
    def goto_screen(screen):
        global POSITION_CACHE
        # do nothing if at home, else show menu
        home_icon_pos = utils.exists("home_icon", record_pos=(-0.312, -0.223))
        if home_icon_pos:
            touch(home_icon_pos)

        if screen == Navigator.HOME:
            utils.cached_touch("home", POSITION_CACHE, record_pos=(-0.38, -0.088))
        elif screen == Navigator.GAY_FRIENDS:
            if home_icon_pos:
                pass
            else:
                utils.touch_image("friends", record_pos=(-0.246, 0.15))
            utils.touch_image("friend_list", record_pos=(-0.415, -0.096))
            utils.touch_image("gay_friends", record_pos=(0.184, -0.133))
        elif screen == Navigator.RECRUIT:
            if home_icon_pos:
                pass
            else:
                utils.touch_image("recruit", record_pos=(0.295, 0.109))
        elif screen == Navigator.TASK:
            if home_icon_pos:
                pass
            else:
                utils.touch_image("task", record_pos=(0.121, 0.161))
        elif screen == Navigator.GAY:
            if home_icon_pos:
                pass
            else:
                utils.touch_image("gay", record_pos=(0.285, 0.176))
        elif screen == Navigator.MAPS:
            if home_icon_pos:
                pass
            else:
                pass

        sleep(0.5)
        if utils.try_touch("confirm", record_pos=(0.176, 0.1)):
            sleep(5)

    @staticmethod
    def goto_map(map_):
        """
        goto certain map and select auto command.
        :param map_: 1-7
        :return:
        """
        Navigator.goto_screen(Navigator.MAPS)
        # TODO
        pass

    @staticmethod
    def at_home():
        if utils.exists("home_icon", record_pos=(-0.312, -0.223)):
            return False
        else:
            return True


def farm(status, map_=None, times=None, auto_drink=False, auto_eat=False, **kwargs):
    """
    :param status:
    :param map_: TODO
    :param times: if 理智 not enough,
    :param auto_drink: drink if reason run out.
    :param auto_eat: eat stones if reason run out and drink run out.
    :return:
    """
    if map_:
        Navigator.goto_map(map_)
    if not times:
        limit = 65535
    else:
        limit = times
    for count in range(limit):
        status.set_status(status.RUNNING, TASKS["farm"]["str"].format(times=f"{count+1}/{times}"))
        print('\r', f"(。・∀・)ノ[{count + 1}]", end='', flush=True)
        if not utils.cached_try_touch("start0", POSITION_CACHE, record_pos=(0.421, 0.201)):
            utils.cached_try_touch("start0_event", POSITION_CACHE, record_pos=(0.4, 0.2))
        sleep(3)
        if not utils.try_touch("start1", record_pos=(0.316, 0.101)):
            pos = utils.exists("cancel", record_pos=(-0.269, 0.123))
            if pos:
                print("\n你理智没了。")
                # TODO auto drink/eat
                touch(pos)
                return
            else:
                raise Exception
        sleep(90)
        while True:
            try:
                pos = utils.wait("over", record_pos=(-0.349, 0.189), timeout=20, interval=5)
                sleep(3)
                touch(pos)
                break
            except:
                pass
            try:
                pos = utils.wait("upgrade", record_pos=(-0.15, 0.011), timeout=1)
                sleep(3)
                touch(pos)
            except:
                pass
            utils.try_touch("update_proxy", record_pos=(-0.292, -0.008))
        sleep(3)
    print()


def recruit(**kwargs):
    print("干员招募中...")
    Navigator.goto_screen(Navigator.RECRUIT)
    while True:
        if utils.try_touch("hire"):
            sleep(3)
            pos = utils.cached_touch("skip", POSITION_CACHE, record_pos=(0.459, -0.22))
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
            else:
                break

    print("任务收集中...")
    Navigator.goto_screen(Navigator.TASK)
    # daily or event
    done_tab()
    # utils.try_touch("task_daily", record_pos=(0.069, -0.225))
    # weekly
    utils.try_touch("task_weekly", record_pos=(0.139, -0.225))
    done_tab()
    # mainline
    utils.try_touch("task_main_line", record_pos=(0.348, -0.226))
    done_tab(main_line=True)


def gay_friends(**kwargs):
    print("正在与好友基♂健...")
    Navigator.goto_screen(Navigator.GAY)
    sleep(5)
    while True:
        pos = utils.try_touch("gay_next", record_pos=(0.433, 0.183))
        if not pos:
            break
        sleep(3)


def poke_wife(**kwargs):
    # 现在可以批量收信赖+制造站，就放在一起了。
    print("少女祈祷中...")

    def deliver_all():
        while utils.try_touch("deliver"):
            sleep(2)

    Navigator.goto_screen(Navigator.GAY)

    # notification
    if utils.try_touch("notification", record_pos=(0.444, -0.184), rgb=True):
        sleep(2)
    else:
        return
    # 制造站
    if utils.try_touch("manufacturer"):
        sleep(1)
    # 信赖
    utils.try_touch("trust")
    # 贸易站
    if not utils.try_touch("trade0"):
        utils.touch_image("trade1")
    utils.touch_image("open_up", record_pos=(-0.37, -0.045))
    utils.try_touch("01", record_pos=(-0.472, -0.102))
    deliver_all()
    if not utils.try_touch("02", record_pos=(-0.47, -0.045)):
        return
    deliver_all()
    if not utils.try_touch("03", record_pos=(-0.471, 0.01)):
        return
    deliver_all()
    if not utils.try_touch("04", record_pos=(-0.471, 0.067)):
        return
    deliver_all()


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
                task_func(**kwargs)
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
        return "Task running."


class DeviceError(Exception):
    pass
