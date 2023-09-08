from prettytable import PrettyTable
from S_Header import *
import json
import textwrap

def wrap(text):
    return "\n".join(textwrap.wrap(text, 50))

def show_result(url):
    data = analyze(url)
    print("{}[+]{} Analyzing Security Header of : {}".format(Clr.Green,Clr.RESET,url))
    print("\t==> Site: {}{}{}".format(Clr.White,data["Host Name"],Clr.RESET))
    print("\t==> IP Address: {}{}{}".format(Clr.White,data["Host IP"],Clr.RESET))
    print("{}[+]{}Security Report Summary :\n".format(Clr.Green,Clr.RESET))

    

    x = PrettyTable(["Headers","Value","Rating","Description"])

    for header, info in data["headers"].items():
        ff = info["rating"]
        header_text = header
        value = info.get("value", "---")
        description = info.get("description",'---')
        x.add_row([header_text, wrap(value), info["rating"], wrap(description)])
    print(x)


show_result("https://google.com")



