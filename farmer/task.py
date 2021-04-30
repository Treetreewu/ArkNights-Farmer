import itertools
import time
from collections import Counter, defaultdict
from copy import deepcopy
from threading import Thread
import logging

from airtest.core.api import sleep, touch, connect_device, auto_setup, ST, keyevent

from farmer.exception import TaskNotFoundError, TaskRunningError, DeviceError, ReasonRunOutException
from farmer.data import POSITION_CACHE, TAGS, RARITY
from farmer import utils

logging.getLogger("airtest").setLevel(logging.ERROR)
ST.FIND_TIMEOUT_TMP = 3
ST.CVSTRATEGY = ["tpl"]  # default strategy 'kaze' is toooooo slow.
ST.SAVE_IMAGE = False


class Navigator:
    MAPS = "maps"
    HOME = "home"
    GAY = "infrastructure"
    RECRUIT = "recruit"
    TASK = "tasks"
    GAY_FRIENDS = "🤺"

    @staticmethod
    def go_back(times=1):
        for i in range(times):
            keyevent("BACK")

    @staticmethod
    def goto_screen(screen):
        # do nothing if at home, else show menu
        home_icon_pos = utils.exists_now("home_icon")
        if home_icon_pos:
            touch(home_icon_pos)

        if screen == Navigator.HOME:
            utils.touch("menu_home")
        elif screen == Navigator.GAY_FRIENDS:
            if home_icon_pos:
                utils.touch("menu_friends")
            else:
                utils.touch("friends")
            utils.touch("friend_list")
            utils.touch("gay_friends")
        elif screen == Navigator.RECRUIT:
            if home_icon_pos:
                utils.touch("menu_recruit")
            else:
                utils.touch("recruit")
        elif screen == Navigator.TASK:
            if home_icon_pos:
                utils.touch("menu_tasks")
            else:
                utils.touch("task")
        elif screen == Navigator.GAY:
            if home_icon_pos:
                utils.touch("menu_gay")
            else:
                utils.touch("gay")
            sleep(5)
        elif screen == Navigator.MAPS:
            if home_icon_pos:
                utils.touch("menu_maps")
            else:
                utils.touch("maps")
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


def farm(status, map_=None, times=None, auto_drink=False, auto_eat=False,
         **kwargs):
    """
    :param status:
    :param map_: TODO goto selected map.
    :param times: if reason not enough,...
    :param auto_drink: drink if reason run out.
    :param auto_eat: eat stones if reason run out and drink run out.
    :return:
    """

    def add_reason(drink, eat):
        if not (drink or eat):
            raise ReasonRunOutException
        if drink:
            if not utils.exists_now("stone_large"):
                utils.touch("ok2")
                time.sleep(4)
                return
        if eat:
            utils.try_touch("use_stone", rgb=True, threshold=0.9)
            if utils.exists("stone_large"):
                utils.touch("ok2")
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
        status.set_status(status.RUNNING, task=TASKS["farm"]["str"].format(
            times=f"{count + 1}/{times}"))
        print('\r', f"(。・∀・)ノ[{count + 1}]", end='', flush=True)
        if not utils.try_touch("start0"):
            utils.try_touch("start0_event", True)
        sleep(3)
        if not utils.try_touch("start1"):
            if utils.exists("cancel1"):
                add_reason(auto_drink, auto_eat)
                if utils.try_touch("cancel1"):
                    return
                # restart
                if not utils.try_touch("start0"):
                    utils.try_touch("start0_event")
                sleep(3)
                utils.touch("start1")
            else:
                raise Exception
        sleep(90)
        while True:
            try:
                pos_over = utils.wait("over", timeout=20, interval=5)
                sleep(4)
                touch(pos_over)
                break
            except:
                pass
            try:
                pos_upgrade = utils.wait("upgrade", timeout=1)
                sleep(3)
                touch(pos_upgrade)
            except:
                pass
            utils.try_touch("update_proxy")
            sleep(5)
        sleep(5)
    print()


def recruit(auto_recruit=True, choosable_over_5=False, **kwargs):
    """
    :param auto_recruit: 是否自动开始新的招募
    :param choosable_over_5: 存在多组保底5、6星标签的时候是否自动招募。
    （如果只有单组标签组合保底5 6星，那么还是会自动）
    （如果）
    """
    print("干员招募中...")

    def read_tags():
        result = {}
        for t in TAGS:
            if p := utils.exists_now(t):
                result[t] = p
        return result

    def count_stars(_tags):
        """Counting starts (o゜▽゜)o☆
        :return : List of tags to select.
                  None if skip this recruit.
        """
        stars = {}
        employs = {}
        # 计算选1, 2, 3个标签的情况
        for count in range(1, 4):
            for comb in itertools.combinations(_tags.keys(), count):
                # 交集
                emp = TAGS[comb[0]].intersection(*(TAGS[t] for t in comb[1:]))
                emp = frozenset(e for e in emp if RARITY[e] > 2)
                if not emp:
                    continue
                # 排除小于等于二星（指某些有高星标签的支援机械），计算保底
                employs[comb] = emp
                stars[comb] = min(RARITY[e] for e in employs[comb])
        # 保底最高星的组合
        result = max(stars, key=stars.get)
        if stars[result] <= 3:
            # 如果最高保底3星，就不选标签了，没必要。
            return []
        combs = [k for k in stars if stars[k] == stars[result]]
        if len(combs) == 1:
            return combs[0]
        if stars[result] == 4:
            # 4星组合有多种，取并集后按照标签出现次数最多的规则缩减为3个标签。
            counter = Counter(itertools.chain(*combs))
            return [t[0] for t in counter.most_common(3)]
        else:
            # 大于等于5星，首先排除干员池相同的标签组
            reverted_employs = defaultdict(list)
            for k, v in employs.items():
                if k in combs:
                    reverted_employs[v].append(k)

            if len(reverted_employs) == 1:
                return max(reverted_employs.popitem()[1], key=len)
            elif choosable_over_5:
                # 大杂烩随便选选。
                vs = itertools.chain(
                    *itertools.chain(*reverted_employs.values()))
                counter = Counter(vs)
                return tuple(t[0] for t in counter.most_common(3))
            else:
                return None

    def select_tags():
        """
        :return: None: 由于包含大于等于5星跳过。
                 True: 选择了4星标签。
                 False: ko ko da yo~~
        """
        t = read_tags()
        bt = count_stars(t)
        if bt is None:
            Navigator.go_back()
            return None
        else:
            map(touch, (t[b] for b in bt))
            return bool(bt)

    Navigator.goto_screen(Navigator.RECRUIT)
    while True:
        if utils.try_touch("hire"):
            sleep(3)
            pos = utils.touch("skip")
            sleep(4)
            touch(pos)
        else:
            break

    if not auto_recruit:
        return
    refreshable = True
    for i in range(4):
        if not utils.try_touch("start_recruit"):
            break
        best_tags = select_tags()
        while best_tags == [] and refreshable:
            # refresh
            if not utils.try_touch("refresh_recruit"):
                refreshable = False
                break
            best_tags = select_tags()

        if best_tags is None:
            continue
        else:
            utils.touch("confirm_recruit")


def done_task(**kwargs):
    def done_tab(main_line=False):
        last_pos = None
        for i in range(12):  # Limit max loop time.
            if main_line:
                pos = utils.exists_now("receive_main_line")
            else:
                pos = utils.exists_now("receive")
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
    utils.try_touch("task_daily")
    done_tab()
    # weekly
    utils.try_touch("task_weekly")
    done_tab()
    # mainline not supported yet
    # utils.try_touch("task_main_line")
    # done_tab(main_line=True)


def gay_friends(**kwargs):
    print("正在与好友击♂剑...")
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

    # Wait for notifications to fade
    sleep(3)
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
        # manufacturing
        if drone.endswith("+"):
            pos = utils.touch("manufacturing_station")
            while not utils.try_touch("open_up_manufacturing"):
                # 防止刚好生产出来一个新的，导致没点进去。
                touch(pos)
            # 假设最多只有5个制造站
            for i in range(1, 6):
                utils.try_touch(f"0{i}", threshold=0.9)
                if utils.exists(drone):
                    utils.touch("drone_manufacturing", POSITION_CACHE)
                    utils.touch("max_drone", POSITION_CACHE)
                    utils.touch("ok", POSITION_CACHE)
                    utils.touch("gather", POSITION_CACHE)
                    break
            Navigator.go_back(2)
        # trade
        elif drone.endswith("-"):
            pos = utils.touch("trade")
            while not utils.try_touch("open_up_trade"):
                # 防止刚好有新订单，导致没点进去。
                touch(pos)
            for i in range(1, 6):
                utils.try_touch(f"0{i}", threshold=0.9)
                if utils.exists(drone):
                    while not utils.exists("0drone", threshold=0.9):
                        utils.touch("drone_trade", False)
                        utils.touch("max_drone", POSITION_CACHE)
                        utils.touch("ok", POSITION_CACHE)
                        utils.try_touch("deliver")
                    break


# for UI
TASKS = {
    "farm": {"function": farm, "str": "刷图({times})", "add_str": "+刷图",
             "config_template": {
                 "map": None,
                 "times": 0,
                 "auto_drink": False,
                 "auto_eat": False
             }},
    "recruit": {"function": recruit, "str": "收招募", "add_str": "+收招募"},
    "done_task": {"function": done_task, "str": "收任务", "add_str": "+收任务"},
    "gay_friends": {"function": gay_friends, "str": "好友击♂剑",
                    "add_str": "+基建信用"},
    "poke_wife": {"function": poke_wife, "str": "基建收菜({drone})",
                  "add_str": "+基建收菜", "config_template": {"drone": None}},
}


class TasksRunner:
    # TODO add scheduled task
    def __init__(self, serial_number, task_list, status):
        from farmer.view import Cache
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
        from farmer.view import Cache
        try:
            for task in self.task_list:
                self.status.set_status(self.status.RUNNING,
                                       task=TASKS[task["type"]]["str"].format(
                                           **(task.get("config")) or {}))
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


if __name__ == '__main__':
    pass
