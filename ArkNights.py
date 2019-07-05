import sys
import os
import traceback
from airtest.core.api import sleep, touch, Template, wait, connect_device, auto_setup, exists

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

ArkNights Farmer V1.2
Site: https://github.com/Treetreewu/ArkNights-Farmer

啊...                          库奈次。
"""

BACK_POS = None
HOME_POS = None
SKIP_POS = None


def farm():
    limit = input("请输入次数(默认65535)：")
    try:
        limit = int(limit)
    except:
        limit = 65535
    if limit == 0:
        limit = 65535

    input("请把游戏置于要刷的图的地方，记得打开代理指挥。\n")
    for count in range(limit):
        print('\r', "(。・∀・)ノ[{}]".format(count + 1), end='', flush=True)
        touch(Template(resource_path("image/tpl1562289614567.png"), record_pos=(0.421, 0.201), resolution=(2160, 1080)))
        touch(Template(resource_path("image/tpl1560329003844.png"), record_pos=(0.316, 0.101), resolution=(2160, 1080)))
        sleep(90)
        while True:
            try:
                pos = wait(Template(resource_path("image/tpl1560328980657.png"), record_pos=(-0.349, 0.189), resolution=(2160, 1080)), timeout=20, interval=5)
                sleep(3)
                touch(pos)
                break
            except:
                pass
            try:
                pos = wait(Template(resource_path("image/tpl1560328943334.png"), record_pos=(-0.15, 0.011), resolution=(2160, 1080)), timeout=1)
                sleep(3)
                touch(pos)
            except:
                pass
            try:
                pos = wait(Template(resource_path("image/tpl1562126367719.png"), record_pos=(-0.292, -0.008), resolution=(2160, 1080)), timeout=1)
                touch(pos)
            except:
                pass


def recruit():
    pos = exists(Template(resource_path("image/tpl1561945272209.png"), record_pos=(0.295, 0.109), resolution=(2160, 1080)))
    if not pos:
        print("放在主页哦~亲。")
        return
    touch(pos)
    while True:
        pos = exists(Template(resource_path("image/tpl1561945278845.png"), record_pos=(-0.216, 0.016), resolution=(2160, 1080)))
        global SKIP_POS
        if pos:
            touch(pos)
            sleep(3)
            if not SKIP_POS:
                SKIP_POS = touch(Template(resource_path("image/tpl1561945291549.png"), record_pos=(0.459, -0.22), resolution=(2160, 1080)))
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
                pos = exists(Template(resource_path("image/tpl1562294702538.png"), record_pos=(0.295, -0.151), resolution=(2160, 1080)))
            else:
                pos = exists(Template(resource_path("image/tpl1562122652880.png"), record_pos=(0.295, -0.151), resolution=(2160, 1080), rgb=True, threshold=0.97))
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
    # 进入任务页
    pos = exists(Template(resource_path("image/tpl1561945262063.png"), record_pos=(0.121, 0.161), resolution=(2160, 1080)))
    if not pos:
        print("放在主页哦~亲。")
        return
    touch(pos)
    # 进入日常任务
    daily = exists(Template(resource_path("image/tpl1562295119847.png"), record_pos=(0.069, -0.225), resolution=(2160, 1080)))
    if daily:
        touch(daily)
    done_tab()
    # 周常
    touch(Template(resource_path("image/tpl1562141815104.png"), record_pos=(0.139, -0.225), resolution=(2160, 1080)))
    done_tab()
    # 主线
    touch(Template(resource_path("image/tpl1562295279615.png"), record_pos=(0.348, -0.226), resolution=(2160, 1080)))
    done_tab(main_line=True)


def gay_friends():
    pos = exists(Template(resource_path("image/tpl1562121233580.png"), record_pos=(-0.246, 0.15), resolution=(2160, 1080)))
    if not pos:
        print("放在主页哦~亲。")
        return
    touch(pos)
    touch(Template(resource_path("image/tpl1562121247202.png"), record_pos=(-0.415, -0.096), resolution=(2160, 1080)))
    touch(Template(resource_path("image/tpl1562121289070.png"), record_pos=(0.184, -0.133), resolution=(2160, 1080)))
    sleep(5)
    while True:
        pos = exists(Template(resource_path("image/tpl1562117180144.png"), record_pos=(0.433, 0.183), resolution=(2160, 1080)))
        if pos:
            touch(pos)
            sleep(3)
        else:
            break


def poke_wife():
    pass


def press_back(times):
    global BACK_POS
    for i in range(times):
        if BACK_POS:
            touch(BACK_POS)
        else:
            BACK_POS = touch(Template(resource_path("image/tpl1562117190883.png"), record_pos=(-0.441, -0.223), resolution=(2160, 1080)))
        sleep(0.5)


def go_home(in_gay=False):
    global HOME_POS
    if HOME_POS and False:
        touch(HOME_POS[0])
        sleep(1)
        touch(HOME_POS[1])
    else:
        HOME_POS = [
            touch(Template(resource_path("image/tpl1562119328762.png"), record_pos=(-0.312, -0.223), resolution=(2160, 1080))),
            touch(Template(resource_path("image/tpl1562119339267.png"), record_pos=(-0.38, -0.088), resolution=(2160, 1080)))
        ]
    sleep(0.5)
    if in_gay:
        pos = exists(Template(resource_path("image/tpl1562120546615.png"), record_pos=(0.176, 0.1), resolution=(2160, 1080)))
        if pos:
            touch(pos)
        sleep(5)


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


TASK_INFO = {
    "1": {"fun": farm, "backs": 2, "in_gay": False},
    "2": {"fun": recruit, "backs": 1, "in_gay": False},
    "3": {"fun": done_task, "backs": 1, "in_gay": False},
    "4": {"fun": gay_friends, "backs": 2, "in_gay": True},
    "5": {"fun": poke_wife, "backs": 2, "in_gay": True},
}


def main():
    task = input("""请选择功能:
    （默认234, 现在可以顺序组合功能 例如 123，但有1时，1必须在第一位）
    1: 刷图
    2: 收招募
    3: 收任务
    4: 好友基♂建
    5: (TODO) 收信赖(这个太难写了，不写了。)
""")
    if task == "":
        task = "234"
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
        go_home(TASK_INFO[t]["in_gay"])


if __name__ == '__main__':
    # connect
    print(welcome)
    print("开始互动 √\n")
    input("请打开USB调试(或网络调试)。（暂时只支持安卓设备）")
    try:
        connect_device("android:///")
    except:
        w = input("有线连接失败，是否使用局域网连接？(Y/n)  ")
        if w.lower() == "n" or w == "0":
            exit()
        ip = input("请输入设备ip[:port(默认:5555)]  ")
        print("互动中……")
        ip = ip.replace("：", ":")
        try:
            os.system(resource_path("airtest\\core\\android\\static\\adb\\windows\\adb.exe") + " connect {}".format(ip))
            connect_device("android:///{}".format(ip))
        except:
            print("互动失败，请尝试有线连接，或手动连接网络adb（adb connect {ip}）")
            exit()
    auto_setup(__file__)
    print("互动成功！（〃｀ 3′〃）")

    while True:
        try:
            main()
            print("\n")
            print("成了！╰(￣ω￣ｏ)")
        except KeyboardInterrupt:
            break
        except:
            traceback.print_exc()
            print()
            print("没成……〒▽〒")
        os.system('pause')

