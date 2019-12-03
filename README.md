# ArkNights-Farmer
[![996.icu](https://img.shields.io/badge/link-996.icu-red.svg)](https://996.icu)

## 介绍

亲爱的刀库塔，你好！

这位农民是基于[Airtest项目](https://airtest.netease.com/)([GitHub](https://github.com/AirtestProject/Airtest))编写的，release使用[pyinstaller](https://www.pyinstaller.org/)打包。
目前功能有:

1. 刷图（自动使用理智合剂/源石）
2. 聘用公开招募
3. 领取已完成的任务
4. 访问好友基♂建获取信用
5. 贸易站交付+制造站收取+信赖收取（自动使用无人机）

### 欢迎进群交♂流

[928918804](https://jq.qq.com/?_wv=1027&k=5TUmy9F)

![qq_group_qr](https://github.com/Treetreewu/ArkNights-Farmer/raw/master/image/gui/qqgroup_qr.jpg)

## 运行

目前release提供了Windows平台的可执行文件。
然而，如果你有完整的Python3 + Airtest环境，那么你将可以仅运行ArkNights.py脚本来工作（当然，image目录是必须的）。

## 构建

安装了pyinstaller，

```sh
pip install pyinstaller
```

你可以运行

```sh
pyinstaller ArkNights.spec
```

来构建。

对于Windows以外的其他平台，**理论上**只需要在airtest\core\android\static\adb\添加对应平台的[adb binary](https://github.com/AirtestProject/Airtest/tree/master/airtest/core/android/static/adb)即可。（这里为了减小体积，没有搞进去）

如果想要修改构建参数，请参考[pyinstaller文档](https://www.pyinstaller.org/documentation.html)。

## 已知问题

见习任务的自动领取还**没有实现**。
浮动通知有时(小概率)会挡住点击的位置，建议开始前打开勿扰模式或关闭浮动通知。

## TODOs

之后可能会做，也可能永远留在TODO里。。

1. 支持命令行调用
2. 刷图时可指定地图
3. 公开招募自动[选标签](http://wiki.joyme.com/arknights/%E5%B9%B2%E5%91%98%E6%95%B0%E6%8D%AE%E8%A1%A8)
4. 自动更换基建疲劳干员
5. 定时/计划执行
6. 软件自动更新
7. 任务列表右键菜单中的新增/剪切/复制/粘贴
8. 保存上次连接的设备/网络adb设备
9. 编辑子任务
10. 皮肤系统
11. 依状态禁用或启用部分UI元素，防止误操作

## FAQ

### 关于静默安装的apk

RotationWatcher：用于监测屏幕旋转，确保点击位置的正确性。  
Yosemite：一个没有界面的输入法，用于输入文字（废话）[本项目虽然没有用到这个，但是这是Airtest初始化设备的一部分]。

以上两个应用均来源于[Airtest项目](https://airtest.netease.com/)，且仅在运行有用。强迫症患者可以写一个脚本退出时自动卸载。

### 在使用中出现问题？

请先尝试理解如下知识：

1. [adb](https://developer.android.com/studio/command-line/adb?hl=zh-cn)连接方式
2. 好友[基♂建](http://wiki.joyme.com/arknights/%E5%9F%BA%E5%BB%BA)
3. [~~养驴技术~~](https://item.jd.com/39923508902.html)

#### 发现bug

麻烦提个issue或者以其他方式告诉我。



### 没有电脑？

对于想要单手机运行的用户，请修改部分代码并用[Firebase打包](https://airtest.netease.com/docs/docs_AirtestIDE-zh_CN/8_plugins/1_firebase.html)（执行需要adb或root权限。）

### 需要其他功能？

告诉我试试(不一定生效)。
欢迎Pull Request。


