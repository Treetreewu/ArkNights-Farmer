import threading
import time
from multiprocessing import Process, Queue, current_process, Pool
import tkinter
from configurator import conf, s
from airtest.core.android.adb import ADB







if __name__ == '__main__':
    # pool = Pool(1)
    # que = Queue()
    # Process(target=worker, args=(que,)).start()
    # add_task(que, add, 1, 2)
    # add_task(que, add, 1, 5)
    # que.put("STOP")
    from view import MainWindow
    main_window = MainWindow()
    # device detective thread
    main_window.main_loop()





