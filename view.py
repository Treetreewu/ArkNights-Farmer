import json
import re
import threading
import time
import tkinter as tk
from tkinter import filedialog
from webbrowser import open as open_with_browser
from tkinter import messagebox, ttk, Toplevel

from airtest.core.android.adb import ADB
from airtest.core.error import AdbError

from configurator import conf, s
from multiprocessing import Process, freeze_support
from threading import Thread

from skins import ENABLED_SKINS
from tasks import TasksRunner, TASKS, TaskRunningError, DeviceError
from utils import StringUtils, resource_path


class DragDropListbox(tk.Listbox):
    """ A Tkinter listbox with drag'n'drop reordering of entries. """
    def __init__(self, master, bind_list=None, right_menu_list=None, **kwargs):
        """
        # TODO right click menu add cut, copy and paste.
        :param master:
        :param bind_list:
        :param right_menu_list: reserve for adding other menu
        :param kwargs:
        """
        if bind_list is None:
            bind_list = []
        self.list = bind_list
        kwargs['selectmode'] = tk.SINGLE
        super().__init__(master, **kwargs)
        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(label=s.delete, command=self.menu_delete)
        if right_menu_list:
            for item in right_menu_list:
                self.popup_menu.add_command(label=item[0], command=item[1])
        self.bind('<B1-Motion>', self.shift_selection)
        self.bind('<ButtonRelease-1>', conf.save)
        self.bind('<Button-3>', self.right_menu)
        self.bind('<Delete>', lambda event: self.menu_delete())

    def right_menu(self, event):
        self.selection_clear(0, tk.END)
        self.selection_set(self.nearest(event.y))
        self.popup_menu.post(event.x_root, event.y_root)

    def update_display(self):
        self.delete(0, tk.END)
        self.insert(tk.END, *[self.item2str(item) for item in self.list])

    def menu_delete(self, first=None, last=None):
        if not first:
            curselection = self.curselection()
            if not curselection:
                return
            first = curselection[0]
        self.delete(first, last)
        if not last or last == "end":
            last = first
        for i in range(first, last+1):
            self.list.pop(first)
        conf.save()

    @staticmethod
    def item2str(item):
        """
        What to display in list (item in list to string)
        :param item: item in self.list
        :return:
        """
        return item.__str__()

    def shift_selection(self, event):
        i = self.nearest(event.y)
        if i < self.curselection()[0]:
            # move display
            x = self.get(i)
            self.delete(i)
            self.insert(i + 1, x)
            self.select_set(i)
            # move list
            x = self.list.pop(i)
            self.list.insert(i + 1, x)
        elif i > self.curselection()[0]:
            # move display
            x = self.get(i)
            self.delete(i)
            self.insert(i - 1, x)
            self.select_set(i)
            # move list
            x = self.list.pop(i)
            self.list.insert(i - 1, x)


class BaseDialogWindow:
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.tk = Toplevel(parent.tk, **kwargs)
        self.tk.resizable(False, False)
        self.tk.grab_set()
        self.tk.lift()
        self.tk.focus_set()
        # self.tk.attributes('-topmost', 'true')


class FarmTaskWindow(BaseDialogWindow):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.tk.title(s.farm)
        self.map_ = ttk.Entry(self.tk)
        self.times = ttk.Spinbox(self.tk, from_=0, to=9999999999, width=5)
        self.times.set(0)
        self.auto_drink_var = tk.IntVar(self.tk, value=0)
        self.auto_drink = ttk.Checkbutton(self.tk, text=s.auto_drink, variable=self.auto_drink_var)
        self.auto_eat_var = tk.IntVar(self.tk, value=0)
        self.auto_eat = ttk.Checkbutton(self.tk, text=s.auto_eat, variable=self.auto_eat_var)
        self.button = ttk.Button(self.tk, text=s.ok, command=self.on_submit)

        # self.map_.pack(padx=10, pady=(15, 0))
        self.auto_drink.pack(padx=10, pady=(10, 0))
        self.auto_eat.pack(padx=10, pady=(10, 0))
        self.times.pack(side=tk.LEFT, padx=(20, 10), pady=10)
        self.button.pack(side=tk.LEFT, padx=(10, 20), pady=10, ipady=5)

    def on_submit(self):
        try:
            config = {
                # TODO specify map
                "map": None,
                "times": int(self.times.get()),
                "auto_drink": bool(self.auto_drink_var.get()),
                "auto_eat": bool(self.auto_eat_var.get()),
            }
        except ValueError:
            messagebox.showerror(s.error, s.input_wrong)
            return
        self.parent.add_task("farm", config)
        self.tk.destroy()


class GayWindow(BaseDialogWindow):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.tk.title(s.gay)
        self.auto_drone_var = tk.IntVar(self.tk, value=0)
        self.auto_drone = ttk.Checkbutton(self.tk, text=s.use_drone, variable=self.auto_drone_var, command=self.on_auto_drone_change)

        # select drone frame of 2 OptionMenus
        self.drone_frame = BaseFrame(self.tk)
        self.drone_var = tk.StringVar(self.drone_frame.tk)
        self.drone = ttk.OptionMenu(
            self.tk, self.drone_var, s.drone_bill, *[s.drone_bill, s.drone_produce], command=self.update_drone_detail
        )
        self.drone.configure(state="disabled")
        self.drone_detail_var = tk.StringVar(self.drone_frame.tk)
        self.drone_detail = ttk.OptionMenu(self.drone_frame.tk, self.drone_detail_var)
        self.drone_detail.configure(state="disabled")
        self.update_drone_detail(s.drone_bill)


        self.button = ttk.Button(self.tk, text=s.ok, command=self.on_submit)

        self.auto_drone.pack(padx=15, pady=(15, 0))
        self.drone_frame.pack(padx=15, pady=(15, 0))
        self.button.pack(padx=(10, 20), pady=10, ipady=5)

    def on_auto_drone_change(self):
        if self.auto_drone_var.get():
            self.drone.configure(state="normal")
            self.drone_detail.configure(state="normal")
            self.drone.pack(side=tk.LEFT, in_=self.drone_frame.tk)
            self.drone_detail.pack(side=tk.LEFT, in_=self.drone_frame.tk)
        else:
            self.drone.configure(state="disabled")
            self.drone_detail.configure(state="disabled")
            self.drone.pack_forget()
            self.drone_detail.pack_forget()

    def update_drone_detail(self, drone):
        if drone == s.drone_bill:
            detail_list = [s.gold, s.stone_debris]
            self.drone_detail.set_menu()
        elif drone == s.drone_produce:
            detail_list = [s.gold, s.stone_debris, s.record]
            pass
        else:
            return
        self.drone_detail.set_menu(detail_list[0], *detail_list)

    def on_submit(self):
        result = None
        if self.auto_drone_var.get():
            drone_var = self.drone_var.get()
            drone_detail_var = self.drone_detail_var.get()
            if drone_var == s.drone_bill:
                result = "-"
            elif drone_var == s.drone_produce:
                result = "+"
            if drone_detail_var == s.gold:
                result = "gold" + result
            elif drone_detail_var == s.record:
                result = "record" + result
            elif drone_detail_var == s.stone_debris:
                result = "stone" + result

        self.parent.add_task("poke_wife", {"drone": result})
        self.tk.destroy()


class NetADBWindow(BaseDialogWindow):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.adb = parent.adb
        self.tk.title(s.add_net_adb)
        # self.tk.geometry("300x200")
        self.label = ttk.Label(self.tk, text=s.net_adb_hint)
        self.label.pack(padx=20, pady=20)
        self.entry = ttk.Entry(self.tk, validate="key")  # validatecommand=self.validate_net_adb)
        self.entry.pack(padx=20)
        self.button = ttk.Button(self.tk, text=s.ok, command=self.add_net_adb)
        self.button.pack(side=tk.BOTTOM, pady=20)

        self.tk.protocol("WM_DELETE_WINDOW", self.destroy)

    @staticmethod
    def validate_net_adb():
        """
        TODO: for future use.
        :return:
        """
        return True

    def destroy(self):
        self.parent.update_devices()
        self.tk.destroy()

    def add_net_adb(self):
        self.button.text = s.connecting
        self.adb.serialno = StringUtils.parse_net_adb(self.entry.get())
        self.adb.connect()

        # TODO: save and restore net adb connection.
        if self.adb.serialno not in conf.config["net_devices"]:
            conf.config["net_devices"].append(self.adb.serialno)
            conf.save()

        self.destroy()


class DonationWindow(BaseDialogWindow):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.tk.title(s.donate_title)
        from PIL import Image, ImageTk
        wechat_qr_png = ImageTk.PhotoImage(Image.open(resource_path("image/gui/wechat_qr.png")))
        alipay_qr_png = ImageTk.PhotoImage(Image.open(resource_path("image/gui/alipay_qr.png")))
        self.wechat_qr = tk.Label(self.tk, image=wechat_qr_png)
        self.alipay_qr = tk.Label(self.tk, image=alipay_qr_png)
        self.wechat_qr.image = wechat_qr_png
        self.alipay_qr.image = alipay_qr_png
        self.wechat_qr.pack(side=tk.LEFT)
        self.alipay_qr.pack()


class BaseFrame:
    def __init__(self, parent, **kwargs):
        self.parent = parent
        try:
            self.tk = ttk.Frame(self.parent.tk, **kwargs)
        except AttributeError:
            self.tk = ttk.Frame(self.parent, **kwargs)
        self.pack = self.tk.pack_configure


class BottomBarFrame(BaseFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.adb = self.parent.adb
        self.device_menu_var = tk.StringVar(self.tk)
        self.device_menu = ttk.OptionMenu(self.tk, self.device_menu_var, direction='above',
                                          command=self.on_device_menu_select)
        self.device_menu.pack(side=tk.RIGHT, in_=self.tk)

        self.status_bar = ttk.Label(textvariable=self.parent.status.status_var)
        self.status_bar.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True, in_=self.tk)

    def on_device_menu_select(self, select):
        if select == s.add_net_adb:
            NetADBWindow(self)
        elif select == s.refresh_adb:
            self.update_devices()
        elif ":" in select:
            # check net adb device status
            self.adb.serialno = select
            try:
                self.adb.connect()
                if not self.adb.get_status() == "device":
                    self.update_devices()
            except AdbError:
                self.update_devices()

    def update_devices(self, background=True):
        def update():
            device_list = []
            for device in self.adb.devices():
                if device[1] == "device":
                    serial = device[0]
                    self.adb.serialno = serial
                    try:
                        device_list.append(f"{self.adb.get_model()} ({serial})")
                    except AdbError:
                        pass

            Cache.devices = device_list
            self.device_menu.set_menu(None, *device_list,
                                      s.add_net_adb, s.refresh_adb)
            if device_list:
                self.device_menu['menu'].insert_separator(len(device_list))
                self.device_menu_var.set(device_list[0])
            else:
                self.device_menu_var.set(s.no_device)

        if background:
            self.device_menu_var.set(s.connecting)
            threading.Thread(target=update).start()
        else:
            update()


class CustomTaskFrame(BaseFrame):
    # TODO add cut/copy/paste.
    def __init__(self, parent):
        super().__init__(parent)
        self.custom_task_list = DragDropListbox(self.tk, conf.config["custom_tasks"], exportselection=0)
        self.custom_task_list.item2str = lambda task: task["name"]
        self.custom_task_list.update_display()
        self.custom_task_list.bind("<<ListboxSelect>>", self.on_select)
        self.custom_task_list.bind("<Double-Button-1>", self.run)
        self.custom_task_list.pack(fill=tk.BOTH, expand=True, in_=self.tk)

        self.start_button = ttk.Button(self.tk, text=s.start, command=self.run)
        self.start_button.pack(in_=self.tk, ipady=6, fill=tk.BOTH)
        self.selection = None
        if self.custom_task_list.list:
            self.custom_task_list.select_set(0)
            self.selection = 0

    def on_select(self, _=None):
        curselection = self.custom_task_list.curselection()
        if curselection:  # and self.selection != curselection[0]:
            self.selection = curselection[0]
            self.parent.task.update()

    def run(self, _=None):
        if self.selection is None:
            return

        try:
            serial_number = re.search("\\((.*?)\\)$", self.parent.bottom_bar.device_menu_var.get()).group(1)
        except:
            messagebox.showerror(s.error, s.error_no_device)
            return
        try:
            TasksRunner(
                serial_number,
                self.parent.task.task_list.list,
                self.parent.status
            ).run()
        except Exception as e:
            messagebox.showerror(s.error, e.__str__())


class TaskFrame(BaseFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.task_list = DragDropListbox(self.tk, exportselection=0)
        self.task_list.item2str = lambda task: TASKS[task["type"]]["str"].format(**(task.get("config")) or {})
        self.update()
        # TODO edit task
        # self.task_list.bind("<Double-Button-1>", command=edit_task)
        self.task_list.pack(fill=tk.BOTH, expand=True, in_=self.tk)
        self.buttons = TaskButtonsFrame(self)
        self.buttons.pack(fill=tk.BOTH, in_=self.tk)

    def update(self):
        if self.parent.custom_task.selection is None:
            self.task_list.list = []
        self.task_list.list = conf.config["custom_tasks"][self.parent.custom_task.selection]["tasks"]
        self.task_list.update_display()

    def set_done(self):
        # TODO show status of single task.
        pass

    def clear_status(self):
        # TODO clear status of all tasks.
        pass


class TaskButtonsFrame(BaseFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.button_list = []

        for t in TASKS:
            button = ttk.Button(text=TASKS[t]["add_str"], command=self.on_click(t))
            button.pack(side=tk.LEFT, in_=self.tk, expand=True, fill=tk.BOTH, ipady=6)
            self.button_list.append(button)

    def on_click(self, task):
        """
        replace lambda to avoid a weird bug.
        :param task:
        :return:
        """
        def add():
            print(task)
            task_windows = {
                "farm": FarmTaskWindow,
                "poke_wife": GayWindow,
            }
            window = task_windows.get(task)
            if window:
                window(self)
            else:
                self.add_task(task)
        return add

    def add_task(self, task, config=None):
        body = {
          "type": task
        }
        if config:
            body["config"] = config
        curselection = self.parent.task_list.curselection()
        if curselection:
            self.parent.task_list.list.insert(curselection[0], body)
        else:
            self.parent.task_list.list.append(body)
        conf.save()
        self.parent.update()


class MenuBar:
    """
    菜单栏
    """

    def __init__(self, parent):
        self.parent = parent
        self.tk = tk.Menu(parent.tk)

        self.file_menu = tk.Menu(self.tk, tearoff=0)
        self.file_menu.add_command(label="导出配置", command=conf.export)
        self.file_menu.add_command(label="导入配置", command=conf.import_)
        self.file_menu.add_command(label="恢复默认配置", command=conf.reset)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="退出")

        self.skin_menu = tk.Menu(self.tk, tearoff=0)
        self.skin_var = tk.IntVar()
        for index, skin in enumerate(ENABLED_SKINS):
            self.skin_menu.add_radiobutton(
                label=skin.name if hasattr(skin, "name") else skin.__name__,
                command=lambda: self.parent.refresh_skin(skin),
                variable=self.skin_var, value=index
            )
            if skin.__name__ == conf.config["skin"]:
                self.skin_var.set(index)

        self.about_menu = tk.Menu(self.tk, tearoff=0)
        self.about_menu.add_command(label=s.donate, command=lambda: DonationWindow(self.parent))
        # TODO: auto update software.
        self.about_menu.add_command(label=s.check_update, command=lambda: open_with_browser(s.github_release_url))
        self.about_menu.add_command(label=s.github, command=lambda: open_with_browser(s.github_url))

        self.tk.add_cascade(label="文件", menu=self.file_menu)
        # TODO change skin.
        # self.tk.add_cascade(label="皮肤", menu=self.skin_menu)
        self.tk.add_cascade(label="关于", menu=self.about_menu)


class MainWindow:
    def __init__(self):
        self.adb = ADB()
        self.tk = tk.Tk()
        self.tk.title(s.title)
        # self.icon = tk.PhotoImage(file=resource_path("image/gui/sora.png"))
        self.tk.iconbitmap(resource_path("image/gui/sora.ico"))
        # self.tk.geometry('500x300')
        self.status = Status(self)

        # menu bar
        self.menu_bar = MenuBar(self)
        self.tk.config(menu=self.menu_bar.tk)

        # bottom bar
        self.bottom_bar = BottomBarFrame(self)
        self.bottom_bar.pack(side=tk.BOTTOM, fill=tk.BOTH)
        self.update_devices = self.bottom_bar.update_devices

        # custom task list
        self.custom_task = CustomTaskFrame(self)
        self.custom_task.pack(side=tk.LEFT, fill=tk.BOTH)

        # inner child task list
        self.task = TaskFrame(self)
        self.task.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # init
        self.update_devices()
        self.status.set_status(Status.READY)

    def main_loop(self, n=0):
        self.tk.mainloop(n)

    def refresh_skin(self, skin_class):
        conf.config["skin"] = skin_class.__name__
        # TODO: reload conf to change skin.
        # TODO: how to reload window?


class Status:
    LOADING = 0
    READY = 1
    RUNNING = 2
    ERROR = 3

    def __init__(self, parent):
        self.parent = parent
        self.status_var = tk.StringVar(parent.tk, s.loading)

    def __str__(self):
        return self.status_var.get()

    def set_status(self, status, **kwargs):
        # TODO enable or disable some widget on status change.
        if status == self.LOADING:
            self.status_var.set(s.loading)
        elif status == self.READY:
            self.status_var.set(s.ready)
        elif status == self.RUNNING:
            if not kwargs:
                kwargs["task"] = ""
            self.status_var.set(s.running.format(**kwargs))
        elif status == self.ERROR:
            self.status_var.set(s.error)
            try:
                Cache.running.thread.join()
            except Exception:
                messagebox.showerror(s.error, Cache.message)


class Cache:
    # tasks.
    running = None
    devices = []
    message = ""


if __name__ == '__main__':
    freeze_support()
    MainWindow().main_loop()
    # messagebox.showinfo(s.hello_title, s.hello_info)
    # messagebox.askokcancel("确认？")
