# ArkNights-Farmer
## 介绍
亲爱的刀库塔，你好！<br>

这位农民是基于[Airtest项目](https://airtest.netease.com/)([GitHub](https://github.com/AirtestProject/Airtest))编写的。<br>
目前功能有：<br>
>1: 刷图<br>
 2: 聘用公开招募<br>
 3: 领取已完成的任务<br>
 4: 访问好友基♂建<br>

## 运行
目前release提供了Windows平台的可执行文件。
然而，如果你有完整的Airtest环境，那么你将可以仅运行ArkNights.py脚本来工作（当然，image目录是必须的）。
## 构建
安装了pyinstaller，
```sh
pip install pyinstaller
```
你可以运行<br>
```sh
pyinstaller ArkNights.spec
```
来构建。<br>
如果想要修改构建参数，请参考[pyinstaller文档](https://www.pyinstaller.org/documentation.html)。
## 已知问题
收取任务时，如果奖励已经领完，而任务未领完，仍有可能被识别到，导致死循环在这。（没试过究竟会不会，也懒得修了）<br>
主线任务 和 另一个忘了叫啥的任务 的自动领取**没有实现**

##FAQ
###在使用中出现问题？
请先尝试理解如下知识：<br>
>[adb](https://developer.android.com/studio/command-line/adb?hl=zh-cn)连接方式<br>
 好友[基♂建](http://wiki.joyme.com/arknights/%E5%9F%BA%E5%BB%BA)<br>
 [养驴技术](https://item.jd.com/39923508902.html)

###TODO
>制造站收取 和 贸易站交付<br>
 信赖收集（不知道怎么搞，难顶）<br>
 收集线索<br>
 干员进驻调整<br>
 公开招募自动[选标签](http://wiki.joyme.com/arknights/%E5%B9%B2%E5%91%98%E6%95%B0%E6%8D%AE%E8%A1%A8)（联络？）
 
###需要其他功能？
>告诉我试试(不一定生效)。<br>
>学习相关知识，提交pr(大概率生效)。
