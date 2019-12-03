class BaseStrings:
    version = "V2.0.5"
    version_sub = ""
    title = f"ArkNights-Farmer {version}{version_sub}"
    hello_title = "注意"
    hello_info = "本应用完全免费，如果你通过任何渠道购买获得，就很气。对此，作者建议对贩售人员*龙门粗口*，并威胁他向作者捐赠源石。"
    farm = "刷图"
    gay = "基建"
    task_list = ""
    customized_task = "自定义"
    refresh_adb = "刷新"
    add_net_adb = "添加网络adb"
    net_adb_hint = "请输入设备ip:端口，默认端口5555"
    no_device = "无设备, 请打开adb调试"
    loading = "启动中..."
    connecting = "连接中..."
    ok = "确定"
    donate = "请作者吃源石(不是)"
    donate_title = "捐赠"
    github = "Github主页"
    github_url = "https://github.com/Treetreewu/ArkNights-Farmer"
    github_release_url = "https://github.com/Treetreewu/ArkNights-Farmer/releases"
    check_update = "检查更新（手动）"
    default = "默认"
    warning = "警告"
    error = "出错辽"
    broken_file_warning = "配置文件错误，使用默认配置。"
    auto_drink = "自动使用理智合剂"
    auto_eat = "自动嗑石头(慎点)"
    use_drone = "自动使用无人机加速"
    running = "执行中 {task}"
    ready = "就绪"
    error_input = "输入有误嗷。"
    error_reason_run_out = ""
    error_task_running = "当前正在运行任务嗷。"
    error_device_fail = "设备初始化失败，重新连接试试。"
    error_no_device = "没设备嗷。"
    delete = "删除"
    start = "开始"
    drone_produce = "加速制造"
    drone_bill = "加速订单"
    gold = "赤金"
    record = "中级作战记录"
    stone_debris = "源石碎片"
    reason_run_out = ""





class BaseColors:
    c1 = 100


class BasePictures:
    p1 = None


class Default:
    name = "默认"

    class Strings(BaseStrings):
        pass

    class Colors(BaseColors):
        pass

    class Pictures(BasePictures):
        pass


class JOJO:
    class Strings(BaseStrings):
        pass

    class Colors(BaseColors):
        pass

    class Pictures(BasePictures):
        pass


class DragonFruit:
    name = "红心火龙果"

    class Strings(BaseStrings):
        pass

    class Colors(BaseColors):
        pass

    class Pictures(BasePictures):
        pass


ENABLED_SKINS = [Default, JOJO, DragonFruit]


if __name__ == '__main__':
    print(hasattr(Default, "name"))
