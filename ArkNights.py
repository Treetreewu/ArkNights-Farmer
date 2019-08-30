import sys
import os
import traceback
from airtest.core.api import sleep, touch, Template, wait, connect_device, auto_setup, exists, ST
from airtest.core.android.adb import ADB
import utils

welcome = """

  ___       _    _   _ _       _     _            _____       
 / _ \     | |  | \ | (_)     | |   | |          |  ___|   
/ /_\ \_ __| | _|  \| |_  __ _| |__ | |_ ___     | |_ __ _ _ __ _ __ ___   ___ _ __ 
|  _  | '__| |/ / . ` | |/ _` | '_ \| __/ __|    |  _/ _` | '__| '_ ` _ \ / _ \ '__|
| | | | |  |   <| |\  | | (_| | | | | |_\__ \    | || (_| | |  | | | | | |  __/ | 
\_| |_/_|  |_|\_\_| \_/_|\__, |_| |_|\__|___/    \_| \__,_|_|  |_| |_| |_|\___|_| 
                          __/ | 
                         |___/ 
______________________________________________________________________________________________________________________
|              -=          ==   ==                            =               =  +==                                 |
|              -=          ==   ==                           +=              =   =                                   |
|              .=          ==   ==                           =              -=  =.         _________________         |
|               =          ==   ==                          ==             -=  =-          |               |         |
|               =+         ==    ==                        .=             =  +=            (   咴 咴 咴 ！  )         |
|               +=         ==     =                        .=           ==   =             |_______________|         |
|                =-        ==     =+            +============          ==   =-                  /                    |
|                ==        ==     ==      ====.            ==        .=.   ==                  /                     |
|                 ==       ==      ==.===                  =-       ==    ====                /                      |
|                  ===     ==     ===.                     =-      ==    ==  ====            /                       |
|                  .=.==   ==  ===                         ==     =     ==      ===         /                        |
|                   += =+  ====                            .+   +=     +=         ===.                               |
|                    == ====                                          -=            .==                              |
|                     ====                                                            ===                            |
|                   -===                                                                ==.                          |
|                  ===                                      .                            ==.                         |
|                 ==+                                      =-                             .==                        |
|               +==                    =-                  ==                              +==                       |
|              -==                    ==                  ===                               ==+                      |
|             ==-                    ==+                 == -=                               ==                      |
|            ==                    += =+                 =   +=           +                   ==                     |
|           ==             -      =+  =+                ==    ==          =                   ==.                    |
|           =             =     ==    ==               -=       =         .-                  .==                    |
|          =+            =    +=      +=               =.  ==++=-=-       .=                   ==                    |
|         -=     =.     =-  ==.+===-   =.  +          ==          ==      =-                   -=                    |
|        .=      =      = ==           ==  ==        ==            ==     =-                    ==                   |
|        =-     +      ==+             .=. =.=      ==  -=========+  ==   =-                    ==                   |
|        =      =      =     .========  -===  =    +=  ================== =                     ==                   |
|       =+      =      =  .===========   =+    == +=  .=           ====-+=+                     ==                   |
|       =       =+     =  =                      .         ====          =                      =+                   |
|      ==       +=     =      ====                      +========-      =+                     -=-                   |
|      =.  -     =     =    ========                   ===========.    =-    -=             =  ==.                   |
|      =  ==      =    =  +==========                 .=========  =  .=.    =               = .==                    |
|      = -==      +=   =  ======== ==                 .========     .=   .==               =  ==                     |
|      =====        == =+ =======                     .===========.== +==.                -=  ==                     |
|       =+-=      ==  === ===========                  ===========   .=.                  =  ==                      |
|          ==    =.        =========                    .=======.   +=                   =+ ==                       |
|          +=   +=          ======+                              -===    =             === ==                        |
|           ==   ==                            =++               ==    =+             === ==                         |
|            =     ==                                           ==   =.             ==.===-                          |
|             =                                               ==+ +=             ===   =                --By Treewu  |
|____________________________________________________________________________________________________________________|

ArkNights Farmer V1.3
Site: https://github.com/Treetreewu/ArkNights-Farmer

啊...                          库奈次。
"""

ST.FIND_TIMEOUT = 5
BACK_POS = None
HOME_POS = None
SKIP_POS = None


def farm():
    limit = input("请输入次数(默认65535)：")
    try:
        limit = int(limit)
    except:
        limit = 65535
    if limit <= 0:
        limit = 65535

    event = False
    input("请把游戏置于要刷的图的地方，记得打开代理指挥。（按回车键开始）\n")
    for count in range(limit):
        print('\r', f"(。・∀・)ノ[{count + 1}]", end='', flush=True)
        if not utils.try_touch("start0", record_pos=(0.421, 0.201)):
            utils.try_touch("start0_event", record_pos=(0.4, 0.2))
        # if count == 0:
        #     if not utils.try_touch("start0", record_pos=(0.421, 0.201), resolution=(2160, 1080)):
        #         event = True
        #         print(event)
        #         utils.try_touch("start0_event", record_pos=(0.4, 0.2))
        # else:
        #     print(event)
        #     if event:
        #         utils.try_touch("start0_event", record_pos=(0.4, 0.2))
        #     else:
        #         utils.try_touch("start0", record_pos=(0.421, 0.201), resolution=(2160, 1080))
        sleep(2)
        try:
            utils.touch_image("start1", record_pos=(0.316, 0.101))
        except Exception as e:
            pos = exists(Template(utils.resource_path("image/cancel.png"), record_pos=(-0.269, 0.123), resolution=(2160, 1080)))
            if pos:
                print("\n你理智没了。")
                touch(pos)
                return
            else:
                raise e
        sleep(90)
        while True:
            try:
                pos = wait(Template(utils.resource_path("image/over.png"), record_pos=(-0.349, 0.189), resolution=(2160, 1080)), timeout=20, interval=5)
                sleep(3)
                touch(pos)
                break
            except:
                pass
            try:
                pos = wait(Template(utils.resource_path("image/upgrade.png"), record_pos=(-0.15, 0.011), resolution=(2160, 1080)), timeout=1)
                sleep(3)
                touch(pos)
                input("升级辣，请选图。（按回车键继续）")
            except:
                pass
            utils.try_touch("update_proxy", record_pos=(-0.292, -0.008))
    print()

def recruit():
    print("干员招募中...")
    pos = utils.exist_at_home("recruit", record_pos=(0.295, 0.109))
    if not pos:
        return
    touch(pos)
    while True:
        pos = exists(Template(utils.resource_path("image/hire.png"), resolution=(2160, 1080)))
        global SKIP_POS
        if pos:
            touch(pos)
            sleep(3)
            if not SKIP_POS:
                SKIP_POS = utils.touch_image("skip", record_pos=(0.459, -0.22))
            else:
                touch(SKIP_POS)
            sleep(4)
            touch(SKIP_POS)
        else:
            break


def done_task():
    def done_tab(main_line=False):
        last_pos = None
        while True:
            if main_line:
                pos = exists(Template(utils.resource_path("image/receive_main_line.png"), resolution=(2160, 1080)))
            else:
                pos = exists(Template(utils.resource_path("image/receive.png"), resolution=(2160, 1080), rgb=True, threshold=0.97))
            if pos:
                last_pos = pos
                touch(pos)
                sleep(1)
                if main_line:
                    touch(pos)
            elif last_pos:
                # 兼容领取奖励的点击。
                touch(last_pos)
                last_pos = None
            else:
                # 是真的没了。
                break
    print("任务收集中...")
    # 进入任务页
    pos = utils.exist_at_home("task", record_pos=(0.121, 0.161))
    if not pos:
        return
    touch(pos)
    # 进入日常任务
    utils.try_touch("task_daily", record_pos=(0.069, -0.225))
    done_tab()
    # 周常
    utils.try_touch("task_weekly", record_pos=(0.139, -0.225))
    done_tab()
    # 主线
    utils.try_touch("task_main_line", record_pos=(0.348, -0.226))
    done_tab(main_line=True)


def gay_friends():
    print("正在与好友基♂健...")
    pos = utils.exist_at_home("friends", record_pos=(-0.246, 0.15))
    if not pos:
        return
    touch(pos)
    utils.touch_image("friend_list", record_pos=(-0.415, -0.096))
    utils.touch_image("gay_friends", record_pos=(0.184, -0.133))
    sleep(5)
    while True:
        pos = utils.try_touch("gay_next", record_pos=(0.433, 0.183))
        if not pos:
            break
        sleep(3)


def poke_wife():
    # 之前竟然没有发现信赖可以批量收。。我都是一个一个戳的，所以起了这个名字。
    print("少女祈祷中...")

    def deliver_all():
        while utils.try_touch("deliver"):
            sleep(2)

    pos = utils.exist_at_home("gay", record_pos=(0.285, 0.176))
    if not pos:
        return
    else:
        touch(pos)
        sleep(5)
    # notification
    if utils.try_touch("notification", record_pos=(0.444, -0.184)):
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


TASK_INFO = {
    "1": {"fun": farm, "backs": 2, "in_gay": False},
    "2": {"fun": recruit, "backs": 1, "in_gay": False},
    "3": {"fun": poke_wife, "backs": 2, "in_gay": True},
    "4": {"fun": gay_friends, "backs": 2, "in_gay": True},
    "5": {"fun": done_task, "backs": 1, "in_gay": False},
    "6": {"fun": poke_wife, "backs": 2, "in_gay": True},
}


def main():
    task = input("""请选择功能:
    （默认2345, 现在可以顺序组合功能 例如 123，但有1时，1必须在第一位）
    1: 刷图
    2: 收招募
    3: 贸易站交付+制造站+收信赖
    4: 好友基♂建
    5: 收任务
""")
    if task == "":
        task = "2345"
    # check input
    while True:
        try:
            for i in task:
                if i not in TASK_INFO.keys():
                    raise ValueError
            if task.count("1") > 1 or (task.count("1") == 1 and not task.startswith("1")):
                raise ValueError
            break
        except:
            task = input("别闹，请重新输入：")
    # execute
    for t in task:
        TASK_INFO[t]["fun"]()
        # press_back(TASK_INFO[i]["backs"])
        # utils.go_home(TASK_INFO[t]["in_gay"])


if __name__ == '__main__':
    # connect
    print(welcome)
    print("开始互动 √\n")
    input("请打开USB调试(或网络调试)。（暂时只支持安卓设备）")

    adb = ADB()
    device_list = []
    ip_or_serial = ""
    for device in adb.devices():
        if device[1] == "device":
            device_list.append(device)
    if len(device_list) > 1:
        text = ""
        for index, device in enumerate(device_list):
            text += f"{index + 1}.{device[0]}\n"
        select = input(f"请选择设备：\n{text}")
        while True:
            try:
                select = int(select) - 1  # index = number - 1
                break
            except:
                select = input("别闹，请重新输入：")
        ip_or_serial = device_list[select][0]
    try:
        connect_device(f"android:///{ip_or_serial}?touch_method=adb")
    except:
        w = input("有线连接失败，是否使用局域网连接？(Y/n)  ")
        if w.lower() == "n" or w == "0":
            exit()
        ip_or_serial = input("请输入设备ip:port(默认:5555)  ")
        print("互动中……")
        ip_or_serial = ip_or_serial.replace("：", ":")
        try:
            if ADB(ip_or_serial).get_status() != "device":
                traceback.print_exc()
                print("互动失败，请尝试有线连接，或手动连接网络adb（adb connect {ip}）")
                os.system('pause')
                exit()
            connect_device(f"android:///{ip_or_serial}?touch_method=adb")
        except:
            traceback.print_exc()
            print("互动失败，请尝试有线连接，或手动连接网络adb（adb connect {ip}）")
            exit()
    auto_setup(__file__)
    print(f"互动成功！（〃｀ 3′〃） {ip_or_serial}")

    while True:
        try:
            main()
            utils.go_home()
            print("\n")
            print("成了！╰(￣ω￣ｏ)")
        except KeyboardInterrupt:
            break
        except:
            traceback.print_exc()
            print()
            print("没成……〒▽〒")
        os.system('pause')

