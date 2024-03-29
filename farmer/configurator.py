import json
import os
from tkinter import filedialog, messagebox
from farmer.utils import resource_path
from farmer import skin

CONFIG_PATH = resource_path("config.json")
DEFAULT_CONFIG_PATH = resource_path("config_default.json")
BROKEN_CONFIG_PATH = resource_path("config_broken.json")


class Configurator:
    def __init__(self):
        self.config = self.load(init=True)

        # preload skin
        try:
            self.skin = getattr(skin, self.config.get("skin"))
        except (AttributeError, TypeError):
            self.skin = skin.Default

    def load(self, config_path=CONFIG_PATH, init=False):
        def _load(file_path):
            with open(file_path, encoding="utf-8") as f:
                return json.load(f)
        try:
            config = _load(config_path)
        except FileNotFoundError:
            if not init:
                return None
            config = _load(DEFAULT_CONFIG_PATH)
        except:
            if not init:
                return None
            messagebox.showwarning(s.warning, s.broken_file_warning)
            if config_path == CONFIG_PATH:
                os.rename(CONFIG_PATH, BROKEN_CONFIG_PATH)
            config = _load(DEFAULT_CONFIG_PATH)

        if not config_path == CONFIG_PATH:
            self.save()
        return config

    def save(self, *args, **kwargs):
        """
        Simple persistent storage.
        :return: None
        """
        # save skin
        self.config["skin"] = self.skin.__name__

        with open(CONFIG_PATH, "w", encoding="utf-8") as file:
            json.dump(self.config, file, ensure_ascii=False)

    def export(self):
        file = filedialog.asksaveasfile(filetypes=[("JSON", ".json")], defaultextension=".json")
        if file is not None:
            self.save()
            json.dump(self.config, file, ensure_ascii=False)

    def import_(self):
        if messagebox.askokcancel("导入配置", "导入将覆盖现有配置，确定吗？"):
            os.remove(CONFIG_PATH)
            self.load(filedialog.askopenfilename())

    def reset(self):
        if messagebox.askokcancel("恢复默认配置", "真的要恢复默认配置吗？"):
            self.load(DEFAULT_CONFIG_PATH)


configurator = Configurator()
conf = configurator.config
s = configurator.skin.Strings

if __name__ == '__main__':
    print(configurator.skin)
