import re
from html.parser import HTMLParser
from sqlalchemy import create_engine
import sqlite3
import requests
from bs4 import BeautifulSoup




if __name__ == '__main__':
    # with open("wifi_data.txt", "w") as file:
    #     file.write(str(re.findall('<td> <a href="(.*?)" title=".*?">(.*?)</a>', html)))
    class Parser(HTMLParser):
        def error(self, message):
            pass

        def handle_data(self, data):
            if not re.fullmatch("\s+", data.strip()) and data != "" and data != "\n":
                print(data.strip(), end="\n")

    def update_data(html_cache=None):
        if html_cache:
            with open(html_cache) as file:
                data_html = file.read()
        else:
            data_html = requests.get("http://wiki.joyme.com/arknights/%E5%B9%B2%E5%91%98%E6%95%B0%E6%8D%AE%E8%A1%A8").content.decode()
        soup = BeautifulSoup(data_html)
        wifi = soup.find("table", id="CardSelectTr").find_all("tr")
        for i, w in enumerate(wifi):
            if i == 0:
                continue
            data = []
            for info in w.find_all("td"):
                data.append(re.sub("\s", "", info.text))
            data[-1] = data[-1].split("、")
            print(data)

    # update_data("wiki.html")
    engine = create_engine("sqlite:///wifi.db")

