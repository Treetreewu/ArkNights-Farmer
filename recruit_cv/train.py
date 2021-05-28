import itertools
import os
import re
import shutil
import subprocess

from farmer.data import TAGS

DIR = os.path.split(__file__)[0]
os.chdir(DIR)
TESSERACT_PATH = None

GROUPS = {
    "hr": {
        "font": "Noto Sans CJK SC Regular",
        "words": TAGS.keys()
    },
}


# Command line equivalent:

# text2image --text dicts/hr.txt --font 'Noto Sans CJK SC Regular' --fonts_dir ./fonts/ --outputbase hr.notosans.exp0 --fontconfig_tmpdir ./ --ptsize 25
# tesseract hr.notosans.exp0.tif hr.notosans.exp0 nobatch box.train
# unicharset_extractor ./hr.notosans.exp0.box
# mftraining -F font_properties -U unicharset -O hr.unicharset hr.notosans.exp0.tr
# cntraining ./hr.notosans.exp0.tr
# mv normproto hr.normproto
# mv inttemp hr.inttemp
# mv pffmtable hr.pffmtable
# mv shapetable hr.shapetable
# combine_tessdata hr.


def execute(command: str, *args):
    if TESSERACT_PATH:
        command = os.path.join(TESSERACT_PATH, command)
    result = subprocess.check_output([command, *args])
    return result


def train(name):
    # make text dict
    full_set = set(itertools.chain(*GROUPS[name]["words"]))
    os.makedirs("dicts", exist_ok=True)
    with open(os.path.join("dicts", f"{name}.txt"), "w",
              encoding="utf-8") as file:
        text = "".join(full_set)
        # Workaround for https://github.com/tesseract-ocr/tesseract/issues/1166
        text *= 3
        file.write(text)

    # train
    font = GROUPS[name]["font"]
    execute(
        "text2image", "--text", f"dicts/{name}.txt", "--font", font,
        "--fonts_dir", "./fonts", "--outputbase", f"{name}.a_font.exp0",
        "--fontconfig_tmpdir", DIR)  # , "--ptsize", "22")
    execute("tesseract", "--oem", "1", f"{name}.a_font.exp0.tif",
            f"{name}.a_font.exp0", "nobatch", "box.train")
    execute("unicharset_extractor", f"{name}.a_font.exp0.box")
    execute(
        "mftraining", "-F", "font_properties", "-U", "unicharset",
        "-O", f"{name}.unicharset", f"{name}.a_font.exp0.tr")
    execute("cntraining", f"{name}.a_font.exp0.tr")

    for file in ("normproto", "inttemp", "pffmtable", "shapetable"):
        shutil.move(os.path.join(DIR, file),
                    os.path.join(DIR, f"{name}.{file}"))
    execute("combine_tessdata", f"{name}.")


if __name__ == '__main__':
    train("hr")

