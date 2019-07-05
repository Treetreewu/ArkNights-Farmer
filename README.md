# ArkNights-Farmer
## 介绍
亲爱的刀库塔，你好！<br>

这位农民是基于[Airtest项目](https://airtest.netease.com/)([GitHub](https://github.com/AirtestProject/Airtest))编写的，release使用[pyinstaller](https://www.pyinstaller.org/)打包。<br>
目前功能有：<br>
>1: 刷图<br>
 2: 聘用公开招募<br>
 3: 领取已完成的任务<br>
 4: 访问好友基♂建<br>

## 运行
目前release提供了Windows平台的可执行文件。
然而，如果你有完整的Python3 + Airtest环境，那么你将可以仅运行ArkNights.py脚本来工作（当然，image目录是必须的）。
## 构建
安装了pyinstaller，
```sh
pip install pyinstaller
```
你可以运行<br>
```sh
pyinstaller ArkNights.spec
```
来构建。<br><br>
对于Windows以外的其他平台，**理论上**只需要在airtest\core\android\static\adb\添加对应平台的[adb binary](https://github.com/AirtestProject/Airtest/tree/master/airtest/core/android/static/adb)即可。（这里为了减少体积，没有搞进去）<br><br>
如果想要修改构建参数，请参考[pyinstaller文档](https://www.pyinstaller.org/documentation.html)。
## 已知问题
~~收取任务时，如果奖励已经领完，而任务未领完，仍有可能被识别到，导致死循环在这。（没试过究竟会不会，也懒得修了）~~(已修复)<br>
~~主线任务和~~见习任务的自动领取还**没有实现**。
## TODO
>制造站收取 和 贸易站交付<br>
 信赖收集（不知道怎么搞，难顶）<br>
 线索收集<br>
 信用收集（没必要）<br>
 干员进驻调整<br>
 公开招募智能[选标签](http://wiki.joyme.com/arknights/%E5%B9%B2%E5%91%98%E6%95%B0%E6%8D%AE%E8%A1%A8)（联络？）<br>
 etc.

## FAQ
### 关于静默安装的apk
 RotationWatcher：用于监测屏幕旋转，确保点击位置的正确性。<br>
 Yosemite：一个没有界面的输入法，用于输入文字（废话）[本项目虽然没有用到这个，但是这是Airtest初始化设备的一部分]。<br><br>
 以上两个应用均来源于[Airtest项目](https://airtest.netease.com/)，<br>
 且仅在运行有用。强迫症患者可以写一个脚本退出时自动卸载。
 
### 在使用中出现问题？
请先尝试理解如下知识：<br>
>[adb](https://developer.android.com/studio/command-line/adb?hl=zh-cn)连接方式<br>
 好友[基♂建](http://wiki.joyme.com/arknights/%E5%9F%BA%E5%BB%BA)<br>
 [~~养驴技术~~](https://item.jd.com/39923508902.html)
### 没有电脑？
对于想要单手机运行的用户，请修改部分代码并用[Firebase打包](https://airtest.netease.com/docs/docs_AirtestIDE-zh_CN/8_plugins/1_firebase.html)（执行需要adb或root权限。）<br>
如果可以pull一个更好，我代表有需要的人感谢你：谢谢你，刀库塔！
### 需要其他功能？
>告诉我试试(不一定生效)。<br>
>学习相关知识，提交pr(大概率生效)。
